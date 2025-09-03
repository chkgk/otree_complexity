from otree.api import *
from datetime import datetime
from otree.settings import DEBUG
import os
import json

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ADVANCE_PAGES = ['ConsentRadboud', 'GameInstructions']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent_given = models.BooleanField(
        label="I have read the information above and I want to participate in this experiment.",
        choices=[
            [True, "Yes"],
            [False, "No"],
        ],
        widget=widgets.RadioSelect,
    )

    confirm_read_understood = models.BooleanField(widget=widgets.CheckboxInput)
    voluntary_participation = models.BooleanField(widget=widgets.CheckboxInput)
    data_access_by_authorities = models.BooleanField(widget=widgets.CheckboxInput)
    data_anonymity = models.BooleanField(widget=widgets.CheckboxInput)
    data_publication = models.BooleanField(widget=widgets.CheckboxInput)
    future_research_use = models.BooleanField(widget=widgets.CheckboxInput)
    agree_to_participate = models.BooleanField(widget=widgets.CheckboxInput)
    confirm_info_reviewed_again = models.BooleanField(widget=widgets.CheckboxInput)


# FUNCTIONS
def vars_for_admin_report(subsession: Subsession):
    s = subsession.session

    player_states = dict()
    player_labels = dict()
    player_finished = dict()
    for p in subsession.get_players():
        part = p.participant
        player_states[p.id_in_subsession] = part.pages_completed
        player_labels[p.id_in_subsession] = part.label
        player_finished[p.id_in_subsession] = part.vars.get('finished', False)

    return {
        "rest_key": os.getenv('OTREE_REST_KEY', ''),
        "session_code": s.code,
        "advance_pages": json.dumps(s.advance_pages),
        "player_states": json.dumps(player_states),
        "player_labels": json.dumps(player_labels),
        "player_finished": json.dumps(player_finished)
    }


def consent_given_error_message(player, value):
    if not value:
        return "You must agree to participate in the experiment. If you do not agree, please contact the experimenter."
    return None


def ensure_page_completed(player: Player, current_page_name=None):
    # This function ensures that the current page is marked as completed in participant.vars['pages_completed']
    
    # Get the participant and the current plage name
    participant = player.participant
    if current_page_name is None:
        current_page_name = participant._current_page_name

    # Initialize pages_completed if it doesn't exist#
    if 'pages_completed' not in participant.vars:
        participant.vars['pages_completed'] = []
        
    # Add the current page to pages_completed if not already present
    if current_page_name not in participant.pages_completed:
        participant.pages_completed.append(current_page_name)


def live_page_advance_check(player, data):
    # This function checks if the current page is in the session's advance_pages and if it should be advanced
    current_page_name = player.participant._current_page_name
    ensure_page_completed(player, current_page_name)

    # If the current page is in advance_pages and is marked True, return the advance signal
    if player.session.advance_pages.get(current_page_name, False):
        return {0: {'advance': current_page_name}}
    return None


def add_pages_to_session_vars(subsession, add_pages):
    # This function adds pages to the session's advance_pages dict if they are not already present
    # This is useful so that the admin page can show pages from all apps
    session_advance_pages = subsession.session.vars.get("advance_pages", dict())
    for page in add_pages:
        if page not in session_advance_pages:
            session_advance_pages[page] = False

    subsession.session.advance_pages = session_advance_pages


def creating_session(subsession: Subsession):
    add_pages_to_session_vars(subsession, C.ADVANCE_PAGES)
    for p in subsession.get_players():
        p.participant.pages_completed = list()

# PAGES

# Not currently used, but can be used to show a demo of the supply chain figure
class FigureDemo(Page):
    def js_vars(player):
        return {
            "own_id_in_group": player.id_in_group,
        }
    
class Welcome(Page):
    def vars_for_template(player):
        return {
            'participation_fee': player.session.config.get('participation_fee', '0.00 EUR')
        }
    
class ConsentRadboud(Page):
    form_model = 'player'
    form_fields = [
        'confirm_read_understood',
        'voluntary_participation',
        'data_access_by_authorities',
        'data_anonymity',
        'data_publication',
        'future_research_use',
        'agree_to_participate',
        'confirm_info_reviewed_again',
    ]
    
    def error_message(self, values):
        required_checks = [
            'confirm_read_understood',
            'voluntary_participation',
            'data_access_by_authorities',
            'data_anonymity',
            'data_publication',
            'future_research_use',
            'agree_to_participate',
            'confirm_info_reviewed_again'
        ]
        unchecked = [field for field in required_checks if not values.get(field)]
        if unchecked:
            return "You must check all boxes to continue."
        return None
    
    def vars_for_template(player):
        return {
            'consent_date': datetime.now().strftime("%Y-%m-%d"),
            'participation_fee': player.session.config.get('participation_fee', '0.00 EUR'),
            'DEBUG': DEBUG
        }

    @staticmethod
    def js_vars(player):
        return {
            "player_id": player.id_in_group,
            "current_page_name": player.participant._current_page_name
        }

    @staticmethod
    def live_method(player, data):
        return live_page_advance_check(player, data)

    @staticmethod
    def before_next_page(player, timeout_happened):
        ensure_page_completed(player)


class GameInstructions(Page):  
    def vars_for_template(player):
        sess = player.session
        rwc_pp = sess.config.get('real_world_currency_per_point', 0.01)
        hundred_ecu = 100 * rwc_pp
        players_per_group = sess.config.get('players_per_group', 5)
        show_chain = sess.config.get('show_chain', False)
        half = players_per_group // 2
        middle_pos = half if players_per_group % 2 == 0 else half + 1
        
        initial_cash_rounds = sess.config.get('initial_cash', None)
        initial_cash_rounds = [[int(x.strip()) for x in blocks.split(',')] for blocks in initial_cash_rounds.split(';')] if initial_cash_rounds else [[0]]
        initial_cash = initial_cash_rounds[0][0]

        ecu_earn = sess.config.get('price_per_unit', "10").split(';')[0]
        ecu_inventory_cost = sess.config.get('cost_per_second', "5").split(';')[0]
        
        return {
            'exchange_rate': f"100 ECU = {hundred_ecu:.2f} €",
            'num_participants': players_per_group if show_chain else "several",
            'show_chain': show_chain,
            'DEBUG': DEBUG,
            'own_id_in_group': middle_pos,
            'ecu_endowment': initial_cash ,
            'ecu_earn': ecu_earn,
            'ecu_inventory_cost': ecu_inventory_cost,
            'round_seconds': sess.config.get('round_seconds', 30),
            'num_rounds': sess.config.get('num_rounds', 1),
            'training_round_seconds': sess.config.get('training_round_seconds', 30),
        }
    
    @staticmethod
    def live_method(player, data):
        return live_page_advance_check(player, data)

    @staticmethod
    def before_next_page(player, timeout_happened):
        ensure_page_completed(player)
    
    @staticmethod
    def js_vars(player):
        players_per_group = player.session.config.get('players_per_group', 5)
        half = players_per_group // 2
        middle_pos = half if players_per_group % 2 == 0 else half + 1
        return {
            'own_id_in_group': middle_pos,
            'players_per_group': players_per_group,
            "player_id": player.id_in_group,
            "current_page_name": player.participant._current_page_name
        }

page_sequence = [
    # FigureDemo, 
    Welcome,
    ConsentRadboud, 
    GameInstructions
]
