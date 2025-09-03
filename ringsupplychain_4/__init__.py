from otree.api import *
import time
import itertools
import json
import math
import random
from collections import defaultdict
from settings import BASE_URL
from otree.settings import DEBUG

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ringsupplychain4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3 


class Subsession(BaseSubsession):
    # We store most configuration variables in the subsession, because they can vary by round
    # these variables are set in creating_session
    players_per_group = models.IntegerField()
    initial_stock = models.StringField()
    initial_cash = models.StringField()
    cost_per_second = models.FloatField()
    price_per_unit = models.FloatField()
    round_seconds = models.IntegerField()
    total_seconds = models.IntegerField()
    show_chain = models.BooleanField(initial=False)
    room_name = models.StringField()
    auto_play = models.BooleanField(initial=False)
    request_timeout_seconds = models.IntegerField()
    info_highlight_timeout_seconds = models.IntegerField()
    countdown_seconds = models.IntegerField()
    treatment = models.StringField()


class Group(BaseGroup):
    start_time = models.FloatField()


class Player(BasePlayer):
    inventory = models.IntegerField()
    balance = models.CurrencyField()
    
    last_inventory_update = models.FloatField()
    init_time = models.FloatField()
    
    total_cost = models.CurrencyField(initial=0)
    total_revenue = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)
    total_items_sold = models.IntegerField(initial=0)
    
    proposed_start_time = models.FloatField()
    
    def get_predecessor(self):
        if self.id_in_group == 1:
            return self.subsession.players_per_group
        else:
            return self.id_in_group - 1
    
class Requests(ExtraModel):
    # We use this model to store all requests made by players
    # This allows us to analyze the data later in more detail
    created = models.FloatField()
    session = models.Link(Subsession)
    group_id = models.IntegerField()
    round = models.IntegerField()
    requested_from_id = models.IntegerField()
    requested_by_id = models.IntegerField()
    units = models.IntegerField()
    transferred = models.BooleanField()
    from_inventory = models.IntegerField()
    from_balance = models.CurrencyField()
    to_inventory = models.IntegerField()
    to_balance = models.CurrencyField()
    kind = models.StringField(choices=['request', 'init'], default='request')


# FUNCTIONS
def shuffled(l):
    # Helper function to shuffle a list and return the shuffled list
    random.shuffle(l)
    return l

# At some point we discussed being able to flexibly choose the treatments for each round
# This is not readily available in oTree, so the workaround was to return participants to an oTree room / lobby
# to wait for the next session to start. I implemented this features here, but we ultimately decided not to use it.
def close_room(subsession):
    # This function makes sure the room is closed, i.e. it does not have an active session.
    room = subsession.session.get_room()
    if room is not None:
        room.set_session(None)

def register_room(subsession):
    # This function registers lets us know which room the session is running in, if any.
    room = subsession.session.get_room()
    room_name = room.name if room is not None else None
    subsession.room_name = room_name


