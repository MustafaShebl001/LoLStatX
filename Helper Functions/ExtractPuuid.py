import requests
import time


def get_summoner_id(region, tier, division, dev_key, Pno):
    ids_list = []
    for n in range(Pno):
        players = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={n+1}&api_key={dev_key}').json() # List of players
        for player in players:
            if player['inactive'] == False:
                ids_list.append({
                    'summonerId': player['summonerId'],
                    "region" : region,
                    'tier': player['tier'],
                    'rank': player['rank'],
                    'no. of games': player['wins'] + player['losses']
                })
    return ids_list

def get_puuid(summoner_id_list, dev_key):
    puuid = []
    for i in range(len(summoner_id_list)):
        try:
            region = summoner_id_list[i]['region']
            summoner_id = summoner_id_list[i]['summonerId']
            response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={dev_key}')
            if response.status_code != 200:
                print(response.status_code)
            if response.status_code == 429:
                time.sleep(125)     # Sleep for 2 min 
                response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={dev_key}')    # Try again
            summoner_api = response.json()
            puuid.append({
                "Puuid": summoner_api['puuid'], # Remember puuid is dev_key dependent
                "region": region,
                "tier": summoner_id_list[i]['tier'],
                "rank": summoner_id_list[i]['rank'],
                "no. of games": summoner_id_list[i]['no. of games']
            })
        except:
            raise Exception(f"Error in get_puuid of index {i}")
    return puuid




def get_master(region, dev_key):
    ids_list = []
    for n in range(1):
        players = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={dev_key}').json()['entries'] # List of players
        for player in players:
            if player['inactive'] == False:
                ids_list.append({
                    'summonerId': player['summonerId'],
                    "region" : region,
                    'tier': 'I',
                    'rank': 'GRANDMASTER',
                    'no. of games': player['wins'] + player['losses']
                })
    return ids_list


def get_grand_master(region, dev_key):
    ids_list = []
    for n in range(1):
        players = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key={dev_key}').json()['entries'] # List of players
        for player in players:
            if player['inactive'] == False:
                ids_list.append({
                    'summonerId': player['summonerId'],
                    "region" : region,
                    'tier': 'I',
                    'rank': 'GRANDMASTER',
                    'no. of games': player['wins'] + player['losses']
                })
    return ids_list


def get_challenger(region, dev_key):
    ids_list = []
    for n in range(1):
        players = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={dev_key}').json()['entries'] # List of players
        for player in players:
            if player['inactive'] == False:
                ids_list.append({
                    'summonerId': player['summonerId'],
                    "region" : region,
                    'tier': 'I',
                    'rank': 'CHALLENGER',
                    'no. of games': player['wins'] + player['losses']
                })
    return ids_list

