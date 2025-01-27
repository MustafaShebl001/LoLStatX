import numpy as np
import pandas as pd
import time
import requests


def delay_with_interrupt(seconds):      # Delay function, so we don't exceed ratelimit of 100 requests per two minutes
    for i in range(seconds):        # This implementation to interrupt in the sleeping state rather than in data extraction state
        time.sleep(1) 
        print(f"Elapsed time: {i + 1} seconds", end="\r")
    print("\nTime is up!")


def get_match_ids(puuid, region, api_key, count=47, queue_ids=[420, 400, 440]):
    """
    Fetches the first `count` match IDs for specific queue types.
    
    Parameters:
        puuid (str): The player's PUUID.
        region (str): The Riot API region (e.g., 'asia', 'europe', 'americas').
        api_key (str): Riot API key.
        count (int): The total number of matches to fetch (default is 47).
        queue_ids (list): List of queue IDs to consider (default is [420, 400, 440]).
    
    Returns:
        list: A list of match IDs.
    """
    all_match_ids = []  # To store fetched match IDs
    start = 0  # Initial starting point for fetching matches

    for queue_id in queue_ids:
        while len(all_match_ids) < count:
            url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
            params = {
                'queue': queue_id,
                'start': start,
                'count': min(count - len(all_match_ids), 100),  # Riot API limit per request
                'api_key': api_key
            }

            # if len(puuid) != 78:
            #     break

            try:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    match_ids = response.json()
                    if not match_ids:  # If no matches are returned, stop fetching for this queue
                        break
                    all_match_ids.extend(match_ids)
                    start += len(match_ids)
                elif response.status_code == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get('Retry-After', 120))
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    break
            except Exception as e:
                print(f"Error fetching matches for queue ID {queue_id}: {e}")
                break  # Break on error to avoid infinite loops

        if len(all_match_ids) >= count:  # Stop if we've fetched enough matches
            break

    return all_match_ids[:count], response  # Return exactly `count` match IDs



def check_dragon_type(air_dragons, fire_dragons,earth_dragons,water_dragons,hextech_dragons,chemtech_dragons,elder_dragons,dragon_type):
    if dragon_type == 'AIR_DRAGON':
        air_dragons += 1
    elif dragon_type == 'FIRE_DRAGON':
        fire_dragons += 1
    elif dragon_type == 'EARTH_DRAGON':
        earth_dragons += 1
    elif dragon_type == 'WATER_DRAGON':
        water_dragons += 1
    elif dragon_type == 'HEXTECH_DRAGON':
        hextech_dragons += 1
    elif dragon_type == 'CHEMTECH_DRAGON':
        chemtech_dragons += 1
    elif dragon_type == 'ELDER_DRAGON':
        elder_dragons += 1
    return air_dragons, fire_dragons, earth_dragons, water_dragons, hextech_dragons, chemtech_dragons, elder_dragons