def creating_session(subsession):
    # When a session is created, we look up the configuration values in the session config and store it in th session
    sess = subsession.session
    players_per_group = sess.config.get('players_per_group', None)
    initial_stock = sess.config.get('initial_stock', None)
    initial_cash = sess.config.get('initial_cash', None)
    cost_per_second = sess.config.get('cost_per_second', None)
    price_per_unit = sess.config.get('price_per_unit', None)
    round_seconds = sess.config.get('round_seconds', None)
    show_chain = sess.config.get('show_chain', False)
    auto_play = sess.config.get('auto_play', False)
    request_timeout_seconds = sess.config.get('request_timeout_seconds', None)
    info_highlight_timeout_seconds = sess.config.get('info_highlight_timeout_seconds', None)
    countdown_seconds = sess.config.get('countdown_seconds', 5)
    total_seconds = countdown_seconds + round_seconds
    treatment = sess.config.get('treatment', None)
    
    # If any of the required variables are not set, raise an error
    if any(var is None for var in [players_per_group, initial_stock, initial_cash, cost_per_second, price_per_unit, round_seconds, show_chain, request_timeout_seconds, info_highlight_timeout_seconds, countdown_seconds, treatment]):
        raise ValueError("session not configured correctly")
    
    # There are two ways to specify the length of a round.
    # If a single integer is given, we use it for all rounds,
    # Otherwise, if a list is given, we use the respective entry for each round.
    if type(round_seconds) is not list:
        round_seconds = [round_seconds] * C.NUM_ROUNDS
    
    # transform into variables for each round:
    initial_stock_rounds = [[i.strip() for i in stock.split(",")] for stock in initial_stock.split(";")]
    initial_cash_rounds = [[i.strip() for i in cash.split(",")] for cash in initial_cash.split(";")]
    show_chain_rounds = [i.strip() for i in show_chain.split(";")]
    cost_per_second_rounds = [i.strip() for i in cost_per_second.split(";")]
    price_per_unit_rounds = [i.strip() for i in price_per_unit.split(";")]
    treatment_rounds = [i.strip() for i in treatment.split(";")]
    
    # assign variables
    subsession.players_per_group = players_per_group
    subsession.initial_stock = json.dumps(initial_stock_rounds[subsession.round_number - 1])
    subsession.initial_cash = json.dumps(initial_cash_rounds[subsession.round_number - 1])
    subsession.cost_per_second = float(cost_per_second_rounds[subsession.round_number - 1])
    subsession.price_per_unit = float(price_per_unit_rounds[subsession.round_number - 1])
    subsession.round_seconds = int(round_seconds[subsession.round_number - 1])
    subsession.show_chain = show_chain_rounds[subsession.round_number - 1] == 'True'
    subsession.treatment = treatment_rounds[subsession.round_number - 1]
    subsession.auto_play = auto_play
    subsession.request_timeout_seconds = request_timeout_seconds
    subsession.info_highlight_timeout_seconds = info_highlight_timeout_seconds
    subsession.total_seconds = total_seconds
    subsession.countdown_seconds = countdown_seconds
    
    player_list = subsession.get_players()
    
    # match groups
    if subsession.round_number == 1:
        # check if the number of players is divisible by the number of players per group
        if subsession.session.num_participants % players_per_group != 0:
            raise ValueError("Number of players must be divisible by players_per_group")
        gm = [list(group) for group in itertools.batched(player_list, players_per_group)]
        subsession.set_group_matrix(gm)
    else:
        # shuffled_player_list = shuffled(player_list)
        # gm = [list(group) for group in itertools.batched(shuffled_player_list, players_per_group)]
        # subsession.set_group_matrix(gm)
        # subsession.group_like_round(1)
        
        # We decided to keep the same groups for all rounds, but shuffle the positions within the group
        gm = subsession.in_round(1).get_group_matrix()
        new_gm = [shuffled(gr) for gr in gm]
        subsession.set_group_matrix(new_gm)

    # double-check whether the initial stock and cash lists are of the correct length
    if any([len(var) != players_per_group for var in [initial_stock_rounds[subsession.round_number - 1], initial_cash_rounds[subsession.round_number - 1]]]):
        raise ValueError("initial_total_stock and initial_total_cash must be of length players_per_group")

    # assign endowments to players
    for player in player_list:
        player.inventory = int(initial_stock_rounds[subsession.round_number - 1][player.id_in_group - 1])
        player.balance = cu(initial_cash_rounds[subsession.round_number - 1][player.id_in_group - 1])


