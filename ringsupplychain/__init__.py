from otree.api import *
import time

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ringsupplychain'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    
    # Timeouts
    DECISION_TIMEOUT_SECONDS = 300  # 5 min
    REQUEST_TIMEOUT_SECONDS = 1
    INFO_HIGHLIGHT_TIMEOUT_SECONDS = 1
    
    # Endowments   
    CASH_ENDOWMENT_PLAYER = { i: cu(30) for i in range(1, PLAYERS_PER_GROUP + 1) }
    UNIT_ENDOWMENT_PLAYER = { i: 2 for i in range(1, PLAYERS_PER_GROUP + 1) }
    
    # Prices & Costs
    PRICE_PER_UNIT = cu(10)
    INVENTORY_UNIT_COST_PER_SECOND = cu(1)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    inventory = models.IntegerField()
    balance = models.CurrencyField()
    
    last_inventory_update = models.FloatField()
    
    total_cost = models.CurrencyField(initial=0)
    total_revenue = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)
    
    def get_predecessor(self):
        if self.id_in_group == 1:
            return C.PLAYERS_PER_GROUP
        else:
            return self.id_in_group - 1
    
class Requests(ExtraModel):
    created = models.FloatField()
    session_code = models.StringField()
    group_id = models.IntegerField()
    requested_from_id = models.IntegerField()
    requested_by_id = models.IntegerField()
    units = models.IntegerField()
    transferred = models.BooleanField()

# FUNCTIONS
def get_endowments(player):
    return C.UNIT_ENDOWMENT_PLAYER[player.id_in_group], C.CASH_ENDOWMENT_PLAYER[player.id_in_group]

def creating_session(subsession):
    for player in subsession.get_players():
        initial_inventory, initial_balance = get_endowments(player)
        player.inventory = initial_inventory
        player.balance = initial_balance

def live_request(player, data):
    take_from = player.get_predecessor()
    units = data['units']

    group = player.group
    take_from_player = group.get_player_by_id(take_from)
    give_to_player = player

    # get current time
    current_time = time.time()

    from_revenue = 0
    transferred = False

    # Check if the take_from player has enough inventory
    if take_from_player.inventory >= units:
        # transfer from player costs
        from_last_update = take_from_player.last_inventory_update
        from_time_delta = current_time - from_last_update
        from_old_inventory = take_from_player.inventory
        from_cost = from_time_delta * C.INVENTORY_UNIT_COST_PER_SECOND * from_old_inventory
        take_from_player.total_cost += from_cost
        
        # transfer to player costs
        to_last_update = take_from_player.last_inventory_update
        to_time_delta = current_time - to_last_update
        to_old_inventory = take_from_player.inventory
        to_cost = to_time_delta * C.INVENTORY_UNIT_COST_PER_SECOND * to_old_inventory
        give_to_player.total_cost += to_cost

        # update inventory 
        take_from_player.inventory -= units
        give_to_player.inventory += units
        
        # update balance and revenue
        from_revenue = units * C.PRICE_PER_UNIT
        from_balance_change = from_revenue - from_cost
        take_from_player.balance += from_balance_change
        take_from_player.total_revenue += from_revenue
        
        to_balance_change = -1 * to_cost
        give_to_player.balance += to_balance_change
        
        # update profit
        take_from_player.total_profit = take_from_player.total_revenue - take_from_player.total_cost
        give_to_player.total_profit = give_to_player.total_revenue - give_to_player.total_cost
        
        # update last inventory update time
        take_from_player.last_inventory_update = current_time
        give_to_player.last_inventory_update = current_time
        
        transferred = True
        

    # Create a failed request record
    Requests.create(
        created=current_time,
        session_code=take_from_player.session.code,
        group_id=group.id_in_subsession,
        requested_from_id=take_from_player.id_in_group,
        requested_by_id=give_to_player.id_in_group,
        units=units,
        transferred=transferred
    )
    
    resp = {
        'type': 'status',
        'data': {
            'to_player': give_to_player.id_in_group,
            'from_player': take_from_player.id_in_group,
            'to_inventory': give_to_player.inventory,
            'to_balance': give_to_player.balance,
            'to_cost': give_to_player.total_cost,
            'to_revenue': give_to_player.total_revenue,
            'to_profit': give_to_player.total_profit,
            'from_inventory': take_from_player.inventory,
            'from_balance': take_from_player.balance,
            'from_cost': take_from_player.total_cost,
            'from_revenue': take_from_player.total_revenue,
            'from_profit': take_from_player.total_profit,
            'units': units,
            'cash': from_revenue,
            'transferred': transferred,
        }
    }
    
    return {0: resp}

def common_vars_for_template(player):
    return {
        'balance': int(player.balance),
        'inventory': int(player.inventory),
        'total_cost': int(player.total_cost),
        'total_revenue': int(player.total_revenue),
        'total_profit': int(player.total_profit),
    }

# PAGES
class JointStart(WaitPage):
    pass

class Decision(Page):
    timeout_seconds = C.DECISION_TIMEOUT_SECONDS    
    
    @staticmethod
    def js_vars(player):
        return {
            'own_id_in_group': player.id_in_group,
            'request_button_timeout_seconds': C.REQUEST_TIMEOUT_SECONDS,
            'info_highlight_timeout_seconds': C.INFO_HIGHLIGHT_TIMEOUT_SECONDS,
            'inventory_unit_cost_per_second': C.INVENTORY_UNIT_COST_PER_SECOND,
            **common_vars_for_template(player),
        }
    
    @staticmethod
    def vars_for_template(player):
        return {
            **common_vars_for_template(player),
        }
    
    @staticmethod
    def live_method(player, data):        
        if data['type'] == 'init':
            player.last_inventory_update = time.time()
            return None
        
        if data['type'] == 'request':
            return live_request(player, data['data'])
        
        return None
        

class Results(Page):
    pass


page_sequence = [JointStart, Decision, Results]


# EXPORTS
def custom_export(players):
    yield ['time', 'session', 'group', 'requested_from', 'requested_by', 'units', 'transferred']
    for request in Requests.filter():
        yield [request.created, 
               request.session_code,
               request.group_id,
               request.requested_from_id,
               request.requested_by_id,
               request.units,
               request.transferred
        ]