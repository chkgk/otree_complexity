from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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


# FUNCTIONS
def consent_given_error_message(player, value):
    if not value:
        return "You must agree to participate in the experiment. If you do not agree, please contact the experimenter."
    return None

# PAGES

class FigureDemo(Page):
    def js_vars(player):
        return {
            "own_id_in_group": player.id_in_group,
        }
    
    
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent_given']


class Introduction(Page):
    pass

class InstructionsRound(Page):
    pass

page_sequence = [
    # FigureDemo, 
    Consent, 
    Introduction, 
    InstructionsRound
]
