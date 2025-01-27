def live_game_init():
    red_towers = ['RED TOP_LANE OUTER_TURRET','RED MID_LANE OUTER_TURRET','RED BOT_LANE OUTER_TURRET',
                    'RED TOP_LANE INNER_TURRET' , 'RED MID_LANE INNER_TURRET', 'RED BOT_LANE INNER_TURRET',
                    'RED TOP_LANE BASE_TURRET', 'RED MID_LANE BASE_TURRET', 'RED BOT_LANE BASE_TURRET']

    blue_towers =  ['BLUE TOP_LANE OUTER_TURRET','BLUE MID_LANE OUTER_TURRET','BLUE BOT_LANE OUTER_TURRET',
                    'BLUE TOP_LANE INNER_TURRET' , 'BLUE MID_LANE INNER_TURRET', 'BLUE BOT_LANE INNER_TURRET',
                    'BLUE TOP_LANE BASE_TURRET', 'BLUE MID_LANE BASE_TURRET', 'BLUE BOT_LANE BASE_TURRET']


    red_first_tower = False
    blue_first_tower = False

    red_top_inhib = 0
    red_mid_inhib = 0
    red_bot_inhib = 0


    blue_top_inhib = 0
    blue_mid_inhib = 0
    blue_bot_inhib = 0


    red_fire_dragons = 0
    red_water_dragons = 0
    red_earth_dragons = 0
    red_air_dragons = 0
    red_hextech_dragons = 0
    red_chemtech_dragons = 0
    red_elder_dragons = 0


    blue_fire_dragons = 0
    blue_water_dragons = 0
    blue_earth_dragons = 0
    blue_air_dragons = 0
    blue_hextech_dragons = 0
    blue_chemtech_dragons = 0
    blue_elder_dragons = 0


    red_barons = 0

    blue_barons = 0


    red_rift = False
    blue_rift = False

    red_hordes = 0

    blue_hordes = 0


    red_top_kda = 0.
    red_jungle_kda = 0.
    red_mid_kda = 0.
    red_adc_kda = 0.
    red_sup_kda = 0.
    red_first_blood = False

    blue_top_kda = 0.
    blue_jungle_kda = 0.
    blue_mid_kda = 0.
    blue_adc_kda = 0.
    blue_sup_kda = 0.
    blue_first_blood = False

    return red_towers, blue_towers ,red_top_inhib , red_mid_inhib ,red_bot_inhib, blue_top_inhib, blue_mid_inhib ,blue_bot_inhib,red_fire_dragons,red_water_dragons,red_earth_dragons,red_air_dragons,red_hextech_dragons,red_chemtech_dragons,red_elder_dragons,blue_fire_dragons,blue_water_dragons,blue_earth_dragons,blue_air_dragons,blue_hextech_dragons,blue_chemtech_dragons,blue_elder_dragons,red_barons,blue_barons,red_rift,blue_rift,red_hordes,blue_hordes, red_first_tower, red_first_blood, blue_first_tower, blue_first_blood 

def map_new_turret_name(turret):
    # Team Mapping
    team_mapping = {
        "T100": "BLUE",
        "T200": "RED"
    }

    # Lane Mapping
    lane_mapping = {
        "L0": "BOT_LANE",
        "L1": "MID_LANE",
        "L2": "TOP_LANE"
    }

    # Position Mapping
    position_mapping = {
        "P1": "BASE_TURRET",
        "P2": "INNER_TURRET",
        "P3": "OUTER_TURRET",
    }

    # Splitting the turret string
    parts = turret.split("_")

    if len(parts) < 4:
        return "UNKNOWN TURRET"

    team = team_mapping.get(parts[1], "UNKNOWN TEAM")
    lane = lane_mapping.get(parts[2], "UNKNOWN LANE")
    position = position_mapping.get(parts[3], "UNKNOWN POSITION")

    return f"{lane} {position}"


def mapping_turrets(turret):
    # Check for top turrets
    if turret == 'Turret_T2_L_03_A':
        return 'TOP_LANE OUTER_TURRET'
    elif turret == 'Turret_T2_L_02_A':
        return 'TOP_LANE INNER_TURRET'
    elif turret == 'Turret_T2_L_01_A':
        return 'TOP_LANE BASE_TURRET'
    
    # Check for mid turrets
    elif turret == 'Turret_T2_C_05_A':
        return 'MID_LANE OUTER_TURRET'
    elif turret == 'Turret_T2_C_04_A':
        return 'MID_LANE INNER_TURRET'
    elif turret == 'Turret_T2_C_03_A':
        return 'MID_LANE BASE_TURRET'
    elif turret == 'Turret_T2_C_02_A' or turret == 'Turret_T2_C_01_A':
        return 'MID_LANE NEXUS_TURRET'
    
    # Check for bot turrets
    elif turret == 'Turret_T2_R_03_A':
        return 'BOT_LANE OUTER_TURRET'
    elif turret == 'Turret_T2_R_02_A':
        return 'BOT_LANE INNER_TURRET'
    elif turret == 'Turret_T2_R_01_A':
        return 'BOT_LANE BASE_TURRET'
    
    
def mapping_inhibs(inhib):
    if inhib == 'Barracks_T2_L1':
        return 'TOP'
    elif inhib == 'Barracks_T2_C1':
        return 'MID'
    elif inhib == 'Barracks_T2_R1':
        return 'BOT'
    
