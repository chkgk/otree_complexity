from otree.api import Currency as c, currency_range, expect, Bot
from . import *

class PlayerBot(Bot):
    def play_round(self):
        yield Welcome
        yield ConsentRadboud, {
            'confirm_read_understood': True,
            'voluntary_participation': True,
            'data_access_by_authorities': True,
            'data_anonymity': True,
            'data_publication': True,
            'future_research_use': True,
            'agree_to_participate': True,
            'confirm_info_reviewed_again': True
        }
        yield GameInstructions