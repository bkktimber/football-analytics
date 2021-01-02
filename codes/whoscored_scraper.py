# %%
import requests
import time
import json
import random
import os
import time
import pickle

from selenium import webdriver
from bs4 import BeautifulSoup, Comment
from glob import glob
from tqdm import tqdm

extraction_dict = {
    0: {'split_txt': 'var matchCentreData = ',
        'type': 'json'},
    1: {'split_txt': 'var matchCentreEventTypeJson = ',
        'type': 'json'},
    2: {'split_txt': 'var matchId = ',
        'type': 'int'},
    3: {'split_txt': 'var formationIdNameMappings = ',
        'type': 'json'},
    4: {'split_txt': None,
        'type': 'terminate'},
}

base_dir = '/Users/Mai/Projects/football-analytics/data/whoscored'
competition = 'epl'
season = '20202021'

def ensure_dst_dir(match_id: str=''):
    dst_dir = match_id
    dst_dir = os.path.join(base_dir, competition, season, dst_dir)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
        if os.path.exists(dst_dir):
            print(f'Created directory at {dst_dir}')
        else:
            raise FileNotFoundError(f'Could not reate directory at {dst_dir}')
    else:
        raise OSError(f'Path existed at {dst_dir}')
    return dst_dir

def save_pickle(dst_dir: str = None, data: list=[]):
    if (dst_dir is not None) and (not data):
        with open(os.path.join(dst_dir, 'data.pkl'), 'wb') as f:
            pickle.dump(data, f, protocol=4)

        with open(os.path.join(dst_dir, 'data.pkl'), 'rb') as f:
            tmp = pickle.load(f)
        for o, d in zip(data, tmp):
            assert o == d     
        print(f'Saved data to {dst_dir}')
    else:
        raise ValueError('Please specify destination path')
    return None

# %%
url = 'https://www.whoscored.com/Matches/1485452/Live/England-Premier-League-2020-2021-Burnley-Sheffield-United'
match_id = url.split('/')[4]
dst_dir = ensure_dst_dir(match_id=match_id)

driver = webdriver.Firefox(executable_path='/tmp/geckodriver')
driver.get(url)

soup = BeautifulSoup(driver.page_source, features='html.parser')
time.sleep(10)
driver.quit()

# %%
data = soup.find('div', {'id': 'multiplex-parent'})
data = data.find_next('script', {'type': 'text/javascript'})
data = str(data).split(';')
print(f'Found {len(data)} items from {url}.')

# %%
lst = []
for idx, item in enumerate(data):
    extractor = extraction_dict.get(idx)
    item = item.split(extractor['split_txt'])[-1]
    if extractor['type'] == 'json':
        lst.append(json.loads(item))
    elif extractor['type'] == 'int':
        lst.append(int(item[:-1]))
    else:
        break
# %%
save_pickle(dst_dir, lst)
# %%
