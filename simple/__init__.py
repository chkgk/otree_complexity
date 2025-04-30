from otree.api import *
import time


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'simple'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 1

    DECISION_TIMEOUT_SECONDS = 600 


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    stock = models.IntegerField(initial=1)
    
class Transfers(ExtraModel):
    created = models.IntegerField()
    group = models.Link(Group)
    from_player = models.Link(Player)
    to_player = models.Link(Player)
    units = models.IntegerField()

# FUNCTIONS
def decision_vars_for_js_and_template(player):
    return {
        'own_id_in_group': player.id_in_group,
    } 


# PAGES
class CommonStart(WaitPage):
    pass

class Decision(Page):
    timeout_seconds = C.DECISION_TIMEOUT_SECONDS

    @staticmethod
    def live_method(player, data):
        print('live_method', data)
        
        take_from = data['from']
        give_to = data['to']
        units = data['units']
        
        group = player.group
        take_from_player = group.get_player_by_id(take_from)
        give_to_player = group.get_player_by_id(give_to)
        
        take_from_player.stock -= units
        give_to_player.stock += units
        
        Transfers.create(
            created=int(time.time()),
            group=group,
            from_player=take_from_player,
            to_player=give_to_player,
            units=units
        )
        
        stock_status = [p.stock for p in group.get_players()]
        return {0: {'type': 'stock_status', 'data': stock_status}}
    
    def js_vars(player):
        return decision_vars_for_js_and_template(player)
    
    def vars_for_template(player):
        return decision_vars_for_js_and_template(player)
    

class Results(Page):
    pass


page_sequence = [CommonStart, Decision, Results]


# EXPORTS
def custom_export(players):
    yield ['created', 'group', 'from_id', 'to_id', 'units']
    for transfer in Transfers.filter():
        yield [transfer.created, 
               transfer.group.id_in_subsession,
               transfer.from_player.id_in_group,
               transfer.to_player.id_in_group,
               transfer.units]