from bs4 import BeautifulSoup
import os
import pickle

with open('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/20210103_live_report_paths.pkl', 'rb') as f:
    live_report_paths = pickle.load(f)
print(f'has {len(live_report_paths)} matches')

# %%
with open('/Users/Mai/Projects/football-analytics/codes/test.txt', 'r') as f:
    tmp = f.readline()

tmp = BeautifulSoup(tmp)
results = tmp.find_all('div', {'class': 'col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 result divtable-data'})
print(len(results))
print(f'has {len(live_report_paths)} matches')
for i, div in enumerate(results):
    live_report_paths.append(div.find('a')['href'])
print(f'added {i+1} matches')
print(f'now has {len(live_report_paths)} matches.')