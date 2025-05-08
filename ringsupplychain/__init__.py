from otree.api import *
import time
import itertools
import json

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ringsupplychain'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    
    # Timeouts
    DECISION_TIMEOUT_SECONDS = 300  # 5 min
    REQUEST_TIMEOUT_SECONDS = 0
    INFO_HIGHLIGHT_TIMEOUT_SECONDS = 1
    


class Subsession(BaseSubsession):
    players_per_group = models.IntegerField()
    initial_stock = models.StringField()
    initial_cash = models.StringField()
    cost_per_second = models.FloatField()
    price_per_unit = models.FloatField()
    round_seconds = models.IntegerField()
    show_chain = models.BooleanField(initial=False)


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
            return self.subsession.players_per_group
        else:
            return self.id_in_group - 1
    
class Requests(ExtraModel):
    created = models.FloatField()
    session_code = models.StringField()
    group_id = models.IntegerField()
    round = models.IntegerField()
    requested_from_id = models.IntegerField()
    requested_by_id = models.IntegerField()
    units = models.IntegerField()
    transferred = models.BooleanField()

# FUNCTIONS
def creating_session(subsession):
    players_per_group = subsession.session.config.get('players_per_group', None)
    initial_stock = subsession.session.config.get('initial_stock', None)
    initial_cash = subsession.session.config.get('initial_cash', None)
    cost_per_second = subsession.session.config.get('cost_per_second', None)
    price_per_unit = subsession.session.config.get('price_per_unit', None)
    round_seconds = subsession.session.config.get('round_seconds', None)
    show_chain = subsession.session.config.get('show_chain', False)
    
    if any(var is None for var in [players_per_group, initial_stock, initial_cash, cost_per_second, price_per_unit, round_seconds, show_chain]):
        raise ValueError("session not configured correctly")
    
    subsession.players_per_group = players_per_group
    subsession.initial_stock = json.dumps(initial_stock)
    subsession.initial_cash = json.dumps(initial_cash)
    subsession.cost_per_second = cost_per_second
    subsession.price_per_unit = price_per_unit
    subsession.round_seconds = round_seconds[subsession.round_number - 1]
    subsession.show_chain = show_chain
    
    player_list = subsession.get_players()

    # match groups
    if subsession.round_number == 1:
        # check if the number of players is divisible by the number of players per group
        if subsession.session.num_participants % players_per_group != 0:
            raise ValueError("Number of players must be divisible by players_per_group")
        gm = [list(group) for group in itertools.batched(player_list, players_per_group)]
        subsession.set_group_matrix(gm)
    else:
        # if not the first round, set group matrix to the same as the first round
        # partner matching
        subsession.group_like_round(1)
        
        
    if any([len(var) != players_per_group for var in [initial_stock, initial_cash]]):
        raise ValueError("initial_total_stock and initial_total_cash must be of length players_per_group")

    # assign endowments to players
    for player in player_list:
        player.inventory = initial_stock[player.id_in_group - 1]
        player.balance = initial_stock[player.id_in_group - 1]

def live_inventory(player):
    # get current time
    current_time = time.time()

    # get time delta
    time_delta = current_time - player.last_inventory_update

    # calculate cost
    old_inventory = player.inventory
    cost = time_delta * player.subsession.cost_per_second * old_inventory

    # update total cost
    player.total_cost += cost

    # update balance
    player.balance -= cost

    # update profit
    player.total_profit = player.total_revenue - player.total_cost

    # update last inventory update time
    player.last_inventory_update = current_time

    resp = {
        'type': 'init_response',
        'data': {
            'inventory': player.inventory,
            'balance': player.balance,
            'cost': player.total_cost,
            'revenue': player.total_revenue,
            'profit': player.total_profit,
        }
    }
    
    return {player.id_in_subsession: resp}

def live_request(player, data):
    take_from = player.get_predecessor()
    units = data['units']

    group = player.group
    subsession = player.subsession
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
        from_cost = from_time_delta * subsession.cost_per_second * from_old_inventory
        take_from_player.total_cost += from_cost
        
        # transfer to player costs
        to_last_update = give_to_player.last_inventory_update
        to_time_delta = current_time - to_last_update
        to_old_inventory = give_to_player.inventory
        to_cost = to_time_delta * subsession.cost_per_second * to_old_inventory
        give_to_player.total_cost += to_cost

        # update inventory 
        take_from_player.inventory -= units
        give_to_player.inventory += units
        
        # update balance and revenue
        from_revenue = units * subsession.price_per_unit
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
        round=player.round_number,
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
    subs = player.subsession
    return {
        'balance': player.balance,
        'inventory': int(player.inventory),
        'total_cost': player.total_cost,
        'total_revenue': player.total_revenue,
        'total_profit': player.total_profit,
        'num_players': subs.players_per_group,
        'show_chain': subs.show_chain,
    }

# PAGES
class JointStart(WaitPage):
    pass

class Decision(Page):
    def get_timeout_seconds(player):
        return player.subsession.round_seconds
    
    @staticmethod
    def js_vars(player):
        return {
            'own_id_in_group': player.id_in_group,
            'request_button_timeout_seconds': C.REQUEST_TIMEOUT_SECONDS,
            'info_highlight_timeout_seconds': C.INFO_HIGHLIGHT_TIMEOUT_SECONDS,
            'inventory_unit_cost_per_second': player.subsession.cost_per_second,
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
            if player.field_maybe_none('last_inventory_update') is None:
                player.last_inventory_update = time.time()
            else:
                # send update
                return live_inventory(player)
            return None
        
        if data['type'] == 'request':
            return live_request(player, data['data'])
        
        return None
        

class Results(Page):
    pass


page_sequence = [JointStart, Decision, Results]


# EXPORTS
def custom_export(players):
    yield ['time', 'session', 'round', 'group', 'requested_from', 'requested_by', 'units', 'transferred']
    for request in Requests.filter():
        yield [request.created, 
               request.session_code,
               request.round,
               request.group_id,
               request.requested_from_id,
               request.requested_by_id,
               request.units,
               request.transferred
        ]