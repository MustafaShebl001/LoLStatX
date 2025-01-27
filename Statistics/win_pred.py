import requests
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path

helper_functions_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Helper Functions")
sys.path.append(helper_functions_path)

from objectives import *
from live_game_helpers import *


def predict_match():
    try:
        live_game_players = requests.get('https://127.0.0.1:2999/liveclientdata/playerlist',verify=False).json()
        live_game_data =   requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata',verify=False).json()
        live_game_events = requests.get('https://127.0.0.1:2999/liveclientdata/eventdata',verify=False).json()  #67
    except:
        return 'You are not in a game or the game is not running', 'N/A'
    
    # Load the model 
    model = tf.keras.models.load_model(current_dir / 'Win_Prob ANN_model3.keras') # tf.keras.models.load_model(current_dir / 'Win_Prob ANN_model.keras')
    game_df = pd.DataFrame()
    game_dic = {}

    # Add Time Stamp
    game_dic['TIME STAMP'] = round(live_game_events['Events'][-1]['EventTime']/60,2)
    
    # Get user team
    user_team = 'BLUE' if live_game_players[0]['team'] == 'ORDER' else 'RED'

    team_dic = {}
    count1 = 9
    count2 = 9

    count3 = 4
    count4 = 4

    count5 = 9
    count6 = 9
    teams_count = 0
    Blue_team = []
    Red_team = []


    # Loop over events to collect game data
    for i in range(len(live_game_players)):
        items_list = [0]*6
        # championName = live_game_players[i]['championName']
        championLevel = live_game_players[i]['level']
        position = live_game_players[i]['position']
        kills = live_game_players[i]['scores']['kills']
        riot_id = live_game_players[i]['riotIdGameName']    # to get which player/team did the event
        assists = live_game_players[i]['scores']['assists']
        deaths = live_game_players[i]['scores']['deaths']
        team = 'BLUE' if live_game_players[i]['team'] == 'ORDER' else 'RED'
        cs = live_game_players[i]['scores']['creepScore']
        if team == 'BLUE':
            Blue_team.append(riot_id)
        else:
            Red_team.append(riot_id)
        kda = float(assists + kills) if deaths == 0 else round((assists+kills)/deaths,2)
        cs_per_min = 0 if game_dic['TIME STAMP'] == 0 else round(cs / game_dic['TIME STAMP'],1)
        # for j in range(len(live_game_players[i]['items'])):  # Loop over items neglecting slot 6 "ward slot"
        #     if live_game_players[i]['items'][j]['slot'] == 6:
        #         pass
        #     else:
        #         items_list[live_game_players[i]['items'][j]['slot']] += live_game_players[i]['items'][j]['itemID']

        if live_game_players[i]['position'] == 'TOP':
            # team_dic.update({f'{team} TOP' : championName})
            team_dic.update({f'{team} TOP KDA' : kda})
            team_dic.update({f'{team} TOP LEVEL' :championLevel})
            # team_dic.update({f'{team} TOP Items' : items_list})
            team_dic.update({f'{team} TOP CS/MIN' : cs_per_min})
        elif live_game_players[i]['position'] == 'JUNGLE' or live_game_players[i]['position'] == '':
            # team_dic.update({f'{team} JUNGLE' : championName})
            team_dic.update({f'{team} JUNGLE KDA' : kda})
            team_dic.update({f'{team} JUNGLE LEVEL' : championLevel})
            # team_dic.update({f'{team} JUNGLE Items' : items_list}) 
            team_dic.update({f'{team} JUNGLE CS/MIN' : cs_per_min})

        elif live_game_players[i]['position'] == 'MIDDLE':
            # team_dic.update({f'{team} MID' : championName})
            team_dic.update({f'{team} MIDDLE KDA' : kda})
            team_dic.update({f'{team} MID LEVEL' : championLevel})
            # team_dic.update({f'{team} MIDDLE Items' : items_list}) 
            team_dic.update({f'{team} MID CS/MIN' : cs_per_min})

        elif live_game_players[i]['position'] == 'BOTTOM':
            # team_dic.update({f'{team} ADC' : championName})
            team_dic.update({f'{team} BOTTOM KDA' : kda})
            team_dic.update({f'{team} ADC LEVEL' : championLevel})
            # team_dic.update({f'{team} ADC Items' : items_list})  
            team_dic.update({f'{team} ADC CS/MIN' : cs_per_min})

        elif live_game_players[i]['position'] == 'UTILITY':
            # team_dic.update({f'{team} SUPPORT' :championName})
            team_dic.update({f'{team} UTILITY KDA' : kda})
            team_dic.update({f'{team} SUPPORT LEVEL' : championLevel})
            # team_dic.update({f'{team} SUPPORT Items' : items_list}) 
        
        # Neglicting ARAM games
        elif live_game_players[i]['position'] == 'Invalid':
            pass

        # else:
        #     print('----------------- ERROR -----------------')


        

        count2 += 1
        count4 += 1
        count6 += 1





        if i%count1 == 0 and i!= 0:
            count1 = count2
            game_df = pd.concat([game_df,pd.DataFrame([team_dic])],ignore_index=True)


    adjusted_items_games = game_df

    # Intialization of the objectives
    red_turrets, blue_turrets ,red_top_inhib , red_mid_inhib ,red_bot_inhib, blue_top_inhib, blue_mid_inhib ,blue_bot_inhib,red_fire_dragons,red_water_dragons,red_earth_dragons,red_air_dragons,red_hextech_dragons,red_chemtech_dragons,red_elder_dragons,blue_fire_dragons,blue_water_dragons,blue_earth_dragons,blue_air_dragons,blue_hextech_dragons,blue_chemtech_dragons,blue_elder_dragons,red_barons,blue_barons,red_rift,blue_rift,red_hordes,blue_hordes, red_first_tower, red_first_blood, blue_first_tower, blue_first_blood = live_game_init()

    # Mapping minions to both teams
    Blue_team.append("Minion_T100")
    Red_team.append('Minion_T200')

    event_dic = {}

    for j in range(len(live_game_events['Events'])):
        event = live_game_events['Events'][j]
        event_name = event['EventName']
        event_time = event['EventTime']
        
        try:
            if event_name == 'FirstBlood':
                bplayer = any(s in event['Recipient'] for s in Blue_team)
                rplayer = any(s in event['Recipient'] for s in Red_team)
                if bplayer:
                    blue_first_blood = True
                elif rplayer:
                    red_first_blood = True
                # else:
                #     print("ERROR IN FIRSTBLOOD")
            else:
                bplayer = any(s in event['KillerName'] for s in Blue_team)
                rplayer = any(s in event['KillerName'] for s in Red_team)

        except:
            # print(event_name,event_time)
            # print('Event with no KillerName')
            continue

        if bplayer:
            flag = 1
        elif rplayer:
            flag = 2
        else:
            flag = 3
            continue


        # First two events are standard: GameStart and MinionSpawning, so we nyeglect i == 0 and i == 1
        if j == 0 or j == 1:
            pass
        else:
            if flag == 1:
                if event_name == 'BaronKill':
                    blue_barons += 1
                elif event_name == 'DragonKill':
                    dragon_type = event['DragonType']
                    blue_air_dragons, blue_fire_dragons, blue_earth_dragons, blue_water_dragons, blue_hextech_dragons, blue_chemtech_dragons, blue_elder_dragons = check_dragon_type(blue_air_dragons, blue_fire_dragons, blue_earth_dragons, blue_water_dragons, blue_hextech_dragons, blue_chemtech_dragons,blue_elder_dragons,dragon_type)
                elif event_name == 'TurretKilled':
                    # print(event['TurretKilled'])
                    turret_name = "RED" + " " + map_new_turret_name(event['TurretKilled'])
                    # print(turret_name)
                    try:
                        red_turrets.remove(turret_name)
                    except:
                        print(turret_name)
                elif event_name == 'FirstBrick':
                    blue_first_tower = True
                elif event_name == 'InhibKilled':
                    inhib_lane = mapping_inhibs(event['InhibKilled'])
                        # Counted for red team that destroyed the inhib
                    if inhib_lane == 'TOP':
                        red_top_inhib += 1 
                    elif inhib_lane == 'MID':
                        red_mid_inhib += 1
                    elif inhib_lane == 'BOT':
                        red_bot_inhib += 1
                elif event_name == 'HordeKill':
                    blue_hordes += 1
                elif event_name == 'HeraldKill':
                    blue_rift = True
                # elif event_name == 'FirstBlood':
                #     blue_first_blood = True
            elif flag == 2:
                if event_name == 'BaronKill':
                    red_barons += 1
                elif event_name == 'DragonKill':
                    dragon_type = event['DragonType']
                    red_air_dragons, red_fire_dragons, red_earth_dragons, red_water_dragons, red_hextech_dragons, red_chemtech_dragons, red_elder_dragons = check_dragon_type(red_air_dragons, red_fire_dragons, red_earth_dragons, red_water_dragons, red_hextech_dragons, red_chemtech_dragons, red_elder_dragons,dragon_type)
                elif event_name == 'TurretKilled':
                    turret_name = 'BLUE' + ' ' + map_new_turret_name(event['TurretKilled'])
                    try:
                        blue_turrets.remove(turret_name)
                    except:
                        print(turret_name)
                elif event_name == 'FirstBrick':
                    red_first_tower = True
                elif event_name == 'InhibKilled':
                    inhib_lane = mapping_inhibs(event['InhibKilled'])
                    # Counted for blue team that destroyed the inhib
                    if inhib_lane == 'TOP':
                        blue_top_inhib += 1 
                    elif inhib_lane == 'MID':
                        blue_mid_inhib += 1
                    elif inhib_lane == 'BOT':
                        blue_bot_inhib += 1
                elif event_name == 'HordeKill':
                    red_hordes += 1
                elif event_name == 'HeraldKill':
                    red_rift = True
                # elif event_name == 'FirstBlood':
                #     red_first_blood = True
            # else:
            #     print("------ Error Event -------")
            
        
    event_dic.update({
        f'RED BARON': red_barons,

        'RED AIR DRAGON': red_air_dragons,
        'RED FIRE DRAGON': red_air_dragons,
        'RED EARTH DRAGON': red_air_dragons,
        'RED WATER DRAGON': red_air_dragons,
        'RED HEXTECH DRAGON': red_air_dragons,
        'RED CHEMTECH DRAGON': red_air_dragons,
        'RED ELDER DRAGON': red_air_dragons,

        # f'RED RiftHerald': red_rift,
        f'RED GRUBS': red_hordes,

        'RED Turrets': red_turrets,
        # 'RED FIRST TOWER': red_first_tower,
        'RED TOP INHIB': red_top_inhib,
        'RED MID INHIB' : red_mid_inhib,
        'RED_BOT_INHIB' : red_bot_inhib,

        
        f'BLUE BARON': blue_barons,

        'BLUE AIR DRAGON': blue_air_dragons,
        'BLUE FIRE DRAGON': blue_air_dragons,
        'BLUE EARTH DRAGON': blue_air_dragons,
        'BLUE WATER DRAGON': blue_air_dragons,
        'BLUE HEXTECH DRAGON': blue_air_dragons,
        'BLUE CHEMTECH DRAGON': blue_air_dragons,
        'BLUE ELDER DRAGON': blue_air_dragons,

        # f'BLUE RiftHerald': blue_rift,
        f'BLUE GRUBS': blue_hordes,

        f'BLUE Turrets': blue_turrets,
        # 'BLUE FIRST TOWER': blue_first_tower,
        'BLUE TOP INHIB': blue_top_inhib,
        'BLUE MID INHIB' : blue_mid_inhib,
        'BLUE_BOT_INHIB' : blue_bot_inhib

        # 'BLUE FIRST BLOOD': blue_first_blood,
        # 'RED FIRST BLOOD': red_first_blood

    })

    # Convert dictionary to dataframe
    event_df = pd.DataFrame([event_dic])

    # Add both teams Turrents

    # RED Team
    event_df['RED TOP_LANE OUTER_TURRET'] = 0
    event_df['RED TOP_LANE INNER_TURRET'] = 0
    event_df['RED TOP_LANE BASE_TURRET'] = 0

    event_df['RED MID_LANE OUTER_TURRET'] = 0
    event_df['RED MID_LANE INNER_TURRET'] = 0
    event_df['RED MID_LANE BASE_TURRET'] = 0

    event_df['RED BOT_LANE OUTER_TURRET'] = 0
    event_df['RED BOT_LANE INNER_TURRET'] = 0
    event_df['RED BOT_LANE BASE_TURRET'] = 0


    # BLUE Team
    event_df['BLUE TOP_LANE OUTER_TURRET'] = 0
    event_df['BLUE TOP_LANE INNER_TURRET'] = 0
    event_df['BLUE TOP_LANE BASE_TURRET'] = 0

    event_df['BLUE MID_LANE OUTER_TURRET'] = 0
    event_df['BLUE MID_LANE INNER_TURRET'] = 0
    event_df['BLUE MID_LANE BASE_TURRET'] = 0

    event_df['BLUE BOT_LANE OUTER_TURRET'] = 0
    event_df['BLUE BOT_LANE INNER_TURRET'] = 0
    event_df['BLUE BOT_LANE BASE_TURRET'] = 0

    # Count available turrets
    red_turrets = ['RED TOP_LANE OUTER_TURRET','RED MID_LANE OUTER_TURRET','RED BOT_LANE OUTER_TURRET',
                            'RED TOP_LANE INNER_TURRET' , 'RED MID_LANE INNER_TURRET', 'RED BOT_LANE INNER_TURRET',
                            'RED TOP_LANE BASE_TURRET', 'RED MID_LANE BASE_TURRET', 'RED BOT_LANE BASE_TURRET']


    # Iterate through each row and with correspoding index
    for index, row in event_df.iterrows():
        # Set 1 for columns in the list, 0 otherwise
        for col in red_turrets:
            event_df.at[index, col] += 1 if col in row['RED Turrets'] else 0

    blue_turrets = ['BLUE TOP_LANE OUTER_TURRET','BLUE MID_LANE OUTER_TURRET','BLUE BOT_LANE OUTER_TURRET',
                            'BLUE TOP_LANE INNER_TURRET' , 'BLUE MID_LANE INNER_TURRET', 'BLUE BOT_LANE INNER_TURRET',
                            'BLUE TOP_LANE BASE_TURRET', 'BLUE MID_LANE BASE_TURRET', 'BLUE BOT_LANE BASE_TURRET']

    # Iterate through each row and with correspoding index
    for index, row in event_df.iterrows():
        # Set 1 for columns in the list, 0 otherwise
        for col in blue_turrets:
            event_df.at[index, col] += 1 if col in row['BLUE Turrets'] else 0

    # Concat game data and events data
    live_game = pd.concat([game_df, event_df], axis=1)


    # Drop Turrets list after Unpacking
    live_game.drop(['RED Turrets', 'BLUE Turrets'], axis=1, inplace=True)

    live_game_encoded_features = live_game[[ 'RED FIRE DRAGON',
       'RED AIR DRAGON', 'RED EARTH DRAGON', 'RED WATER DRAGON',
       'RED HEXTECH DRAGON', 'RED CHEMTECH DRAGON', 'RED ELDER DRAGON',
       'BLUE FIRE DRAGON', 'BLUE AIR DRAGON', 'BLUE EARTH DRAGON',
       'BLUE WATER DRAGON', 'BLUE HEXTECH DRAGON', 'BLUE CHEMTECH DRAGON',
       'BLUE ELDER DRAGON', 'RED BARON', 'BLUE BARON',
       'RED GRUBS', 'BLUE GRUBS','RED TOP_LANE OUTER_TURRET', 'RED TOP_LANE INNER_TURRET',
       'RED TOP_LANE BASE_TURRET', 'RED MID_LANE OUTER_TURRET',
       'RED MID_LANE INNER_TURRET', 'RED MID_LANE BASE_TURRET',
       'RED BOT_LANE OUTER_TURRET', 'RED BOT_LANE INNER_TURRET',
       'RED BOT_LANE BASE_TURRET',
       'BLUE TOP_LANE OUTER_TURRET', 'BLUE TOP_LANE INNER_TURRET',
       'BLUE TOP_LANE BASE_TURRET', 'BLUE MID_LANE OUTER_TURRET',
       'BLUE MID_LANE INNER_TURRET', 'BLUE MID_LANE BASE_TURRET',
       'BLUE BOT_LANE OUTER_TURRET', 'BLUE BOT_LANE INNER_TURRET',
       'BLUE BOT_LANE BASE_TURRET','BLUE TOP KDA', 'BLUE JUNGLE KDA',
       'BLUE MIDDLE KDA', 'BLUE BOTTOM KDA', 'BLUE UTILITY KDA', 'RED TOP KDA',
       'RED JUNGLE KDA', 'RED MIDDLE KDA', 'RED BOTTOM KDA', 'RED UTILITY KDA']]
    
    with open(current_dir / 'train_col3.txt', 'r') as filehandle:
        train_col = filehandle.readlines()

    # Strip newline characters from each line
    train_col = [line.strip() for line in train_col]

    test_encoded = live_game_encoded_features.reindex(columns=train_col, fill_value=0)
    print(test_encoded.shape)
    pred = model.predict(test_encoded)

    # Load the text file containing the column names
    

    test_col = list(live_game_encoded_features.columns)
    # print(train_col)
    unique_to_list2 = list(set(test_col) - set(train_col))
    print(unique_to_list2)

    # test_encoded = live_game_encoded_features.reindex(columns=train_col)
    # pred = model.predict(test_encoded)
    pred_value = float(pred[0][0]) if isinstance(pred, (np.ndarray, list)) else float(pred)
    pred_value = pred_value*100
    return f"{pred_value:.1f}", user_team  # Return as a formatted ASCII string


if __name__ == "__main__":
    result = predict_match()
    print(result)