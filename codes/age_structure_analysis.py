# %%
import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
# %%
os.chdir('/Users/Mai/Projects/football-analytics')
contract = 'data/assests/epl/new-utd.csv'
epl_matches = 'data/epl/20192020'

df_contract = pd.read_csv(contract, index_col=0)
df_fixtures = pd.read_csv(os.path.join(epl_matches, 'fixtures.csv'), index_col=0)

# %%
selected_team = 'Newcastle Utd'
bool_home = (df_fixtures.home_team == selected_team)
bool_away = (df_fixtures.away_team == selected_team)
bool_select = bool_home | bool_away
nufc_fixtures = df_fixtures[bool_select]
nufc_fixtures['is_home'] = 1
nufc_fixtures.loc[bool_away, 'is_home'] = 0
# %%
matches = []
home_mapping = {1: 'home', 0: 'away'}
for idx, row in nufc_fixtures.iterrows():
    match_id = row.match_id
    gw = row.gameweek
    team_status = home_mapping[row.is_home]
    match_report = f'gw_{gw}/match_id_{match_id}/{team_status}_summary.csv'
    match_report = os.path.join(epl_matches, 'matches', match_report)
    tmp = pd.read_csv(match_report, index_col=0)
    tmp.loc[:, 'player_name'] = tmp.player_name.str.strip('\xa0')
    matches.append(tmp)

df_players = pd.concat(matches).groupby(by='player_name')
df_players = df_players.agg({'shirt_num': 'last',
                             'minute_played': 'sum'}).reset_index()
# %%
df_contract.loc[:, 'shirt_num'] = df_contract.loc[:, 'shirt_num'].replace('-', 0)
df_contract.loc[:, 'shirt_num'] = df_contract.loc[:, 'shirt_num'].astype(int)
plot = pd.merge(df_contract, df_players, how='left', on='shirt_num')
# %%
plot.loc[:, 'date_of_birth'] = pd.to_datetime(plot['date_of_birth']).map(lambda x: x.strftime('%Y'))
plot.loc[:, 'join_date'] = pd.to_datetime(plot['join_date']).map(lambda x: x.strftime('%Y'))
plot.loc[:, 'contract_expire'] = pd.to_datetime(plot['contract_expire']).map(lambda x: x.strftime('%Y'))
# %%
plot['age_join'] = plot['join_date'].astype(int) - plot['date_of_birth'].astype(int)
plot['age_exp'] = plot['contract_expire'].astype(int) - plot['date_of_birth'].astype(int)
# %%
