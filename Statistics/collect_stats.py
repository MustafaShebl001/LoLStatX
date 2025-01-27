import numpy as np
import pandas as pd
import requests
import time


# Collect 100 matches_id for a given user puuid, region, queue_id = 420 represent ranked queue
def get_ranked_match_ids(puuid, region, api_key, count=100, queue_id=420, start=0):     # region like europe
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&queue_id={queue_id}&api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        # return response.json()
        retry_after = 120
        # print("Starting to sleep for", retry_after, "seconds")
        time.sleep(retry_after)
        print("Waking up")

        return get_ranked_match_ids(puuid, region, api_key, queue_id, start, count)
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
def collect_ranked_data(ranked_match_ids, puuid, api_key, region):
    stat_df = pd.DataFrame()
    # Loop over all matches
    for match_id in ranked_match_ids:
        stat_dic = {}
        match = requests.get(f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}')
        if match.status_code != 200:
            return stat_df
            # print("Starting to sleep for 120 seconds")
            # time.sleep(120)
            # print("Waking up")
            # match = requests.get(f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}')
        match = match.json()
        # Loop over all players in the match to identify the  user 
        for i in range(len(match['info']['participants'])):
            if match['info']['participants'][i]['puuid'] == puuid:
                index = i
                role = match['info']['participants'][index]['teamPosition']
        try:
            stat_dic.update({
                # 'Champion':match['info']['participants'][index]['championName'],
                # 'Role':role,
                'Kills':match['info']['participants'][index]['kills'],
                'Deaths':match['info']['participants'][index]['deaths'],
                "Assists":match['info']['participants'][index]['assists'],
                'KDA':(match['info']['participants'][index]['kills'] + match['info']['participants'][index]['assists'])/match['info']['participants'][index]['deaths'] if match['info']['participants'][index]['deaths'] != 0 else match['info']['participants'][index]['kills'] + match['info']['participants'][index]['assists'],
                'First Blood':match['info']['participants'][index]['firstBloodKill'],
                'Solo Kills':match['info']['participants'][index]['challenges']['soloKills'],

                'Damage/Min': match['info']['participants'][index]['challenges']['damagePerMinute'],
                'Damage To Champions':match['info']['participants'][index]['totalDamageDealtToChampions'],
                'Damage To Buildings':match['info']['participants'][index]['damageDealtToBuildings'],
                'Damage To Objectives':match['info']['participants'][index]['damageDealtToObjectives'],
                'Damage Taken':match['info']['participants'][index]['totalDamageTaken'],
                'Team Damage Percentage': match['info']['participants'][index]['challenges']['teamDamagePercentage'],
                'Kill Participation':match['info']['participants'][index]['challenges']['killParticipation'],
                'Self Mitigated Damage':match['info']['participants'][index]['damageSelfMitigated'],
                'True Damage To Champions': match['info']['participants'][index]['trueDamageDealtToChampions'],


                'Dragons Takedown':match['info']['participants'][index]['challenges']['dragonTakedowns'],
                'Rift Herald':match['info']['participants'][index]['challenges']['riftHeraldTakedowns'],
                'Barons Takedown':match['info']['participants'][index]['challenges']['baronTakedowns'],

                'Turrets Takedown': match['info']['participants'][index]['turretTakedowns'],
                'Inhibs Takedown': match['info']['participants'][index]['inhibitorTakedowns'],
                'Turret Plates Taken': match['info']['participants'][index]['challenges']['turretPlatesTaken'],
                'Destroy First Turret':match['info']['participants'][index]['challenges']['firstTurretKilled'],   # ['firstTowerAssist']

                'Wards Placed': match['info']['participants'][index]['wardsPlaced'],
                'Wards/Min':match['info']['participants'][index]['wardsPlaced'] /match['info']['participants'][index]['timePlayed'],
                'Wards Killed':match['info']['participants'][index]['challenges']['wardTakedowns'],
                'Vision Score/Min':match['info']['participants'][index]['challenges']['visionScorePerMinute'],

                'Gold/Min':match['info']['participants'][index]['challenges']['goldPerMinute'],
                "Exp/Min":match['info']['participants'][index]['champExperience']/match['info']['participants'][index]['timePlayed'],

                'Max CS Advantage on Lane Opponent': match['info']['participants'][index]['challenges']['maxCsAdvantageOnLaneOpponent'],

                'Total Time Spent Dead':match['info']['participants'][index]['totalTimeSpentDead']

            })

            # Jungler stats
            if role == 'JUNGLE':
                stat_dic.update({
                    'Jungler CS Before min 10':match['info']['participants'][index]['challenges']['jungleCsBefore10Minutes'],
                    'Number of ScuttleCrabs Killed':match['info']['participants'][index]['challenges']['scuttleCrabKills']
                })

            # Not jungler nor support
            if role != 'JUNGLE' and role != 'UTILITY':
                stat_dic.update({
                    'CS': match['info']['participants'][index]['neutralMinionsKilled'] + match['info']['participants'][index]['totalMinionsKilled'],
                    'Lane CS Before Min 10': match['info']['participants'][index]['challenges']['laneMinionsFirst10Minutes']
                })

            # Helping Teammates
            stat_dic.update({
                'Total Time CC Dealt':match['info']['participants'][index]['totalTimeCCDealt'],
                'Self Healing':match['info']['participants'][index]['totalHeal'],
                'Healing Allys':match['info']['participants'][index]['totalHealsOnTeammates'],
                'Sheilding Allys':match['info']['participants'][index]['totalDamageShieldedOnTeammates'],
                
            })

            stat_dic.update({
            f'Win Rate':match['info']['participants'][index]['win']
            })

            # Adv on Lanning Opponent 
            # stat_dic.update({

            # })
            # Concluded stats
            # vision score per min, wards per min, 
            # print(len(stat_df))
        except:
            print(match_id)
        stat_df = pd.concat([stat_df,pd.DataFrame([stat_dic])], ignore_index=True)
    return stat_df


def format_to_csv_file(stat_df):
    stat_df = stat_df.map(lambda x: int(x) if isinstance(x, bool) else x)      # Convert Bool to int
    df = stat_df.mean(numeric_only=True)        # Get the mean average
    rounded_mean_values = df.round(2)       # Round the mean value to 2 significant figures

    # print(list(rounded_mean_values.items()))
    rounded_df = pd.DataFrame(list(rounded_mean_values.items()), columns=['Statistics', 'Average_Values'])  # Convert it to DataFrame to save it as .csv file

    return rounded_df    # Return the rounded DataFrame with the number of games

