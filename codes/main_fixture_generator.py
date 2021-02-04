import pandas as pd
import pickle
import os

fixture = '/Users/Mai/Projects/football-analytics/data/epl/20202021/fixtures.csv'
epl_20202021_fixture = pd.read_csv(fixture)

whoscored_data_dir = '/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021'
whoscored_match_dirs = [d for d in os.listdir(whoscored_data_dir) if os.path.isdir(os.path.join(whoscored_data_dir, d))]
whoscored_data = [os.path.join(whoscored_data_dir,
                               d, 'data.pkl') for d in whoscored_match_dirs if not d.startswith('.')]
lst = []
for path in whoscored_data:
    with open(path, 'rb') as f:
        data = pickle.load(f)
    home_team_name = data[0].get('home').get('name')
    away_team_name = data[0].get('away').get('name')
    whoscored_match_id = data[2]
    lst.append([whoscored_match_id, home_team_name, away_team_name])

# map from Opta names (in Whoscored) to Statsbomb names (FBref)
# epl_team_dict = {'Arsenal': 'Arsenal',
#                  'Aston Villa': 'Aston Villa',
#                  'Brighton': 'Brighton',
#                  'Burnley': 'Burnley',
#                  'Chelsea': 'Chelsea',
#                  'Crystal Palace': 'Crystal Palace',
#                  'Everton': 'Everton',
#                  'Fulham': 'Fulham',
#                  'Leeds': 'Leeds United',
#                  'Leicester': 'Leicester City',
#                  'Liverpool': 'Liverpool',
#                  'Man City': 'Manchester City',
#                  'Man Utd': 'Manchester Utd',
#                  'Newcastle': 'Newcastle Utd',
#                  'Sheff Utd': 'Sheffield Utd',
#                  'Southampton': 'Southampton',
#                  'Tottenham': 'Tottenham',
#                  'West Brom': 'West Brom',
#                  'West Ham': 'West Ham',
#                  'Wolves': 'Wolves'}
col_names = ['whoscored_match_id', 'home_team', 'away_team']
tmp = pd.DataFrame(lst, columns=col_names)

opta_epl_names = pd.unique(tmp.home_team.sort_values(ascending=True)).tolist()
statsbomb_epl_names = pd.unique(epl_20202021_fixture.home_team.sort_values(ascending=True)).tolist()
epl_team_dict = dict(zip(opta_epl_names, statsbomb_epl_names))

tmp.replace({'home_team': epl_team_dict}, inplace=True)
tmp.replace({'away_team': epl_team_dict}, inplace=True)
tmp.head()

epl_20202021_fixture_main = pd.merge(epl_20202021_fixture.iloc[:, 1:-1], tmp, on=['home_team', 'away_team'], how='left')
print(epl_20202021_fixture_main.tail(20))

epl_20202021_fixture_main.to_pickle('/Users/Mai/Projects/football-analytics/data/fixtures/20202021/epl_fixture.pkl')