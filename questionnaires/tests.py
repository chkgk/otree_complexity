from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        yield Questionnaire, {
            'gender': random.choice(['male', 'female', 'other', 'prefer_not_to_say']), 
            'birth_year': random.randint(1950, 2005), 
            'education_level': random.choice(['high_school', 'bachelor', 'master', 'phd', 'other']),
            'risk_general': random.randint(1, 7),
            'instructions_understood': random.randint(1, 5),
            'specific_strategy': True,
            'strategy_text': 'not much', 
            'comments': ''
        }
        yield FinalScreen, {
            'payment_code': random.randint(1000, 9999),
        }