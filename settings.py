from os import environ

GAME_CONFIG = dict(
    request_timeout_seconds=0,
    info_highlight_timeout_seconds=1,
    countdown_seconds=5,
    round_seconds=180,
    payment_link="https://fmru.az1.qualtrics.com/jfe/form/SV_4ZXrz1uGVKevsrA",
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
    treatment="INV_LO_A",
    players_per_group=5,
    initial_stock="1, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False",
)

INV_HI_A = dict(
    treatment="INV_HI_A",
    players_per_group=5,
    initial_stock="10, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False",
)

INV_HI_S = dict(
    treatment="INV_HI_S",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

INV_HI_S_INFO = dict(
    treatment="INV_HI_S_INFO",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="True"
)

A_10_NT = dict(
    treatment="A_10_NT",
    players_per_group=5,
    initial_stock="10, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

A_1_NT = dict(
    treatment="A_1_NT",
    players_per_group=5,
    initial_stock="1, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

A_3_NT = dict(
    treatment="A_3_NT",
    players_per_group=5,
    initial_stock="3, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

A_5_NT = dict(
    treatment="A_1_NT",
    players_per_group=5,
    initial_stock="5, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

S_10_NT = dict(
    treatment="S_10_NT",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="False"
)

S_10_T = dict(
    treatment="S_10_T",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300",
    cost_per_second="5",
    price_per_unit="100",
    show_chain="True"
)

# A_10_NT -> S_10_NT -> A_1_NT
SESSION_1 = dict(
    treatment="A_10_NT; S_10_NT; A_1_NT",
    players_per_group=5,
    initial_stock="10, 0, 0, 0, 0; 2, 2, 2, 2, 2; 1, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="False; False; False",
    num_rounds=3
)

# A_5_NT -> A_1_NT -> A_10_NT
SESSION_2 = dict(
    treatment="A_5_NT; A_1_NT; A_10_NT",
    players_per_group=5,
    initial_stock="5, 0, 0, 0, 0; 1, 0, 0, 0, 0; 10, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="False; False; False",
    num_rounds=3
)
# A_1_NT -> A_5_NT -> A_3_NT
SESSION_3 = dict(
    treatment="A_1_NT; A_5_NT; A_3_NT",
    players_per_group=5,
    initial_stock="1, 0, 0, 0, 0; 5, 0, 0, 0, 0; 3, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="False; False; False",
    num_rounds=3
)

# A_3_NT - A_10_NT - A_5_NT
SESSION_4 = dict(
    treatment="A_3_NT; A_10_NT; A_5_NT",
    players_per_group=5,
    initial_stock="3, 0, 0, 0, 0; 10, 0, 0, 0, 0; 5, 0, 0, 0, 0",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="False; False; False",
    num_rounds=3
)

# S_10_NT - A_3_NT - S_10_T
SESSION_5 = dict(
    treatment="S_10_NT; A_3_NT; S_10_T",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2; 3, 0, 0, 0, 0; 2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="False; False; True",
    num_rounds=3
)

# S_10_T - A_3_NT - S_10_NT
SESSION_6 = dict(
    treatment="S_10_T; A_3_NT; S_10_NT",
    players_per_group=5,
    initial_stock="2, 2, 2, 2, 2; 3, 0, 0, 0, 0; 2, 2, 2, 2, 2",
    initial_cash="300, 300, 300, 300, 300; 300, 300, 300, 300, 300; 300, 300, 300, 300, 300",
    cost_per_second="5; 5; 5",
    price_per_unit="100; 100; 100",
    show_chain="True; False; False",
    num_rounds=3
)
    


SESSION_CONFIGS = [
    # dict(
    #     name="intro",
    #     display_name="Introduction",
    #     app_sequence=["intro"],
    #     num_demo_participants=1,
    #     players_per_group=5,
    #     initial_cash="30, 30, 30, 30, 30",
    #     initial_stock="2, 2, 2, 2, 2",
    #     show_chain=False,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG
    # ),
    # dict(
    #     name="training",
    #     display_name="Training Round",
    #     app_sequence=["training"],
    #     num_demo_participants=1,
    #     players_per_group=1,
    #     **TRAINING_CONFIG
    # ),
    # dict(
    #     name="inv_lo_a",
    #     display_name="INV_LO_A (1,0,0,0,0 units; 300ecu; no info)",
    #     app_sequence=["ringsupplychain"],
    #     num_demo_participants=5, 
    #     **INV_LO_A,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="inv_hi_a",
    #     display_name="INV_HI_A (10,0,0,0,0 units; 300ecu; no info)",
    #     app_sequence=["ringsupplychain"],
    #     num_demo_participants=5, 
    #     **INV_HI_A,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="inv_hi_s",
    #     display_name="INV_HI_S (sym 2 units; 300ecu; no info)",
    #     app_sequence=["ringsupplychain"],
    #     num_demo_participants=5, 
    #     **INV_HI_S,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="inv_hi_s_info",
    #     display_name="INV_HI_S_INFO (sym 2 units; 300ecu; with info)",
    #     app_sequence=["ringsupplychain"],
    #     num_demo_participants=5, 
    #     **INV_HI_S_INFO,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="session_1_demo",
    #     display_name="Session 1 DECISION: INV_LO_A -> INV_HI_A -> INV_HI_S -> INV_HI_S_INFO",
    #     app_sequence=["ringsupplychain_4"],
    #     num_demo_participants=3,
    #     treatment="INV_LO_A; INV_HI_A; INV_HI_S; INV_HI_S_INFO",
    #     players_per_group=3,
    #     initial_stock="2, 2, 2; 1, 0, 0; 10, 0, 0; 2, 2, 2",
    #     initial_cash="300, 300, 300; 300, 300, 300; 300, 300, 300; 300, 300, 300",
    #     cost_per_second="5; 5; 5; 5",
    #     price_per_unit="100; 100; 100; 100",
    #     show_chain="False; False; False; True",
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="session_2",
    #     display_name="Session 2: INV_HI_S_INFO -> INV_HI_S -> INV_HI_A -> INV_LO_A",
    #     app_sequence=["ringsupplychain_4"],
    #     num_demo_participants=5,
    #     **SESSION_2,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    # dict(
    #     name="questionnaire",
    #     display_name="Final Questionnaire + Payments",
    #     app_sequence=["questionnaires"],
    #     num_demo_participants=1,
    #     **GAME_CONFIG
    # ),
    # dict(
    #     name="complete_demo_single",
    #     display_name="Experiment Demo: INV_HI_S",
    #     app_sequence=["intro", "training", "ringsupplychain", "questionnaires"],
    #     num_demo_participants=5,
    #     **INV_HI_S,
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=False,
    # ),
    dict(
        name="session_1",
        display_name="Session 1 (A_10_NT -> S_10_NT -> A_1_NT)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_1,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="session_2",
        display_name="Session 2 (A_5_NT -> A_1_NT -> A_10_NT)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_2,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="session_3",
        display_name="Session 3 (A_1_NT -> A_5_NT -> A_3_NT)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_3,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="session_4",
        display_name="Session 4 (A_3_NT -> A_10_NT -> A_5_NT)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_4,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="session_5",
        display_name="Session 5 (S_10_NT -> A_3_NT -> S_10_T)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_5,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    dict(
        name="session_6",
        display_name="Session 6 (S_10_T -> A_3_NT -> S_10_NT)",
        app_sequence=["intro", "training", "ringsupplychain_4", "questionnaires"],
        num_demo_participants=5,
        **SESSION_6,
        **GAME_CONFIG,
        **TRAINING_CONFIG,
        auto_play=False,
    ),
    # dict(
    #     name="inv_hi_s_info_auto",
    #     display_name="INV_HI_S_INFO (3 players, sym 2 units; 300ecu; with info, auto play)",
    #     app_sequence=["ringsupplychain"],
    #     num_demo_participants=3,
    #     treatment="INV_HI_S_INFO",
    #     players_per_group=3,
    #     initial_stock="2, 2, 2",
    #     initial_cash="300, 300, 300",
    #     cost_per_second="5",
    #     price_per_unit="100",
    #     show_chain="True",
    #     **GAME_CONFIG,
    #     **TRAINING_CONFIG,
    #     auto_play=True,
    # ),
    # dict(
    #     name="admin_advance",
    #     display_name="Admin Advance",
    #     app_sequence=["admin_advance"],
    #     num_demo_participants=3,
    # )
]

# Rooms
ROOMS = [
    dict(
        name='room1',
        display_name='Room 1',
        participant_label_file='_rooms/room1.txt',
    ),
    dict(
        name='room2',
        display_name='Room 2',
        participant_label_file='_rooms/room1.txt',
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.0008, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['game_rounds', 'pages_completed']
SESSION_FIELDS = ['advance_pages']

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