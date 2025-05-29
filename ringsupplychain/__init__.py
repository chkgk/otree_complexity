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
    NAME_IN_URL = 'ringsupplychain'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1 


class Subsession(BaseSubsession):
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
    random.shuffle(l)
    return l

def creating_session(subsession):
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
    
    if any(var is None for var in [players_per_group, initial_stock, initial_cash, cost_per_second, price_per_unit, round_seconds, show_chain, request_timeout_seconds, info_highlight_timeout_seconds, countdown_seconds, treatment]):
        raise ValueError("session not configured correctly")
    
    # if it is not a list, make it a list
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
        gm = subsession.in_round(1).get_group_matrix()
        new_gm = [shuffled(gr) for gr in gm]
        subsession.set_group_matrix(new_gm)


    if any([len(var) != players_per_group for var in [initial_stock_rounds[subsession.round_number - 1], initial_cash_rounds[subsession.round_number - 1]]]):
        raise ValueError("initial_total_stock and initial_total_cash must be of length players_per_group")

    # assign endowments to players
    for player in player_list:
        player.inventory = int(initial_stock_rounds[subsession.round_number - 1][player.id_in_group - 1])
        player.balance = cu(initial_cash_rounds[subsession.round_number - 1][player.id_in_group - 1])

def live_inventory(player):
    # get current time
    current_time = time.time()

    # get time delta
    last_inventory_time = player.field_maybe_none('last_inventory_update')
    if last_inventory_time is None:
        last_inventory_time = current_time
    time_delta = current_time - last_inventory_time
    

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
            'items_sold': player.total_items_sold,
            'chain_inventory': {p.id_in_group: p.inventory for p in player.group.get_players()},
        }
    }
    
    return {player.id_in_group: resp}

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
        take_from_player.total_items_sold += units
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
        
    # request record
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
        
        # print('init_time', init_time)
        # print('end_time', end_time)
        # print('last_update', last_update)
        # print('time_to_end_of_round', time_to_end_of_round)
        # if there was time left between last update and the expected end of round, we need to account for costs.
        if time_to_end_of_round > 0:
            # calculate cost
            old_inventory = player.inventory
            cost = time_to_end_of_round * cost_per_second * old_inventory

            # update total cost, balance, and profit
            player.total_cost += cost
            player.balance -= cost
            player.total_profit = player.total_revenue - player.total_cost
            
            # print('old_inventory', old_inventory)
            # print('cost', cost)
            # print('total_cost', player.total_cost)
            # print('balance', player.balance)
            # print('total_profit', player.total_profit)
        
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
        

def close_room(subsession):
    room = subsession.session.get_room()
    if room is not None:
        room.set_session(None)
        
def register_room(subsession):
    room = subsession.session.get_room()
    room_name = room.name if room is not None else None
    subsession.room_name = room_name


def start_time_check(player: Player, data):
    current_time = time.time()
    player.proposed_start_time = data['start_time']

    subs = player.subsession
    group_players = player.group.get_players()
    proposed_start_times = list()
    for p in group_players:
        if p.field_maybe_none('proposed_start_time') is not None:
            proposed_start_times.append(p.proposed_start_time)

    if len(proposed_start_times) == subs.players_per_group:
        if player.group.field_maybe_none('start_time') is not None:
            return {0: {
                'type': 'start_time_decision',
                'start_time': player.group.start_time
            }
            }

        decision_candidate = max(proposed_start_times)
        if decision_candidate > current_time + subs.countdown_seconds:
            selected_time = decision_candidate
        else:
            selected_time = current_time + subs.countdown_seconds

        player.group.start_time = selected_time

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
        if data['type'] == 'init':
            return handle_init(player)

        if data['type'] == 'request':
            return live_request(player, data['data'])

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