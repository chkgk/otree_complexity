from otree.api import *
from settings import BASE_URL

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'training'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    

class Subsession(BaseSubsession):
    players_per_group = models.IntegerField()
    initial_stock = models.IntegerField()
    initial_cash = models.FloatField()
    cost_per_second = models.FloatField()
    price_per_unit = models.FloatField()
    show_chain = models.BooleanField(initial=False)
    transfer_probability = models.FloatField()

    start_delay_seconds = models.IntegerField()
    leave_seconds = models.IntegerField()
    round_seconds = models.IntegerField()
    total_seconds = models.IntegerField()
    request_timeout_seconds = models.IntegerField()
    info_highlight_timeout_seconds = models.IntegerField()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    inventory = models.IntegerField()
    balance = models.CurrencyField()

    last_inventory_update = models.FloatField()

    total_cost = models.CurrencyField(initial=0)
    total_revenue = models.CurrencyField(initial=0)
    total_profit = models.CurrencyField(initial=0)


# FUNCTIONS
def creating_session(subsession):
    sess = subsession.session
    players_per_group = sess.config.get('players_per_group', None)
    initial_stock = sess.config.get('training_initial_stock', None)
    initial_cash = sess.config.get('training_initial_cash', None)
    cost_per_second = sess.config.get('training_cost_per_second', None)
    price_per_unit = sess.config.get('training_price_per_unit', None)
    show_chain = sess.config.get('training_show_chain', False)
    transfer_probability = sess.config.get('training_transfer_probability', None)
    
    start_delay_seconds = sess.config.get('training_start_delay_seconds', None)
    leave_seconds = sess.config.get('training_leave_seconds', None)
    round_seconds = sess.config.get('training_round_seconds', None)
    request_timeout_seconds = sess.config.get('training_request_timeout_seconds', None)
    info_highlight_timeout_seconds = sess.config.get('training_info_highlight_timeout_seconds', None)
    total_seconds = start_delay_seconds + round_seconds

    if any(var is None for var in
           [players_per_group, initial_stock, initial_cash, cost_per_second, price_per_unit,
            show_chain, transfer_probability, start_delay_seconds, leave_seconds, round_seconds, request_timeout_seconds,info_highlight_timeout_seconds]):
        raise ValueError("session not configured correctly")

    subsession.players_per_group = players_per_group
    subsession.initial_stock = initial_stock
    subsession.initial_cash = initial_cash
    subsession.cost_per_second = cost_per_second
    subsession.price_per_unit = price_per_unit
    subsession.show_chain = show_chain
    subsession.transfer_probability = transfer_probability

    subsession.round_seconds = round_seconds
    subsession.start_delay_seconds = start_delay_seconds
    subsession.leave_seconds = leave_seconds
    subsession.request_timeout_seconds = request_timeout_seconds
    subsession.info_highlight_timeout_seconds = info_highlight_timeout_seconds
    subsession.total_seconds = total_seconds

    player_list = subsession.get_players()

    # assign endowments to players
    for player in player_list:
        player.inventory = initial_stock
        player.balance = initial_stock

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
        'info_highlight_timeout_seconds': subs.info_highlight_timeout_seconds,
        'training_start_delay_seconds': subs.start_delay_seconds,
        'training_seconds': subs.round_seconds,
        'allow_training_leave_seconds': subs.leave_seconds,
        'transfer_probability': subs.transfer_probability,
    }


# PAGES
class TrainingRound(Page):
    def get_timeout_seconds(player):
        return player.subsession.total_seconds

    @staticmethod
    def js_vars(player):
        subs = player.subsession
        return {
            'own_id_in_group': player.id_in_group,
            'request_button_timeout_seconds': subs.request_timeout_seconds,
            'inventory_unit_cost_per_second': subs.cost_per_second,
            'inventory_unit_price': subs.price_per_unit,
            **common_vars_for_template(player),
        }

    @staticmethod
    def vars_for_template(player):
        return {
            **common_vars_for_template(player),
        }
    
class TrainingFeedback(Page):
    pass


page_sequence = [
    TrainingRound, 
    TrainingFeedback
]
