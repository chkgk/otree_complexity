from otree.api import *
import json

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'training'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    TRAINING_SECONDS = 120
    REQUEST_TIMEOUT_SECONDS = 0
    INFO_HIGHLIGHT_TIMEOUT_SECONDS = 1

class Subsession(BaseSubsession):
    players_per_group = models.IntegerField()
    initial_stock = models.IntegerField()
    initial_cash = models.FloatField()
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


# FUNCTIONS
def creating_session(subsession):
    players_per_group = subsession.session.config.get('players_per_group', None)
    initial_stock = subsession.session.config.get('training_initial_stock', None)
    initial_cash = subsession.session.config.get('training_initial_cash', None)
    cost_per_second = subsession.session.config.get('training_cost_per_second', None)
    price_per_unit = subsession.session.config.get('training_price_per_unit', None)
    round_seconds = subsession.session.config.get('training_round_seconds', None)
    show_chain = subsession.session.config.get('training_show_chain', False)

    if any(var is None for var in
           [players_per_group, initial_stock, initial_cash, cost_per_second, price_per_unit, round_seconds,
            show_chain]):
        raise ValueError("session not configured correctly")

    subsession.players_per_group = players_per_group
    subsession.initial_stock = initial_stock
    subsession.initial_cash = initial_cash
    subsession.cost_per_second = cost_per_second
    subsession.price_per_unit = price_per_unit
    subsession.round_seconds = round_seconds
    subsession.show_chain = show_chain

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
    }


# PAGES
class TrainingIntro(Page):
    pass

class TrainingRound(Page):
    def get_timeout_seconds(player):
        return player.subsession.round_seconds

    @staticmethod
    def js_vars(player):
        return {
            'own_id_in_group': player.id_in_group,
            'request_button_timeout_seconds': C.REQUEST_TIMEOUT_SECONDS,
            'info_highlight_timeout_seconds': C.INFO_HIGHLIGHT_TIMEOUT_SECONDS,
            'inventory_unit_cost_per_second': player.subsession.cost_per_second,
            'transfer_probability': 0.5,
            'inventory_unit_price': player.subsession.price_per_unit,
            
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
    # FigureDemo,
    TrainingIntro, 
    TrainingRound, 
    TrainingFeedback
]
