import numpy as np
import pandas as pd
import requests
import ast
import json
import copy
import time
import random
from urllib3 import Timeout, PoolManager


def get_df(match):
    stat_dic = {}
    stat_df = pd.DataFrame()

    for i in range(10):
        # ChampionName
        stat_dic.update({
            "Champion":match['info']['participants'][i]['championName'],
            'Role':match['info']['participants'][i]['teamPosition']
        })


        # kills, deaths, assists, kda
        stat_dic.update({
            'Kills':match['info']['participants'][i]['kills'],
            'Deaths':match['info']['participants'][i]['deaths'],
            'Assists':match['info']['participants'][i]['assists'],
            'Solo Kills':match['info']['participants'][i]['challenges']['soloKills'],
            'First Blood':match['info']['participants'][i]['firstBloodKill'],
            'Kills Near Enemy Turret':match['info']['participants'][i]['challenges']['killsNearEnemyTurret'],
            'Kills Under Own Turret':match['info']['participants'][i]['challenges']['killsUnderOwnTurret'],
            'Largest killingSpree':match['info']['participants'][i]['largestKillingSpree']
        })

        # Damage
        stat_dic.update({
            'Damage/Min': match['info']['participants'][i]['challenges']['damagePerMinute'],
            # 'Kill Participation':match['info']['participants'][i]['challenges']['killParticipation'],
            'Damage dealt to Buildings':match['info']['participants'][i]['damageDealtToBuildings'],
            'Damage dealt to Objectives':match['info']['participants'][i]['damageDealtToObjectives'],
            'Team Damage Percentage': match['info']['participants'][i]['challenges']['teamDamagePercentage'],
            'Total Damage dealt to Champions':match['info']['participants'][i]['totalDamageDealtToChampions'],
            'Total True Damage Dealt to Champions': match['info']['participants'][i]['trueDamageDealtToChampions'],
            'Total Damage taken':match['info']['participants'][i]['totalDamageTaken'],
            'Total Self Mitigated Damage':match['info']['participants'][i]['damageSelfMitigated']
        })

        # wards, control wards, vision score
        stat_dic.update({
            'Stealth Wards Placed':match['info']['participants'][i]['challenges']['stealthWardsPlaced'],
            'Control Wards Placed':match['info']['participants'][i]['challenges']['controlWardsPlaced'] ,
            'Wards Killed':match['info']['participants'][i]['wardsKilled'],  # ['wardTakedowns']
            'Vision Score':match['info']['participants'][i]['visionScore']
        })

        # Buildings
        stat_dic.update({
            'Destroy First Turret':match['info']['participants'][i]['challenges']['firstTurretKilled'],   # ['firstTowerAssist']
            'Turrets Takedown': match['info']['participants'][i]['turretTakedowns'],
            'Turret Plates Taken': match['info']['participants'][i]['challenges']['turretPlatesTaken'],
            'Inhib Takedown': match['info']['participants'][i]['inhibitorTakedowns']
        })

        # Neutral Monsters
        stat_dic.update({
            'Dragon Takedows':match['info']['participants'][i]['challenges']['dragonTakedowns'],
            'Rift Takedowns':match['info']['participants'][i]['challenges']['riftHeraldTakedowns'],
            'Baron Takedowns':match['info']['participants'][i]['challenges']['baronTakedowns'],
            'Elder Dragons Takedowns':match['info']['participants'][i]['challenges']['teamElderDragonKills'],
            # 'Earlest Baron':match['info']['participants'][i]['challenges']['earliestBaron'],
            # 'Earlest Dragon':match['info']['participants'][i]['challenges']['earliestDragonTakedown'],
            'Solo Barons': match['info']['participants'][i]['challenges']['soloBaronKills']
        })


        # Other stats
        stat_dic.update({
            "Exp":match['info']['participants'][i]['champExperience'],
            'Gold/Min':match['info']['participants'][i]['challenges']['goldPerMinute'],
            'Total Gold Earned':match['info']['participants'][i]['goldEarned'],
            'Total Time Spent Dead':match['info']['participants'][i]['totalTimeSpentDead'],
            'Skill Shots Dodged':match['info']['participants'][i]['challenges']['skillshotsDodged'],
            'Skill Shots Hit':match['info']['participants'][i]['challenges']['skillshotsHit'],
            # 'Max CS Advantage on Lane Opponent': match['info']['participants'][i]['challenges']['maxCsAdvantageOnLaneOpponent'],
            # 'Max Level Lead Lane Opponent':match['info']['participants'][i]['challenges']['maxLevelLeadLaneOpponent'],
            'Game Ended in Surrender': match['info']['participants'][i]['gameEndedInSurrender'],
            'Time': str(match['info']['participants'][i]['timePlayed'])
        })

        # Jungler stats
        stat_dic.update({
            'Jungle Cs before min 10':match['info']['participants'][i]['challenges']['jungleCsBefore10Minutes'],
            'Number of ScuttleCrabs Killed':match['info']['participants'][i]['challenges']['scuttleCrabKills']
        })

        # Not jungler nor support
        stat_dic.update({
            'CS': match['info']['participants'][i]['neutralMinionsKilled'] + match['info']['participants'][i]['totalMinionsKilled'],
            'Lane Cs before min 10': match['info']['participants'][i]['challenges']['laneMinionsFirst10Minutes']
        })

        # Helping Teammates
        stat_dic.update({
            'Total Time CC Dealt':match['info']['participants'][i]['totalTimeCCDealt'],
            'Total Healing':match['info']['participants'][i]['totalHeal'],
            'Total Heals on Teammates':match['info']['participants'][i]['totalHealsOnTeammates'],
            'Total Damage Shielded in Teammates':match['info']['participants'][i]['totalDamageShieldedOnTeammates'],
            
        })

        stat_dic.update({
            'Wards Placed': match['info']['participants'][i]['wardsPlaced']

        })

        # Win
        stat_dic.update({
            'Win':match['info']['participants'][i]['win']
        })

        # Adv on Lanning Opponent 
        stat_dic.update({
        })

        # Concluded stats
        # vision score per min, wards per min, 

        stat_df = pd.concat([stat_df,pd.DataFrame([stat_dic])], ignore_index=True)
    return stat_df.reset_index(drop=True)
