# %%
from bs4 import BeautifulSoup, Comment
import pandas as pd
import requests
import time
import random
import os
from glob import glob
from tqdm import tqdm

# %%
col_names = ['match_id', 'gameweek', 'day_of_week',
             'date', 'time', 'home_team', 'xg_home', 'score_home',
             'score_away', 'xg_away', 'away_team', 'attendance', 'venue',
             'referee', 'match_report_url', 'tmp1']

summary_col_names = ['player_name', 'shirt_num', 'nationality',
                     'position', 'minute_played',
                     'goals', 'assists', 'penalties', 'penalty_attempt',
                     'shots', 'shots_on_target', 'yellow_card', 'red_card',
                     'touch', 'pressure', 'tackles', 'interceptions', 'blocks',
                     'xg', 'npxg', 'xa',
                     'sca', 'gca',
                     'passes', 'pass_attempts', 'pass_percentage', 'progress_pass_yrd',
                     'carries', 'progress_carry_yrd', 'dribbles', 'dribble_attempts']

passing_col_names = ['player_name', 'shirt_num', 'nationality',
                     'position', 'minute_played',
                     'passes', 'pass_attempts', 'pass_percentage', 'pass_yrd', 'progress_pass_yrd',
                     'short_passes', 'short_pass_attempts', 'short_pass_percentage',
                     'medium_passes', 'medium_pass_attempts', 'medium_pass_percentage',
                     'long_passes', 'long_pass_attempts', 'long_pass_percentage',
                     'assists', 'xa', 'key_passes', 'pass_to_final_third', 'pass_to_penalty_area', 
                     'crosses_to_penalty_area', 'progress_pass']

passing_types_col_names = ['player_name', 'shirt_num', 'nationality',
                           'position', 'minute_played', 'pass_attempts',
                           'live_ball', 'dead_ball', 'free_kicks', 'throw_ins',
                           'pressing', 'switch_plays', 'crosses', 'corner_kicks',
                           'in_swing_corners', 'out_swing_corners', 'straigth_corners',
                           'ground_passes', 'low_passes', 'high_passes',
                           'left_foot', 'right_foot', 'header', 'throw', 'others',
                           'completed', 'offsides', 'out_of_bound', 'intercepted', 'blocks']

defense_col_names = ['player_name', 'shirt_num', 'nationality',
                     'position', 'minute_played',
                     'tackles', 'tackles_won',
                     'tackles_def_3rd', 'tackles_mid_3rd', 'tackles_akt_3rd',
                     'tackles_v_dribble', 'tackle_attempts_v_dribble', 'tackles_v_dribble_percentage', 'past',
                     'pressure', 'pressure_success', 'pressure_percentage',
                     'pressure_def_3rd', 'pressure_mid_3rd', 'pressure_akt_3rd',
                     'blocks', 'shots_blocked', 'shots_saved', 'passes_blocked',
                     'interceptions', 'int_plus_tackles', 'clearances', 'error']

possession_col_names = ['player_name', 'shirt_num', 'nationality',
                        'position', 'minute_played',
                        'touches', 'touches_def_pen', 'touches_def_3rd',
                        'touches_mid_3rd', 'touches_akt_3rd', 'touches_atk_pen',
                        'touches_live_ball',
                        'dribbles', 'dribble_attempts', 'dribble_percentage',
                        'players_pass', 'nutmegs',
                        'carries', 'total_carry_yrd', 'progress_carry_yrd', 
                        'receive_target', 'receives', 'receive_percentage',
                        'miscontrolled', 'dispossessed',
                        ]

misc_col_names = ['player_name', 'shirt_num', 'nationality',
                  'position', 'minute_played',
                  'yellow_card', 'red_card', '2nd_yellow_card',
                  'fouls', 'fouled', 'offsides', 'crosses', 'interceptions',
                  'tackles', 'penalty_won', 'penalty_conceded',
                  'own_goals', 'recovery',
                  'aerial_won', 'aerial_lost', 'aerial_won_percentage']

keeper_col_names = ['player_name', 'nationality', 'minute_played',
                  'shots_on_target_against', 'goals_against',
                  'saves', 'save_percentage', 'psxg',
                  'launch_completed', 'launch_attempts', 'launch_completed_percentage',
                  'pass_attempts', 'throw_attempts',
                  'launch_to_pass', 'avg_pass_yrd',
                  'goal_kick_attempts', 'launch_to_gk', 'avg_gk_yrd',
                  'opponent_crosses', 'crosses_stoped', 'cross_stop_percentage',
                  'def_actions_outside_penaly_area', 'avg_def_action_yrd']

shot_col_names = ['minute', 'player_name', 'squad',
                  'shot_outcome', 'shot_distance',
                  'body_part', 'notes',
                  'sca_1_player_name', 'sca_1_pass_type',
                  'sca_2_player_name', 'sca_2_pass_type',]


url = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
url_base = 'https://fbref.com/en'

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

def get_fixture(response=None, season_id=None):
    target_url = response.url
    if season_id is None:
        season_id = target_url.split('/')[6]
    div_id = f'div_sched_ks_{season_id}_1'
    table_id = f'sched_ks_{season_id}_1'
    print(div_id, table_id)
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

def extract_fixture(fixture_list=None, match_week=(0, 0), match_id=(0, 0)):
    data = []
    idx = 0
    (week_start, week_end) = match_week
    (match_start, match_end) = match_id

    for row in table:
        if not row.attrs.get('class'):
            match = []
            idx+=1
            match.append(idx)
            table_contents = row.find_all('td')
            match_note = bool(table_contents[-1].text)
            match_played = [table_contents[4].text, table_contents[5].text, table_contents[6].text]
            match_played = all(match_played)
            if not match_note and match_played:
                for col in row:
                    if col['data-stat'] == 'match_report':
                        match.append(col.find('a')['href'])
                    elif col['data-stat'] == 'score':
                        try:
                            match.append(col.text.split('–')[0])
                            match.append(col.text.split('–')[1])
                        except:
                            match.append(None)
                            match.append(None)
                    else:
                        match.append(col.text)
            else:
                # match += [col.text for col in row]
                continue
            if len(match) > 16:
                data.append(match[:-1])
            else:
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
soup = BeautifulSoup(response.content)
table = soup.find('div', {'class': 'overthrow table_container',
                              'id': 'div_sched_ks_10728_1'})
table = table.find('table', {'id': 'sched_ks_10728_1'})
table = table.find('tbody')
table = table.find_all('tr')
data = []
idx = 0
for row in table:
    if not row.attrs.get('class'):
        match = []
        idx+=1
        match.append(idx)
        if not bool(row.find_all('td')[-1].text):
            for col in row:
                if col['data-stat'] == 'match_report':
                    match.append(col.find('a')['href'])
                elif col['data-stat'] == 'score':
                    try:
                        match.append(col.text.split('–')[0])
                        match.append(col.text.split('–')[1])
                    except:
                        match.append(None)
                        match.append(None)
                else:
                    match.append(col.text)
        else:
                match = [col.text for col in row]
        if len(match) > 16:
            data.append(match[:-1])
        else:
            data.append(match)

df = pd.DataFrame(data, columns=col_names)
# %%
def get_results_from_fixture(response=None, match_week=(0, 0), match_id=(0, 0)):
    (week_start, week_end) = match_week
    (match_start, match_end) = match_id

    data = []
    return data
# %%
df.to_csv('/Users/Mai/Projects/ideas/open-data/fbref/fff/20192020/fixtures.csv')
t1 = time.time()
print(f'take {t1-t0:.2f} s')