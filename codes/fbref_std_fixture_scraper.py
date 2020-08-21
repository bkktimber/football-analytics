# %%
from bs4 import BeautifulSoup, Comment
import pandas as pd
import requests
import time
import random
import os
from glob import glob
from tqdm import tqdm

col_names = ['match_id', 'gameweek', 'day_of_week',
             'date', 'time', 'home_team', 'score_home',
             'score_away', 'away_team', 'attendance', 'venue',
             'referee', 'match_report_url', 'tmp1']

url = 'https://fbref.com/en/comps/9/1526/schedule/2016-2017-Premier-League-Scores-and-Fixtures'

# %%
def url_request(url=None):
    print(f'Prepare to load data from {url}')
    t0 = time.time()
    target_page = url
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_page, headers=headers)
    t1 = time.time()
    print(f'Load Completed. Take {t1-t0:.2f} s')
    return response

def get_fixture(response=None):
    target_url = response.url
    season_id = target_url.split('/')[6]
    div_id = f'div_sched_ks_{season_id}_1'
    table_id = f'sched_ks_{season_id}_1'
    print(div_id, div_id)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content)

    else:
        print(f'Bad Response: code {response.status_code}')
        return None
    
    fixture = soup.find('div', {'class': 'overthrow table_container',
                              'id': div_id})
    fixture = fixture.find('table', {'id': table_id})
    fixture = fixture.find('tbody')
    fixture = fixture.find_all('tr')
    return [season_id, fixture]

def check_previous(content=None):
    has_previous = False
    link = None
    s = BeautifulSoup(content)
    season_links = s.find('div', {'class': 'prevnext'})
    season_links = season_links.find_all('a')
    if len(season_links) != 2:
        print(f'End of fixture')
    else:
        link = season_links[0]['href']
        has_previous = True
    return [has_previous, link]

def extract_fixture(fixture_list=None):
    data = []
    idx = 0
    for row in fixture_list:
        if not row.attrs.get('class'):
            match = []
            idx += 1
            match.append(idx)
            for col in row:
                if col['data-stat'] == 'match_report':
                    match.append(col.find('a')['href'])
                elif col['data-stat'] == 'score':
                    match.append(col.text.split('–')[0])
                    match.append(col.text.split('–')[1])
                else:
                    match.append(col.text)
            data.append(match)
    return data

# %%
response = url_request(url)
previous_flag = check_previous(response.content)
while previous_flag[0]:
    season_id, fixtures = get_fixture(response)
    data = extract_fixture(fixtures)
    filename = f'epl_fixture_{season_id}.csv'
    df = pd.DataFrame(data, columns=col_names)
    save_path = '/Users/Mai/Projects/football-analytics/data/match_records/epl'
    print(f'Save fixture to {filename}')
    df.to_csv(os.path.join(save_path, filename))
    print('Save Completed.')
    print('Cool Down')
    time.sleep(7)
    print('Check for previous season')
    url =  'https://fbref.com' + previous_flag[1]
    response = url_request(url)
    previous_flag = check_previous(response.content)

print('No more fixure')

# %%
