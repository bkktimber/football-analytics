# %%
import os
import pandas as pd
# %%
base_dir = '/Users/Mai/Projects/football-analytics/data/match_records/epl'
os.chdir(base_dir)
record_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if not f.startswith('.')]
record_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f != 'epl_fixture_records.csv']
# %%
lst = []
target_dir = '/Users/Mai/Projects/football-analytics/data/fixtures'
for file in record_files:
    data_df = pd.read_csv(file)
    data_df = data_df.iloc[:, 1:-1]
    season_id = file.split('_')[-1][:-4]
    start_year = pd.to_datetime(data_df.head(1).date).dt.strftime('%Y').values[0]
    end_year = pd.to_datetime(data_df.tail(1).date).dt.strftime('%Y').values[0]
    target_season = f'{start_year}{end_year}'
    season_dir = os.path.join(target_dir, target_season)
    # if not os.path.isdir(season_dir):
    #     os.mkdir(season_dir)
    # data_df.to_pickle(os.path.join(season_dir, 'epl_fixture.pkl'))
    lst.append([int(season_id), target_season])
# %%
col_names = ['fbref_epl_season_id', 'season_name']
df = pd.DataFrame(lst, columns=col_names)
df.sort_values(by='fbref_epl_season_id', inplace=True)
df.reset_index(drop=True, inplace=True)
df.loc[:, 'fbref_epl_season_id'] = df.loc[:, 'fbref_epl_season_id'].astype(str)
df.to_pickle('/Users/Mai/Projects/football-analytics/data/fixtures/season_id_keys/fbref_epl.pkl')
# %%
