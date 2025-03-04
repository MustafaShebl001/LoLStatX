
# LoLStatX

A brief description of what this project does and who it's for

This project is mainly for *League Of Legends* **(LOL)** players and enthusiasts.
By providing your account name, tagline, and region you will have three choices:

**MATCH HISTORY:** provide you with screen like in game match history, inspired by op.gg, displaying post games results and stats, like champions, win/lose, items, KDA, damage, and more. It shows byt default first 20 games but has "SHOW MORE" button to load next 20 games.

**MY STATS:** asks you for a given number of games to be considered, then shows over 30 stats about these games which helps players see their accumlative performance.

**Predict Win Probability (Live Match):** uses a deeplearning model (FFNN) trained with almost 600,000 games collected from all rank divisions to predict your current win probability for given game objectives and player stats (almost 50 features used) and achieved over 97% accuracy on both dev and test set with almost 98% accuracy on training set.



## External files for icons

You need to download game icon images from profileicons, items, champions from the next link and replacing the **VERSION** with desired *LOL* version.
https://ddragon.leagueoflegends.com/cdn/dragontail-{VERSION}.tgz
