# %%
from bs4 import BeautifulSoup
import os
import pickle

# %%
live_path = '/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/all_live_report_paths.pkl'
with open(live_path, 'rb') as f:
    live_report_paths = pickle.load(f)

num_records = len(live_report_paths)
print(f'has {num_records} matches')

# %%
# live_report_paths = []
# %%
with open('/Users/Mai/Projects/football-analytics/codes/test.txt', 'r') as f:
    tmp = f.readline()

tmp = BeautifulSoup(tmp, features='html.parser')
results = tmp.find_all('div', {'class': 'col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 result divtable-data'})
print(f'Found {len(results)} new matches.')
i = 0
for _, div in enumerate(results):
    match_url = div.find('a')['href']
    if match_url in live_report_paths:
        continue
    match_id = match_url.split('/')[2]
    match_status = match_url.split('/')[3]
    if match_status == 'Live':
        live_report_paths.append(match_url)
        i += 1
    elif match_status == 'Show':
        print(f'Match id {match_id} has not played.')
print(f'added {i+1} matches')
print(f'now has {len(live_report_paths)} matches.')
print(f'Last match is {live_report_paths[-1]}')
# %%
with open('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/all_live_report_paths.pkl', 'wb') as f:
    pickle.dump(live_report_paths, f)

with open('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/all_live_report_paths.pkl', 'rb') as f:
    live_report_paths_2 = pickle.load(f)

assert live_report_paths == live_report_paths_2
# %%