def live_inventory(player):
    # Whenever the player loads or re-loads the decision page, we need to make sure they get the latest inventory and balance
    # Note:
    # This seems redundant at first, because we basically do the same calculations as in live_request and on the client side
    # However, it is necessary to do this here, because the player might reload the page or mess with the client-side code
    # Generally, we can never trust data that comes from the browser / client side, so we need to do the calculations on the server side as well.
    
    # First: calculate costs since last update
    # get current time
    current_time = time.time()

    # get time delta to last inventory update
    last_inventory_time = player.field_maybe_none('last_inventory_update')
    if last_inventory_time is None:
        last_inventory_time = current_time
    time_delta = current_time - last_inventory_time
    
    # calculate cost incurred since last update
    old_inventory = player.inventory
    cost = time_delta * player.subsession.cost_per_second * old_inventory

    # update total cost
    player.total_cost += cost

    # update balance
    player.balance -= cost

    # update profit
    player.total_profit = player.total_revenue - player.total_cost

    # update last inventory update time to the current time
    player.last_inventory_update = current_time

    # send the current status to the player's page
    resp = {
        'type': 'init_response',
        'data': {
            'inventory': player.inventory,
            'balance': player.balance,
            'cost': player.total_cost,
            'revenue': player.total_revenue,
            'profit': player.total_profit,
            'items_sold': player.total_items_sold,
            'chain_inventory': {p.id_in_group: p.inventory for p in player.group.get_players()},
        }
    }
    
    return {player.id_in_group: resp}

def live_request(player, data):
    # This function is triggered when a player sends a request for units to their predecessor
    
    # identify player to take from and the number of units requested
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

        # update inventories 
        take_from_player.inventory -= units
        take_from_player.total_items_sold += units
        give_to_player.inventory += units
        
        # update balances and revenues
        from_revenue = units * subsession.price_per_unit
        from_balance_change = from_revenue - from_cost
        take_from_player.balance += from_balance_change
        take_from_player.total_revenue += from_revenue
        
        to_balance_change = -1 * to_cost
        give_to_player.balance += to_balance_change
        
        # update profits
        take_from_player.total_profit = take_from_player.total_revenue - take_from_player.total_cost
        give_to_player.total_profit = give_to_player.total_revenue - give_to_player.total_cost
        
        # update last inventory update times
        take_from_player.last_inventory_update = current_time
        give_to_player.last_inventory_update = current_time
        
        transferred = True
        
    # We store every single request made in the Requests model for later analysis
    Requests.create(
        created=current_time,
        session=take_from_player.subsession,
        group_id=group.id_in_subsession,
        round=player.round_number,
        requested_from_id=take_from_player.id_in_group,
        requested_by_id=give_to_player.id_in_group,
        units=units,
        transferred=transferred,
        from_inventory=take_from_player.inventory,
        from_balance=take_from_player.balance,
        to_inventory=give_to_player.inventory,
        to_balance=give_to_player.balance,
    )
    
    # Send a status update to all players in the group, clearly identifying who requested / transferred how many units 
    # from whom to whom, and what the resulting inventories and balances are.
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
    # Some variables are needed both in the template and in the javascript on the template
    # To avoid repeating ourselves, we define a function that returns all these variables in a dictionary
    subs = player.subsession
    return {
        'balance': player.balance,
        'inventory': int(player.inventory),
        'price_per_unit': subs.price_per_unit,
        'total_cost': player.total_cost,
        'total_revenue': player.total_revenue,
        'total_profit': player.total_profit,
        'total_items_sold': player.total_items_sold,
        'num_players': subs.players_per_group,
        'show_chain': subs.show_chain,
        'auto_play': subs.auto_play,
        'round_seconds': subs.round_seconds,
        'total_seconds': subs.total_seconds,
        'request_button_timeout_seconds': subs.request_timeout_seconds,
        'info_highlight_timeout_seconds': subs.info_highlight_timeout_seconds,
        'countdown_seconds': subs.countdown_seconds,
        'DEBUG': DEBUG
    }

