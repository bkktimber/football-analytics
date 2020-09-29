# %%
import asyncio
import json
import aiohttp
import random
import pandas as pd
import time
from understat import Understat

# %%
shot_col = ['match_id', 'minute', 'player', 'coord_x', 'coord_y', 'shot_type', 'xg', 'outcome', 'situation', 'player_assist', 'last_action']
save_path = '/Users/Mai/Projects/football-analytics/data/understats/epl/20182019'
team_status_mapping = {'h': 'home', 'a': 'away'}

# %%
async with aiohttp.ClientSession() as session:
    understat = Understat(session)
    fix = await understat.get_league_results(
            "epl",
            2018,
        )
len(fix)
idx = []
for f in fix:
    if bool(f['isResult']):
        idx.append(f['id'])

len(idx)

# %%
for i in idx[24:]:
    if not os.path.isdir(os.path.join(save_path, str(i))):
        os.mkdir(os.path.join(save_path, str(i)))
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        shots = await understat.get_match_shots(i)
    len(shots)
    for k, v in shots.items():
        team = k
        data = []
        for shot in v:
            minute = shot['minute']
            outcome = shot['result']
            coord_x = shot['X']
            coord_y = shot['Y']
            xg = shot['xG']
            player = shot['player']
            situation = shot['situation']
            shot_type = shot['shotType']
            match_id = shot['match_id']
            player_assist = shot['player_assisted']
            last_act = shot['lastAction']
            data.append([match_id, minute, player,
                        coord_x, coord_y, shot_type, 
                        xg, outcome, situation,
                        player_assist, last_act])
        df = pd.DataFrame(data, columns=shot_col)
        fn = f'{team_status_mapping[team]}.csv'
        fn = os.path.join(save_path, str(i), fn)
        df.to_csv(fn)
        print('saved file to ', fn)
    d = random.randint(3, 7)
    d = int(d * 5)
    print(f'sleep for {d} s')
    time.sleep(d)
    print('continue')
# %%
