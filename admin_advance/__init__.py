from otree.api import *
import os
import json

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'admin_advance'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    ADVANCE_PAGES = ['MyPage', 'MyPage2']

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
def vars_for_admin_report(subsession: Subsession):
    s = subsession.session

    player_states = dict()
    for p in subsession.get_players():
        player_states[p.id_in_subsession] = p.participant.pages_completed
    
    return {
        "rest_key": os.getenv('OTREE_REST_KEY', ''),
        "session_code": s.code,
        "advance_pages": json.dumps(s.advance_pages),
        "player_states": json.dumps(player_states)
    }

# FUNCTIONS
def ensure_page_completed(player: Player, current_page_name=None):
    participant = player.participant
    if current_page_name is None:
        current_page_name = participant._current_page_name
        
    if current_page_name not in participant.pages_completed:
        participant.pages_completed.append(current_page_name)

def live_page_advance_check(player, data):
    current_page_name = player.participant._current_page_name
    ensure_page_completed(player, current_page_name)

    if player.session.advance_pages.get(current_page_name, False):
        return {0: {'advance': current_page_name}}
    return None

def add_pages_to_session_vars(subsession, add_pages):
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
class MyPage(Page):
    @staticmethod
    def live_method(player, data):
        return live_page_advance_check(player, data)

    @staticmethod
    def js_vars(player):
        return {
            "player_id": player.id_in_group,
            "current_page_name": player.participant._current_page_name
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        ensure_page_completed(player)
        # make sure that if the first player leaves the page in debug, the others do not have to wait either.
        if player.id_in_group == 1:
            player.session.vars[f"advance_{player.participant._current_page_name}"] = True


class MyPage2(Page):
    @staticmethod
    def live_method(player, data):
        return live_page_advance_check(player, data)

    @staticmethod
    def js_vars(player):
        return {
            "player_id": player.id_in_group,
            "current_page_name": player.participant._current_page_name
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        ensure_page_completed(player)
        # make sure that if the first player leaves the page in debug, the others do not have to wait either.
        if player.id_in_group == 1:
            player.session.vars[f"advance_{player.participant._current_page_name}"] = True

class Results(Page):
    pass


page_sequence = [MyPage, MyPage2, Results]
