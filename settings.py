from os import environ

GAME_CONFIG = dict(
    request_timeout_seconds=0,
    info_highlight_timeout_seconds=1,
    cost_per_second=5,
    price_per_unit=100,
    round_seconds=180,
    num_rounds=4,
    payment_link="https://example.com/",
)

TRAINING_CONFIG = dict(
    training_cost_per_second=5,
    training_price_per_unit=100,
    training_initial_stock=2,
    training_initial_cash=300,
    training_round_seconds=90,
    training_transfer_probability=0.5,
    training_start_delay_seconds=15,
    training_leave_seconds=15,
    training_request_timeout_seconds=0,
    training_info_highlight_timeout_seconds=1,
)

INV_LO_A = dict(
    players_per_group=5,
    initial_stock="1, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300", 
    show_chain=False,
)

INV_HI_A = dict(
    players_per_group=5,
    initial_stock="10, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300", 
    show_chain=False,
)

INV_HI_S = dict(
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300", 
    show_chain=False,
)

INV_HI_S_INFO = dict(
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300", 
    show_chain=True,
)

SESSION_CONFIGS = [
    dict(
        name="intro_invisible",
        display_name="Introduction - Ring not Visible",
        app_sequence=["intro"],
        num_demo_participants=1,
        players_per_group=5,
        initial_cash="30, 30, 30, 30, 30",
        initial_stock="2, 2, 2, 2, 2",
        show_chain=False,
        **GAME_CONFIG,
        **TRAINING_CONFIG
    ),
    dict(
        name="intro_visible",
        display_name="Introduction - Ring Visible",
        app_sequence=["intro"],
        num_demo_participants=1,
        players_per_group=5,
        initial_cash="300, 300, 300, 300, 300",
        initial_stock="2, 2, 2, 2, 2",
        show_chain=True,
        **GAME_CONFIG,
        **TRAINING_CONFIG
    ),
    dict(
        name="training",
        display_name="Training Round",
        app_sequence=["training"],
        num_demo_participants=1,
        players_per_group=1,
        **TRAINING_CONFIG
    ),
    dict(
        name="inv_lo_a",
        display_name="INV_LO_A (1,0,0,0,0 units; 300ecu; no info)",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5, 
        **INV_LO_A,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="inv_hi_a",
        display_name="INV_HI_A (10,0,0,0,0 units; 300ecu; no info)",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5, 
        **INV_HI_A,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=True,
    ),
    dict(
        name="inv_hi_s",
        display_name="INV_HI_S (sym 2 units; 300ecu; no info)",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5, 
        **INV_HI_S,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="inv_hi_s_info",
        display_name="INV_HI_S_INFO (sym 2 units; 300ecu; with info)",
        app_sequence=["ringsupplychain"],
        num_demo_participants=5, 
        **INV_HI_S_INFO,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="questionnaire",
        display_name="Final Questionnaire + Payments",
        app_sequence=["questionnaires"],
        num_demo_participants=1,
    ),
    dict(
        name="complete_demo",
        display_name="Experiment Demo: INV_HI_S",
        app_sequence=["intro", "training", "ringsupplychain", "questionnaires"],
        num_demo_participants=5,
        **INV_HI_S,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=True,
    ),
]

# Rooms
ROOMS = [
    dict(
        name='room1',
        display_name='Room 1'
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['game_rounds']
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

BROWSER_COMMAND = "/Users/christian/chrome.sh"

# URL from heroku labs runtime-dyno-metadata
BASE_URL = environ.get('HEROKU_APP_DEFAULT_DOMAIN_NAME', 'localhost:8000')