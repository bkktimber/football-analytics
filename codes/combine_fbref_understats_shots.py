# %%
import pandas as pd
import os
import json

# %%
os.chdir('/Users/Mai/Projects/football-analytics')
fb_ref_path = 'data/epl/20202021'
understats_path = 'data/understats/epl/20202021'

fixtures = pd.read_csv(os.path.join(fb_ref_path, 'fixtures.csv'), index_col=0)
fixtures.head()

# %%
for idx, match in fixtures.iterrows():
    match_id = match.match_id
    gw = match.gameweek
    home_team = match.home_team
    away_team = match.away_team
    report_path = f'data/epl/20202021/matches/gw_{gw}/match_id_{match_id}'
    break
    home_shots = pd.read_csv(os.path.join(report_path, 'home_shots.csv'))
    home_shots_xg = pd.read_csv(
        os.path.join(understats_path, f'match_id_{match_id}',
                     'home_shots.csv'))
    away_shots = pd.read_csv(os.path.join(report_path, 'away_shots.csv'))

# step
# 1 convert shots minute to int
# join on minute and player
#  select relevent data
#  save to disk
# %%
