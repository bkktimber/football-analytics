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

with open(os.path.join(base_dir, 'check_data_key.json'), 'r') as f:
    test_data = json.load(f)
data_key_verify = test_data.keys()

def ensure_dst_dir(match_id: str=''):
    dst_dir = match_id
    dst_dir = os.path.join(base_dir, competition, season, dst_dir)
    if not os.path.exists(dst_dir+'.pkl'):
        os.mkdir(dst_dir)
        if os.path.exists(dst_dir):
            print(f'Created directory at {dst_dir}')
        else:
            raise FileNotFoundError(f'Could not create directory at {dst_dir}')
    else:
        raise OSError(f'Path already existed at {dst_dir}')
    return dst_dir

def save_pickle(dst_dir: str = None, data: list=[], match_id: str = None):
    assert match_id is not None
    if (dst_dir is not None) and data:
        with open(dst_dir + '.pkl', 'wb') as f:
            pickle.dump(data[0], f, protocol=4)

        with open(dst_dir + '.pkl', 'rb') as f:
            tmp = pickle.load(f)
        print(f'Saved data to {dst_dir}')
        print('verify pickle file.')
        # for i, (o, d) in enumerate(zip(data[0], tmp)):
        assert data[0] == tmp
        assert tmp.keys() == data_key_verify
        print('Completed.')
    else:
        raise ValueError('Please specify destination path')
    return None
# %%
with open('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/all_live_report_paths.pkl', 'rb') as f:
    live_report_paths = pickle.load(f)
print(f'has {len(live_report_paths)} matches')

whoscored_base_url = 'https://www.whoscored.com'
urls = [whoscored_base_url + p for p in live_report_paths]

# %%
for ix, url in enumerate(urls):
    match_id = url.split('/')[4]
    if url.split('/')[5] != 'Live':
        print('No Live Match Data. Please Check')
        print(f'Skip match id: {match_id}')
        continue
    try:
        dst_dir = ensure_dst_dir(match_id=match_id)
        os.environ['MOZ_HEADLESS'] = '1'
        driver = webdriver.Firefox(executable_path='/Users/Mai/Projects/football-analytics/gecko/geckodriver')
        print(f'Opening {url}')
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 1000)") 
        soup = BeautifulSoup(driver.page_source, features='html.parser')
        driver.execute_script("window.scrollTo(0, 800)") 
        time.sleep(random.randint(13, 23))
        driver.quit()
        print('Extracting data..')
        data = soup.find('div', {'id': 'multiplex-parent'})
        data = data.find_next('script', {'type': 'text/javascript'})
        data = str(data).split(';')
        print(f'Found {len(data)} items from {url}.')

        lst = []
        for idx, item in enumerate(data):
            extractor = extraction_dict.get(idx)
            item = item.split(extractor['split_txt'])[-1]
            if extractor['type'] == 'json':
                lst.append(json.loads(item))
            elif extractor['type'] == 'int':
                lst.append(str(item))
            else:
                break
        assert lst[2] == match_id
        #
        print('Wait for cool down.')
        time.sleep(random.randint(13, 23))
        save_pickle(dst_dir=dst_dir, data=lst, match_id=match_id)

        print('Wait a little longer')
        time.sleep(random.randint(60, 180))
        print('OK. Let\'s go!')
    except OSError:
        print('Go to next match')

    
    print(f'Downloaded {ix+1} of {len(urls)} records')
# %%
