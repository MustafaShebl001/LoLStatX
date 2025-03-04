
# LoLStatX

A brief description of what this project does and who it's for

This project is mainly for *League Of Legends* **(LOL)** players and enthusiasts.

We have different folders in this repo, let's explain briefly each one:
**Get Matches**
Collecting relevant games data from riot API provided from riot games, here we are navigating through played games to collect them in a DataFrame to be used in training the model, looping over players Puuids (unique identifiers for each player per API) with taking ratelimit in consideration (100 requests per 2 min) by implementing *sleepfunction*, also considering games only in Summoners' rift with healthy format (10 players exist per match).

**Puuid** Collecting players Puuids from riot API by specifying: *division, tier, key, number of pages*.

**Statistics** Implementing GUIs, collecting live game data from localhost URLs into identical DataFrame to be used by the predictive model, collect your last x games data and format it into DataFrame to be used in **'MY STATS'**.

**Win Probability** Including model training, here concat all games from different divisions in one DataFrame, perform some important formating on the data, then implementing the model to feed it with this data, after finishing we compared different models (dicision tree, logistic regression, FFNN) by inspecting the weights and features and FFNN gave the most reasonable and logical weights and features, lastly we save the model to be used in the prediction process.

**-------------------------Application Interface-------------------------**

By providing your account name, tagline, and region you will have three choices:

**MATCH HISTORY:** provide you with screen like in game match history, inspired by op.gg, displaying post games results and stats, like champions, win/lose, items, KDA, damage, and more. It shows byt default first 20 games but has "SHOW MORE" button to load next 20 games.

**MY STATS:** asks you for a given number of games to be considered, then shows over 30 stats about these games which helps players see their accumlative performance.

**Predict Win Probability (Live Match):** uses a deeplearning model (FFNN) trained with almost 600,000 games collected from all rank divisions to predict your current win probability for given game objectives and player stats (almost 50 features used) and achieved over 97% accuracy on both dev and test set with almost 98% accuracy on training set.


## External files for icons

You need to download game icon images from profileicons, items, champions from the next link and replacing the **VERSION** with desired *LOL* version.
https://ddragon.leagueoflegends.com/cdn/dragontail-{VERSION}.tgz