def finalize_round(group):
    # At the end of the round, we need to make sure that we account for any costs incurred since the last inventory update
    # This is similar to what we do in live_inventory, but we need to make sure we do it for all players in the group.
    
    subs = group.subsession
    round_seconds = subs.round_seconds
    cost_per_second = subs.cost_per_second
    for player in group.get_players():
        # first we figure out when the last update of the inventory took place relative to the expected end of round time
        init_time = player.field_maybe_none('init_time')
        if init_time is None:
            init_time = 0
        end_time = init_time + round_seconds
        last_update = player.field_maybe_none('last_inventory_update')
        if last_update is None:
            last_update = 0
        time_to_end_of_round = end_time - last_update
        
        # if there was time left between last update and the expected end of round, we need to account for costs.
        if time_to_end_of_round > 0:
            # calculate cost
            old_inventory = player.inventory
            cost = time_to_end_of_round * cost_per_second * old_inventory

            # update total cost, balance, and profit
            player.total_cost += cost
            player.balance -= cost
            player.total_profit = player.total_revenue - player.total_cost
            
        
        # store payment data on the participant
        game_data = {
            'ecu_earnings': int(player.total_profit),
            'eur_earnings': float(player.total_profit.to_real_world_currency(subs.session)),
            'round': player.round_number
        }
        
        if player.round_number == 1:
            player.participant.vars['game_rounds'] = [game_data]
        else:
            player.participant.vars['game_rounds'].append(game_data)
    

def start_time_check(player: Player, data):
    # This function implements the logic to determine the start time of the round
    # Each player proposes a start time, and when all players have proposed a time, the
    # maximum of these times is taken as the start time, unless there is not enough time left to communicate 
    # it to all players, in which case the start time is set to "current time + countdown_seconds".
    
    current_time = time.time()
    player.proposed_start_time = data['start_time']

    # Here we basically make a list of proposed start times from all players in the group
    subs = player.subsession
    group_players = player.group.get_players()
    proposed_start_times = list()
    for p in group_players:
        if p.field_maybe_none('proposed_start_time') is not None:
            proposed_start_times.append(p.proposed_start_time)
    
    # if all players have proposed a start time, we can determine the actual start time
    if len(proposed_start_times) == subs.players_per_group:
        # if the start time has already been set, we just return it
        if player.group.field_maybe_none('start_time') is not None:
            return {0: {
                'type': 'start_time_decision',
                'start_time': player.group.start_time
            }
        }
        
        # if it has not been set, we determine it now
        decision_candidate = max(proposed_start_times)
        if decision_candidate > current_time + subs.countdown_seconds:
            selected_time = decision_candidate
        else:
            selected_time = current_time + subs.countdown_seconds

        # store the selected start time
        player.group.start_time = selected_time
        
        # create an "init" request for each player, which is used to trigger the countdown on the client side
        for p in group_players:
            if p.field_maybe_none('last_inventory_update') is None:
                p.last_inventory_update = selected_time
    
            Requests.create(
                created=selected_time,
                # init is trigged on page load, but the countdown starts after the page is loaded
                session=subs,
                group_id=p.group.id_in_subsession,
                round=p.round_number,
                requested_from_id=p.id_in_group,
                requested_by_id=p.id_in_group,
                units=0,
                transferred=False,
                from_inventory=0,
                from_balance=0,
                to_inventory=0,
                to_balance=0,
                kind='init'
            )

        return {0: {
                'type': 'start_time_decision',
                'start_time': selected_time
            }
        }
    return None

def handle_init(player):
    # This function stores when the player first loaded the decision page
    # This is important to calculate the end of round time correctly
    # It prevents players from re-loading the page to reset their round time
    current_time = time.time()
    if player.field_maybe_none('init_time') is None:
        player.init_time = current_time
    return live_inventory(player)

# PAGES
class RoundPreface(Page):
    def vars_for_template(player):
        return common_vars_for_template(player)

class JointStart(WaitPage):
    pass
    # wait_for_all_groups = True
    # after_all_players_arrive = 'register_room'

