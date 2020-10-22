# %%
import os
import json
import pandas as pd
# %%
base_path = '/Users/Mai/Projects/football-analytics/'
os.chdir(base_path)
# %%
fixture_file = 'data/epl/20192020/fixtures.csv'
fixtures = pd.read_csv(fixture_file).iloc[:, 1:-1]
# %%
selected_team = 'Newcastle Utd'
selected_home = (fixtures.home_team == selected_team)
selected_away = (fixtures.away_team == selected_team)
filter_bool = (selected_home | selected_away)
nufc_fixtures = fixtures.loc[filter_bool, :].reset_index(drop=True)
nufc_fixtures = nufc_fixtures.iloc[:, :-1]
nufc_fixtures['is_home'] = 1
nufc_fixtures.loc[(nufc_fixtures.away_team == selected_team), 'is_home'] = 0
# %%
match_report_path = 'data/epl/20192020/matches'
match_id = nufc_fixtures.iloc[0, 0]
match_week = nufc_fixtures.iloc[0, 1]
home_or_away_dict = {
    0: 'away',
    1: 'home',
}
team_status = home_or_away_dict[nufc_fixtures.iloc[0, -1]]
match_report_file = f'gw_{match_week}/match_id_{match_id}/teamsheet_{team_status}.txt'
teamsheet_path = os.path.join(match_report_path, match_report_file)
# %%
with open(teamsheet_path, 'r') as f:
    txt = f.readlines()
# %%