def championName_playerId(match):
    games_dic = {}
    players_id = {}
    flag = True
    for i in range(5):      # First five players form Blue team
        if match['info']['participants'][i]['teamPosition'] == 'TOP':
            games_dic.update({"BLUE TOP": match['info']['participants'][i]['championName']})
            players_id.update({"BLUE TOP": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'MIDDLE':
            games_dic.update({'BLUE MID': match['info']['participants'][i]['championName']})
            players_id.update({"BLUE MID": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'JUNGLE':
            games_dic.update({'BLUE JUNGLE': match['info']['participants'][i]['championName']})
            players_id.update({"BLUE JUNGLE": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'BOTTOM':
            games_dic.update({'BLUE ADC': match['info']['participants'][i]['championName']})
            players_id.update({"BLUE ADC": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'UTILITY':
            games_dic.update({'BLUE SUPPORT': match['info']['participants'][i]['championName']})
            players_id.update({"BLUE SUPPORT": match['info']['participants'][i]['participantId']})
        else:
            flag = False    # Flagging invalid roles on Blue team

        
    for i in range(5,10):       # Second five players from Red team
        if match['info']['participants'][i]['teamPosition'] == 'TOP':
            games_dic.update({"RED TOP": match['info']['participants'][i]['championName']})
            players_id.update({"RED TOP": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'MIDDLE':
            games_dic.update({'RED MID': match['info']['participants'][i]['championName']})
            players_id.update({"RED MID": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'JUNGLE':
            games_dic.update({'RED JUNGLE': match['info']['participants'][i]['championName']})
            players_id.update({"RED JUNGLE": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'BOTTOM':
            games_dic.update({'RED ADC': match['info']['participants'][i]['championName']})
            players_id.update({"RED ADC": match['info']['participants'][i]['participantId']})
        elif match['info']['participants'][i]['teamPosition'] == 'UTILITY':
            games_dic.update({'RED SUPPORT': match['info']['participants'][i]['championName']})
            players_id.update({"RED SUPPORT": match['info']['participants'][i]['participantId']})
        else:
            flag = False    # Flagging invalid roles on Red team

    return games_dic, players_id, flag
        

def intialization(players_id):
        # Initializations
        red_towers = ['RED TOP_LANE OUTER_TURRET','RED MID_LANE OUTER_TURRET','RED BOT_LANE OUTER_TURRET',
                        'RED TOP_LANE INNER_TURRET' , 'RED MID_LANE INNER_TURRET', 'RED BOT_LANE INNER_TURRET',
                        'RED TOP_LANE BASE_TURRET', 'RED MID_LANE BASE_TURRET', 'RED BOT_LANE BASE_TURRET',
                        'RED MID_LANE NEXUS_TURRET' , 'RED MID_LANE NEXUS_TURRET']

        blue_towers =  ['BLUE TOP_LANE OUTER_TURRET','BLUE MID_LANE OUTER_TURRET','BLUE BOT_LANE OUTER_TURRET',
                        'BLUE TOP_LANE INNER_TURRET' , 'BLUE MID_LANE INNER_TURRET', 'BLUE BOT_LANE INNER_TURRET',
                        'BLUE TOP_LANE BASE_TURRET', 'BLUE MID_LANE BASE_TURRET', 'BLUE BOT_LANE BASE_TURRET',
                        'BLUE MID_LANE NEXUS_TURRET' , 'BLUE MID_LANE NEXUS_TURRET']
        

        
        
        red_first_tower = False
        blue_first_tower = False

        red_top_inhib = 1
        red_mid_inhib = 1
        red_bot_inhib = 1
        

        blue_top_inhib = 1
        blue_mid_inhib = 1
        blue_bot_inhib = 1
       

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


        kda = {
        0:0,
        players_id['BLUE TOP'] : 0,
        players_id['BLUE JUNGLE']: 0,
        players_id['BLUE MID'] : 0,
        players_id['BLUE ADC'] : 0,
        players_id['BLUE SUPPORT']: 0,
        
        players_id['RED TOP'] : 0,
        players_id['RED JUNGLE']: 0,
        players_id['RED MID'] : 0,
        players_id['RED ADC'] : 0,
        players_id['RED SUPPORT']: 0,

        }
    
        kills = {
        0:0,
        players_id['BLUE TOP'] : 0,
        players_id['BLUE JUNGLE']: 0,
        players_id['BLUE MID'] : 0,
        players_id['BLUE ADC'] : 0,
        players_id['BLUE SUPPORT']: 0,
        
        players_id['RED TOP'] : 0,
        players_id['RED JUNGLE']: 0,
        players_id['RED MID'] : 0,
        players_id['RED ADC'] : 0,
        players_id['RED SUPPORT']: 0,

        }

        deaths ={
        0:0,
        players_id['BLUE TOP'] : 0,
        players_id['BLUE JUNGLE']: 0,
        players_id['BLUE MID'] : 0,
        players_id['BLUE ADC'] : 0,
        players_id['BLUE SUPPORT']: 0,
        
        players_id['RED TOP'] : 0,
        players_id['RED JUNGLE']: 0,
        players_id['RED MID'] : 0,
        players_id['RED ADC'] : 0,
        players_id['RED SUPPORT']: 0,
        }
        assists = {
        0:0,
        players_id['BLUE TOP'] : 0,
        players_id['BLUE JUNGLE']: 0,
        players_id['BLUE MID'] : 0,
        players_id['BLUE ADC'] : 0,
        players_id['BLUE SUPPORT']: 0,
        
        players_id['RED TOP'] : 0,
        players_id['RED JUNGLE']: 0,
        players_id['RED MID'] : 0,
        players_id['RED ADC'] : 0,
        players_id['RED SUPPORT']: 0,

        }


        return red_towers, blue_towers ,red_top_inhib , red_mid_inhib ,red_bot_inhib, blue_top_inhib, blue_mid_inhib ,blue_bot_inhib,red_fire_dragons,red_water_dragons,red_earth_dragons,red_air_dragons,red_hextech_dragons,red_chemtech_dragons,red_elder_dragons,blue_fire_dragons,blue_water_dragons,blue_earth_dragons,blue_air_dragons,blue_hextech_dragons,blue_chemtech_dragons,blue_elder_dragons,red_barons,blue_barons,red_rift,blue_rift,red_hordes,blue_hordes, kills, deaths, assists, kda, red_first_tower, red_first_blood, blue_first_tower, blue_first_blood
    


def kills_deaths_assists(killer_id, victim_id, assistors_list,kills,deaths,assists):
        kills[killer_id] += 1
        deaths[victim_id] += 1
        if len(assistors_list) != 0:
                for assistor in assistors_list:
                        assists[assistor] += 1

        return kills, deaths, assists
    

def compute_kda(kills, deaths, assists,kda):
    for i in range(1,11): # participantsId from 1 to 10
        kda[i] = (kills[i] + assists[i]) if deaths[i] == 0 else round((kills[i] + assists[i]) / deaths[i],2)
    return kda
    
def players_cs(participant_frame,players_id):
    players_cs_dic = {}
    keys = list(players_id.keys())

    for i in range(1,11):
        if keys[i-1] == "RED SUPPORT" or keys[i-1] == "BLUE SUPPORT":   # Neglect supports cs
            continue
        players_cs_dic[keys[i-1] + " " + "CS"] = participant_frame[str(i)]['minionsKilled'] +  participant_frame[str(i)]['jungleMinionsKilled']
        
    return players_cs_dic

def champions_level(participant_frame, players_id):
    levels = {}
    keys = list(players_id.keys())
    for i in range(1,11):
        levels[keys[i-1] + " " + "LEVEL"] = participant_frame[str(i)]['level']

    return levels

def collect_items(match_data, players_id):
    keys = list(players_id.keys())
    items_dic = {}
    for key in keys:
        items_list = []
        for i in range(6):  # Items 0 to 5, neglecting slot 6 which contains the ward
            items_list.append(match_data['info']['participants'][keys.index(key)][f'item{i}'])

        items_dic[f"{key} Items"] = items_list

    return items_dic
