from os import environ

SESSION_CONFIGS = [
    dict(
        name="intro",
        display_name="Introduction",
        app_sequence=["intro"],
        num_demo_participants=1,
    ),
    dict(
        name="training",
        display_name="Training Round",
        app_sequence=["training"],
        num_demo_participants=1,
        players_per_group=1,
        training_cost_per_second=2,
        training_price_per_unit=10,
        training_initial_stock=2,
        training_initial_cash=30,
        training_round_seconds=600,
        training_show_chain=False
    ),
    dict(
        name="ringsupplychain_3_pilot",
        display_name="RSC, 3 Players, 2 rounds, cost 1, inventory sym 2, cash sym 30, time 30 always, no chain",
        app_sequence=["ringsupplychain"],
        num_demo_participants=3, 
        players_per_group=3,
        cost_per_second=1,
        price_per_unit=10,
        initial_stock=[2, 2, 2],
        initial_cash=[30, 30, 30], 
        round_seconds=[300, 300],
        show_chain=False
    ),
    dict(
        name="ringsupplychain_5_pilot",
        display_name="RSC PILOT, 5 Players, 8 rounds, cost 1, inventory sym 2, cash sym 30, time 30 always, no chain",
        app_sequence=["ringsupplychain"],
        num_demo_participants=3, 
        players_per_group=3,
        cost_per_second=1,
        price_per_unit=10,
        initial_stock=[2, 2, 2, 2, 2],
        initial_cash=[30, 30, 30, 30, 30], 
        round_seconds=[300, 300, 300, 300, 300, 300, 300, 300],
        show_chain=False
    ),
    dict(
        name="ringsupplychain_3_sym",
        display_name="RSC, 3 Players, 2 rounds, cost 1, inventory (2, 2, 2), cash (30, 30, 30), time (300, 300), no chain",
        app_sequence=["ringsupplychain"],
        num_demo_participants=3, 
        players_per_group=3,
        cost_per_second=2,
        price_per_unit=10,
        initial_stock=[2, 2, 2],
        initial_cash=[30, 30, 30], 
        round_seconds=[300, 300],
        show_chain=False
    ),
    dict(
        name="ringsupplychain_3_sym_chain",
        display_name="RSC, 3 Players, 2 rounds, cost 1, inventory (2, 2, 2), cash (30, 30, 30), time (300, 300), chain visible",
        app_sequence=["ringsupplychain"],
        num_demo_participants=3, 
        players_per_group=3,
        cost_per_second=1,
        price_per_unit=10,
        initial_stock=[2, 2, 2],
        initial_cash=[30, 30, 30], 
        round_seconds=[300, 300],
        show_chain=True
    ),
    dict(
        name="ringsupplychain_5_asym",
        display_name="RSC, 5 Players, 2 rounds, cost 1, inventory (0, 5, 0, 5, 0), cash (30, 30, 30, 30 , 30), time (300, 300), no chain",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5,
        players_per_group=5,
        cost_per_second=2,
        price_per_unit=10,
        initial_stock=[0, 5, 0, 5, 0],
        initial_cash=[30, 30, 30, 30, 30], 
        round_seconds=[300, 300],
        show_chain=False
    ),
    dict(
        name="ringsupplychain_5_asym_chain",
        display_name="RSC, 5 Players, 2 rounds, cost 1, inventory (0, 5, 0, 5, 0), cash (30, 30, 30, 30 , 30), time (300, 300), chain visible",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5,
        players_per_group=5,
        cost_per_second=1,
        price_per_unit=10,
        initial_stock=[0, 5, 0, 5, 0],
        initial_cash=[30, 30, 30, 30, 30], 
        round_seconds=[300, 300],
        show_chain=True
    ),
    dict(
        name="ringsupplychain_10_asym",
        display_name="RSC, 10 Players, 2 rounds, cost 2, inventory sym 2, cash sym 30, time 300, chain visible",
        app_sequence=["ringsupplychain"],
        num_demo_participants=20,
        players_per_group=10,
        cost_per_second=1,
        price_per_unit=10,
        initial_stock=[2 for _ in range(10)],
        initial_cash=[30 for _ in range(10)],
        round_seconds=[300, 300],
        show_chain=True
    ),
    dict(
        name="questionnaire",
        display_name="Final Questionnaire",
        app_sequence=["questionnaires"],
        num_demo_participants=1,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.02, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7220483092201'
