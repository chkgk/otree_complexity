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

    confirm_read_understood = models.BooleanField(widget=widgets.CheckboxInput)
    voluntary_participation = models.BooleanField(widget=widgets.CheckboxInput)
    data_access_by_authorities = models.BooleanField(widget=widgets.CheckboxInput)
    data_anonymity = models.BooleanField(widget=widgets.CheckboxInput)
    data_publication = models.BooleanField(widget=widgets.CheckboxInput)
    future_research_use = models.BooleanField(widget=widgets.CheckboxInput)
    agree_to_participate = models.BooleanField(widget=widgets.CheckboxInput)
    confirm_info_reviewed_again = models.BooleanField(widget=widgets.CheckboxInput)
    instructor_code_1 = models.IntegerField()
    instructor_code_2 = models.IntegerField()


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
        'instructor_code_1'
    ]
    
def instructor_code_1_error_message(player, value):
    if value != 17:
        return "Please enter the correct instructor code."
    return None

def instructor_code_2_error_message(player, value):
    if value != 6:
        return "Please enter the correct instructor code."
    return None

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

class Introduction(Page):
    pass

class InstructionsRound(Page):
    form_model = 'player'
    form_fields = ['instructor_code_2']

page_sequence = [
    # FigureDemo, 
    ConsentRadboud, 
    Introduction, 
    InstructionsRound
]
