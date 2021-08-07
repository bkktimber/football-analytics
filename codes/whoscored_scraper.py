# %%
import requests
import time
import json, _jsonnet
import random
import os
import time
import pickle
import re

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
class seleniumBrowser():
    def setUp(self):
        gecko_path = '/Users/Mai/Projects/football-analytics/gecko/geckodriver'
        self.browser = webdriver.Firefox(executable_path=gecko_path)
    def tearDown(self):
        self.browser.quit()
    def loadUrl(self, target_url):
        self.browser.get(target_url) 
        return self.browser.page_source
    def exeScript(self,  script=[]):
        self.browser.execute_script(script)

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
save_path = '/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021'
match_lst = os.listdir('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021')
match_lst = [f.split('.')[0] for f in lst if len(f.split('.')[0]) == 7]
# %%
for ix, url in enumerate(urls):
    match_id = url.split('/')[4]
    if url.split('/')[5] != 'Live':
        print('No Live Match Data. Please Check')
        print(f'Skip match id: {match_id}')
        continue
    if match_id in match_lst:
        print('Match Already Existed')
        continue
    try:
        print(f'Downloading {url}')
        browser = seleniumBrowser()
        browser.setUp()
        browser.exeScript(f'window.scrollTo({random.randint(0, 1000)}, {random.randint(0, 1000)})')
        soup = BeautifulSoup(browser.loadUrl(url), features='html.parser')
        browser.exeScript(f'window.scrollTo({random.randint(0, 1000)}, {random.randint(0, 1000)})')
        browser.tearDown()

        data = soup.find_all('script')
        lst = [len(str(item)) for item in data]
        data = str(data[lst.index(max(lst))])
        data = data.split('\n')
        match_id_js = re.findall(r'\d+', data[2])[0]
        data_obj = json.loads(_jsonnet.evaluate_snippet('snippet',
                            data[3].lstrip()[17:-1]))
        assert(match_id == match_id_js)
        data_filename = os.path.join(save_path, match_id)
        with open(data_filename + '.pkl', 'wb') as f:
            pickle.dump(data_obj, f, protocol=4)
        print(f'saved file at: {data_filename}')

        print('Wait for cool down.')
        time.sleep(random.randint(13, 23))

        print('Wait a little longer')
        time.sleep(random.randint(60, 180))
        print('OK. Let\'s go!')
    except OSError:
        print('Go to next match')

    
    print(f'Downloaded {ix+1} of {len(urls)} records')
# %%
with open(fp + '.pkl', 'rb') as f:
    data = pickle.load(f)