class Decision(Page):
    def get_timeout_seconds(player):
        return player.subsession.total_seconds
    
    @staticmethod
    def js_vars(player):
        # There is some data that we need to provide both to the template in for the javascript on the template
        # We largely use a "common vars for template" function to avoid repeating ourselves
        return {
            'own_id_in_group': player.id_in_group,
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
        # If the page is loaded, it sends the "init" message to the server, which triggers the init handling
        if data['type'] == 'init':
            return handle_init(player)
                        
        # If the player sends a request message, we handle it here
        if data['type'] == 'request':
            return live_request(player, data['data'])
        
        # If the player sends a proposed start time, we handle it here
        if data['type'] == 'start_time_proposal':
            return start_time_check(player, data)
        return None
        
class ResultsWait(WaitPage):
    after_all_players_arrive = 'finalize_round'

class Results(Page):
    def vars_for_template(player):
        cv = common_vars_for_template(player)

        room = player.session.get_room()
        room_url = None
        if room is not None:
            target_room = 'room1' if room.name == 'room2' else 'room2'
            room_url = f"http://{BASE_URL}/room/{target_room}/"


        subs = player.subsession
        items_delivered = player.total_revenue / subs.price_per_unit if subs.price_per_unit > 0 else 0

        return {
            'room_url': room_url,
            'initial_balance': json.loads(subs.initial_cash)[player.id_in_group - 1],
            'num_items_delivered': int(items_delivered),
            **cv
        }

# These Back to Room (BTR) Pages are not currently in use
# We decided not to implement the feature of returning to a lobby / room between rounds
# but I am keeping the code here in case we want to use it in the future
class BTRWait(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'close_room'

class BackToRoom(Page):
    def is_displayed(player):
        room = player.subsession.field_maybe_none('room_name')
        return room is not None
    
    def vars_for_template(player):
        room = player.subsession.field_maybe_none('room_name')
        room_url = None
        if room is not None:
            room_url = f"http://{BASE_URL}/room/room1/"
            
        return {
            'room_url': room_url,
        }
        
# At some point we discussed showing players a figure of their balance and inventory over time
# We decided not to use this feature, but I am keeping the code here in case we want to use it in the future
class ResultsFigure(Page):
    def js_vars(player):
        subs = player.subsession

        reqs = Requests.filter(
            session=subs,
            group_id=player.group.id_in_subsession,
            round=player.round_number,
            transferred=True
        )
        own_reqs = [req for req in reqs if req.requested_by_id == player.id_in_group or req.requested_from_id == player.id_in_group]

        init_time = math.floor(player.init_time)
        end_time = math.ceil(init_time + subs.round_seconds)
    
        batches_sold = defaultdict(list)
        batches_received = defaultdict(list)
        for req in own_reqs:
            base_second = math.floor(req.created - init_time)
            if req.requested_from_id == player.id_in_group:
                # i sold something
                batches_sold[base_second].append(req)
            elif req.requested_by_id == player.id_in_group:
                # i received something
                batches_received[base_second].append(req)
            
        balance = list()
        inventory = list()
        
        initial_cash = json.loads(subs.initial_cash)[player.id_in_group - 1]
        initial_stock = json.loads(subs.initial_stock)[player.id_in_group - 1]
        
        for sec in range(subs.round_seconds + 1):
            if sec == 0:
                bal = initial_cash
                inv = initial_stock
            else:
                bal = balance[sec-1]
                inv = inventory[sec-1]

            bal -= subs.cost_per_second * inv
            
            for req in batches_sold[sec]:
                bal += req.units * subs.price_per_unit

            for req in batches_received[sec]:
                inv += req.units
                
            balance.append(bal)
            inventory.append(inv)
            

        return {
            'own_id_in_group': player.id_in_group,
            'init_time': init_time,
            'end_time': end_time,
            'round_seconds': subs.round_seconds,
            'balance': balance,
            'inventory': inventory,
        }
        

page_sequence = [
    RoundPreface,
    JointStart, 
    Decision, 
    ResultsWait, 
    Results, 
    # BTRWait, 
    # BackToRoom
]


# EXPORTS
def custom_export(players):
    yield ['time', 'subsession', 'round', 'group', 'kind', 'requested_from', 'requested_by', 'units', 'transferred', 'from_inventory', 'from_balance', 'to_inventory', 'to_balance']
    for request in Requests.filter():
        yield [request.created, 
               request.session.session.code,
               request.round,
               request.group_id,
               request.kind,
               request.requested_from_id,
               request.requested_by_id,
               request.units,
               request.transferred,
               request.from_inventory,
               request.from_balance,
               request.to_inventory,
               request.to_balance
        ]