# %%
import glob
import os
import random
import requests
import time
import pandas as pd

from bs4 import BeautifulSoup, Comment
# %%

competition_keys = {
    'epl' : {'competition_name': 'epl',
             'competition_id': 10728,
             'competition_fixture_url': 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures',},
    'serie-a': {'competition_name': 'figc',
             'competition_id': 10730,
             'competition_fixture_url': 'https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures',},
    'laliga': {'competition_name': 'rfef',
             'competition_id': 10731,
             'competition_fixture_url': 'https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures',},
    'ligue-1': {'competition_name': 'fff',
             'competition_id': 10732,
             'competition_fixture_url': 'https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures',},
    'bundesliga' : {'competition_name': 'dfb',
             'competition_id': 10737,
             'competition_fixture_url': 'https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures',},
    
}

col_names = [
    'match_id', 'gameweek', 'day_of_week', 'date', 'time', 'home_team',
    'xg_home', 'score_home', 'score_away', 'xg_away', 'away_team',
    'attendance', 'venue', 'referee', 'match_report_url'
]

summary_col_names = [
    'player_name', 'shirt_num', 'nationality', 'position', 'age', 'minute_played',
    'goals', 'assists', 'penalties', 'penalty_attempt', 'shots',
    'shots_on_target', 'yellow_card', 'red_card', 'touch', 'pressure',
    'tackles', 'interceptions', 'blocks', 'xg', 'npxg', 'xa', 'sca', 'gca',
    'passes', 'pass_attempts', 'pass_percentage', 'progress_pass_yrd',
    'carries', 'progress_carry_yrd', 'dribbles', 'dribble_attempts'
]

passing_col_names = [
    'player_name', 'shirt_num', 'nationality', 'position', 'age', 'minute_played',
    'passes', 'pass_attempts', 'pass_percentage', 'pass_yrd',
    'progress_pass_yrd', 'short_passes', 'short_pass_attempts',
    'short_pass_percentage', 'medium_passes', 'medium_pass_attempts',
    'medium_pass_percentage', 'long_passes', 'long_pass_attempts',
    'long_pass_percentage', 'assists', 'xa', 'key_passes',
    'pass_to_final_third', 'pass_to_penalty_area', 'crosses_to_penalty_area',
    'progress_pass'
]

passing_types_col_names = [
    'player_name', 'shirt_num', 'nationality', 'position', 'age', 'minute_played',
    'pass_attempts', 'live_ball', 'dead_ball', 'free_kicks', 'throw_ins',
    'pressing', 'switch_plays', 'crosses', 'corner_kicks', 'in_swing_corners',
    'out_swing_corners', 'straigth_corners', 'ground_passes', 'low_passes',
    'high_passes', 'left_foot', 'right_foot', 'header', 'throw', 'others',
    'completed', 'offsides', 'out_of_bound', 'intercepted', 'blocks'
]

defense_col_names = [
    'player_name', 'shirt_num', 'nationality', 'position', 'age', 'minute_played',
    'tackles', 'tackles_won', 'tackles_def_3rd', 'tackles_mid_3rd',
    'tackles_akt_3rd', 'tackles_v_dribble', 'tackle_attempts_v_dribble',
    'tackles_v_dribble_percentage', 'past', 'pressure', 'pressure_success',
    'pressure_percentage', 'pressure_def_3rd', 'pressure_mid_3rd',
    'pressure_akt_3rd', 'blocks', 'shots_blocked', 'shots_saved',
    'passes_blocked', 'interceptions', 'int_plus_tackles', 'clearances',
    'error'
]

possession_col_names = [
    'player_name',
    'shirt_num',
    'nationality',
    'position', 'age',
    'minute_played',
    'touches',
    'touches_def_pen',
    'touches_def_3rd',
    'touches_mid_3rd',
    'touches_akt_3rd',
    'touches_atk_pen',
    'touches_live_ball',
    'dribbles',
    'dribble_attempts',
    'dribble_percentage',
    'players_pass',
    'nutmegs',
    'carries',
    'total_carry_yrd',
    'progress_carry_yrd',
    'progress_carry_count',
    'carry_to_final_third',
    'carry_to_penalty_area',
    'miscontrolled',
    'dispossessed',
    'receive_target',
    'receives',
    'receive_percentage',
    'progressive_pass_recieved'
]

misc_col_names = [
    'player_name', 'shirt_num', 'nationality', 'position', 'age', 'minute_played',
    'yellow_card', 'red_card', '2nd_yellow_card', 'fouls', 'fouled',
    'offsides', 'crosses', 'interceptions', 'tackles', 'penalty_won',
    'penalty_conceded', 'own_goals', 'recovery', 'aerial_won', 'aerial_lost',
    'aerial_won_percentage'
]

keeper_col_names = [
    'player_name', 'nationality', 'age', 'minute_played', 'shots_on_target_against',
    'goals_against', 'saves', 'save_percentage', 'psxg', 'launch_completed',
    'launch_attempts', 'launch_completed_percentage', 'pass_attempts',
    'throw_attempts', 'launch_to_pass', 'avg_pass_yrd', 'goal_kick_attempts',
    'launch_to_gk', 'avg_gk_yrd', 'opponent_crosses', 'crosses_stoped',
    'cross_stop_percentage', 'def_actions_outside_penaly_area',
    'avg_def_action_yrd'
]

shot_col_names = [
    'minute',
    'player_name',
    'squad',
    'shot_outcome',
    'shot_distance',
    'body_part',
    'notes',
    'sca_1_player_name',
    'sca_1_pass_type',
    'sca_2_player_name',
    'sca_2_pass_type',
]

lineup_col_names = ['team_status', 'team_name',
                    'formation',
                    'player_id', 'player_name', 'shirt_num',
                    'lineup_status']

stats_types = ['summary',
              'passing', 'passing_types',
              'defense', 'possession',
              'misc', 'keeper']

col_names_list = [summary_col_names,
                  passing_col_names, passing_types_col_names,
                  defense_col_names, possession_col_names,
                  misc_col_names,
                  keeper_col_names
                  ]

col_names_dict = dict(zip(stats_types, col_names_list))
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

    fixture = soup.find('div', {
        'class': 'table_container',
        'id': div_id
    })
    # fixture = fixture.find('table', {'id': table_id})
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
    for row in fixture_list:
        if not row.attrs.get('class'):
            match = []
            idx += 1
            match.append(idx)
            table_contents = row.find_all('td')
            match_note = bool(table_contents[-1].text)
            match_played = [
                table_contents[4].text, table_contents[5].text,
                table_contents[6].text
            ]
            match_played = all(match_played)
            if not match_note and match_played:
                for col in row:
                    if col['data-stat'] == 'match_report':
                        match.append(col.find('a')['href'])
                    elif col['data-stat'] == 'score':
                        match.append(col.text.split('–')[0])
                        match.append(col.text.split('–')[1])
                    else:
                        match.append(col.text)
            else:
                continue
            if len(match) > 16:
                data.append(match[:-1])
            else:
                data.append(match[:-1])
    return data


def extract_match_report(response=None):
    soup = BeautifulSoup(response.content)
    table = soup.find('div', {
        'class': 'section_wrapper',
        'id': 'all_kitchen_sink_shots'
    })
    table = table.find('div', {
        'class': 'section_content',
        'id': 'div_kitchen_sink_shots'
    })
    tables = table.find_all('div', {'class': 'table_wrapper'})
    return None


def _extract_lineup(div_field=None):
    lineups = []
    home_team = div_field.find('div', {'class': 'lineup', 'id': 'a'})
    away_team = div_field.find('div', {'class': 'lineup', 'id': 'b'})
    lineup_data = zip(['home', 'away'], [home_team, away_team])
    for team_status, data in lineup_data:
        lineup = []
        teamsheet = data.find_all('tr')
        for ix, player in enumerate(teamsheet):
            if ix == 0:
                team_name, formation = player.text.split('(')
                player_status = 'first_team'
            elif ix == 12:
                player_status = 'sub'
            else:
                player = player.find_all('td')
                shirt_num = player[0].text
                player_name = player[1].text
                player_id = player[1].find('a')['href']
                player_id = player_id.split('/')[-2]
                lineup.append([team_status, team_name[:-1],
                                formation[:-1],
                                player_id, player_name,
                                shirt_num, player_status])
        lineups.append(lineup)
    return lineups[0], lineups[1]


def _extract_shots(div_shots=None, team_uid=None):
    id_txt = f'all_shots_{team_uid}'
    table = div_shots.find('div', {'id': id_txt})
    if table:
        rows = BeautifulSoup(table.find(string=_read_comment))
        rows = rows.find_all('tr')
        data = [[item.text for item in row] for ix, row in enumerate(rows) if ix > 2]
    else:
        data = []
    return data


def _get_team_uid(div_scorebox=None):
    team_uids = []
    teams = div_scorebox.find_all('div', {'itemprop': 'performer'})
    for team in teams:
        team_url = team.find('a')['href']
        team_uids.append(team_url.split('/')[-2])
    return team_uids


def _extract_player_stats(div_stats=None, team_uid=None, stats_type=None):
    if stats_type != 'keeper':
        stat_id_txt = f'div_stats_{team_uid}_{stats_type}'
    else:
        stat_id_txt = f'div_keeper_stats_{team_uid}'
    # print(stat_id_txt)
    stats = div_stats.find('div', {'id': stat_id_txt})
    stats = stats.find('tbody')
    stats = stats.find_all('tr')
    players = []
    for row in stats:
        stat = [col.text for col in row]
        players.append(stat)
    return players


def get_match_data(path=None):
    return [p for p in os.listdir(path) if not p.startswith('.')]


def save_path_generator(base_path, filename):
    assert os.path.isdir(base_path)
    
    target_path = os.path.join(base_path, filename)
    return target_path


def delay_timer():
    print('enter sleep mode...')
    i = random.randint(3, 7)
    time.sleep(i * 11)
    print(f'took {i * 11} s rest. ready to work!')
    return None


def ensure_match_dir(base_dir, match_id):
    match_dir = os.path.join(base_dir, match_id)
    if not os.path.isdir(match_dir):
        os.mkdir(match_dir)
        print('Created direcotry: ', match_dir)
    else:
        print('Path Existed')
    return match_dir


_read_comment = lambda text: isinstance(text, Comment)


# %%
match_report_dir = '/Users/Mai/Projects/football-analytics/data'
season_name = '20202021'
competition = 'epl'
competition = list(competition_keys.get(competition).values())
base_dir = os.path.join(match_report_dir,
                       competition[0],
                       season_name,)
response = url_request(competition[2])
s, f = get_fixture(response, season_id=competition[1])
data = extract_fixture(f)
df = pd.DataFrame(data, columns=col_names)
df.tail()
# %%
df.to_csv(os.path.join(base_dir, 'fixtures.csv'))

report_dir = os.path.join(base_dir, 'matches')
current_match_ids = get_match_data(report_dir)

# %%
# df = pd.read_csv('/Users/Mai/Projects/football-analytics/data/epl/202020211/fixtures.csv')
# match_report_url = df.sample(random_state=42).loc[:, 'match_report_url']
# match_report_url = match_report_url.values[0]

match_urls = df.match_report_url.tolist()
base_url = 'https://fbref.com'
match_data_dir = os.path.join(base_dir, 'matches')
for url in match_urls:
    url = os.path.join(base_url, url[1:])
    match_id = url.split('/')[-2]
    if match_id in current_match_ids:
        print(f'Match {match_id} existed! Skip to next match.')
        continue
    response = url_request(url)
    match_dir = ensure_match_dir(match_data_dir, match_id)
    soup = BeautifulSoup(response.content)
    div_scorebox = soup.find('div', {'class': 'scorebox',})
    home_uid, away_uid = _get_team_uid(div_scorebox)
    table_keys = [(uid, stats_type) for uid in [home_uid, away_uid] for stats_type in stats_types]

    div_lineups = soup.find('div', {'id': 'field_wrap'})
    home_lineup, away_lineup = _extract_lineup(div_lineups)
    home_lineup = pd.DataFrame(home_lineup, columns=lineup_col_names)
    away_lineup = pd.DataFrame(away_lineup, columns=lineup_col_names)

    div_shots = soup.find('div', {'class': 'section_content',
                                'id': 'div_kitchen_sink_shots',
                                })
    for uid in [home_uid, away_uid]:
        shot_data = _extract_shots(div_shots=div_shots, team_uid=uid)
        shot_data = pd.DataFrame(shot_data, columns=shot_col_names)

    for key in table_keys:
        uid = key[0]
        stat_type = key[1]
        filename = f'{uid}_{stat_type}.csv'
        if stat_type == 'keeper':
            id_txt = f'all_keeper_stats_{uid}'      
            player_stats = soup.find('div', {'id': id_txt})
        else:
            id_txt = f'all_player_stats_{uid}'              
            player_stats = soup.find('div', {'id': id_txt})
        player_data = _extract_player_stats(player_stats, uid, stat_type)
        player_data = pd.DataFrame(player_data, columns=col_names_dict[stat_type])
        player_data.to_csv(os.path.join(match_dir, filename))
    print(f'Donwload {url}.')
    delay_timer()
# %%
