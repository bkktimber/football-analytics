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
# %%
url = 'https://www.whoscored.com/Matches/1485454/Live/England-Premier-League-2020-2021-Chelsea-Aston-Villa'

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
with open('/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021/1485454/data.pkl', 'wb') as f:
    pickle.dump(lst, f, protocol=4)
# %%
