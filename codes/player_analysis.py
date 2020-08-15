# %%
import os
import pandas as pd
import numpy as np
import matplotsoccer

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as clr
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.lines import Line2D

from codes.radar_factory import radar_factory

plt.style.use('ggplot')

color_map = clr.LinearSegmentedColormap.from_list(
    "intensity", [(0.0, '#EAE2B7'),
                #  (0.25, '#8080FF'),
                #  (0.5, '#FCBF49'),
                #  (0.75, '#FF8080'),
                 (1, '#D62828')])

# %%
data_dir = 'fbref/epl/20192020'
fixture_path = 'fbref/epl/20192020/fixtures.csv'
df_fixture = pd.read_csv(fixture_path).iloc[:, 1:-2]

# %%
selected_team = 'Newcastle Utd'
nufc_matches = df_fixture[(df_fixture.home_team == selected_team) | (df_fixture.away_team == selected_team)]
nufc_matches.reset_index(inplace=True, drop=True)
# %%
nufc_matches['home'] = 1
nufc_matches.loc[nufc_matches.away_team == selected_team, 'home'] = 0

# %%
host_mapping = {0: 'away',
                1: 'home'}
match_ids = nufc_matches.match_id.tolist()
gameweek_ids = nufc_matches.gameweek.tolist()
home_status = nufc_matches.home.tolist()
match_file_dir = 'fbref/epl/20192020/matches'
match_stats_dir = [os.path.join(match_file_dir, f'gw_{g}', f'match_id_{m}') for (g, m) in zip(gameweek_ids, match_ids)]
lst = []
for idx, d in enumerate(match_stats_dir):
    is_home = host_mapping[home_status[idx]]
    filename = f'{is_home}_summary.csv'
    match_stat_file = os.path.join(d, filename)
    tmp = pd.read_csv(match_stat_file, index_col=0)
    tmp.loc[:, 'player_name'] = tmp.player_name.str.strip('\xa0')
    tmp['match_id'] = d.split('_')[-1]
    lst.append(tmp)

df_summary = pd.concat(lst, axis=0, ignore_index=True)
del(lst)
print(df_summary.shape)

# %%
big_joe = df_summary.groupby('player_name').get_group('Joelinton').reset_index(drop=True, inplace=False)
# %%
plt.figure()
plt.plot(np.arange(1,39), big_joe.xg)
plt.plot(np.arange(1,39), big_joe.xg.rolling(3).mean().fillna(0))
plt.xticks(np.arange(38),rotation=90)
plt.axvline(28)
plt.legend()
plt.show()

# %%
formations = []
for idx, f in enumerate(match_stats_dir):
    match_id = f.split('_')[-1]
    is_home = host_mapping[home_status[idx]]
    filename = f'teamsheet_{is_home}.txt'
    teamsheet_file = os.path.join(f, filename)
    with open(teamsheet_file, 'r') as f:
        l = f.readlines()[0]
        l = l.split()[-1]
        formations.append([match_id, l[1:-1]])

df_formations = pd.DataFrame(formations, columns=['match_id', 'formations'])
df_formations.head()
# %%
player_std_col = ['rank', 'player_name', 'nationality',
'position', 'squad', 'age', 'year_of_birth',
 'match_played', 'match_started', 'minute_played',
 'goals', 'assists', 'penalties', 'penalty_attempts',
 'yellow_card', 'red_card',
 'goals_per_90', 'assists_per_90',
 'goal_plus_assist_per_90', 'goal_minus_penalty_per_90',
 'goal_plus_assist_minus_penalty_per_90',
 'xg', 'npxg', 'xa',
 'xg_per_90', 'xa_per_90', 'xg_plus_xa_per_90', 
 'npxg_per_90', 'npxg_plus_xa_per_90',
 'match_report']

player_shot_col = ['rank', 'player_name', 'nationality',
'position', 'squad', 'age', 'year_of_birth', 
'90s', 'goals',  'penalties', 'penalty_attempts',
'shots', 'shot_on_target', 'freekicks', 
'shot_on_target_percentage', 'shot_per_90',
 'shot_on_target_per_90', 'goal_per_shot',
 'goal_per_shot_on_target',
 'xg', 'npxg', 'npxg_per_shot', 'goal_minus_xg',
 'np_goals_minus_npxg', 'match_report'] 

player_pass_col = ['rank', 'player_name', 'nationality',
'position', 'squad', 'age', 'year_of_birth', 
'90s', 'passes_completed', 'pass_attempts', 'pass_complete_percentage',
'total_pass_distance', 'progressive_pass_distance',
 'short_passes_completed',
 'short_passes_attempts',
 'short_pass_complete_percentage',
 'medium_passes_completed',
 'medium_passes_attempts',
 'medium_pass_complete_percentage',
 'long_passes_completed',
 'long_passes_attempts',
 'long_pass_complete_percentage',
 'assists',
 'xa',
 'assists_minus_xa',
 'key_passes',
 'pass_to_final_third',
 'pass_to_penalty_area',
 'cross_to_penalty_area',
 'progressive_pass',
 'match_report']

player_pass_type_col = ['rank', 'player_name', 'nationality',
'position', 'squad', 'age', 'year_of_birth', 
'90s', 'pass_attempts',
 'live_ball_passes',
 'dead_ball_passes',
 'freekick_passes',
 'throughball',
 'under_pressure_passes',
 'switch_of_play_passes',
 'crosses',
 'coner_kicks',
 'corner_kick_inswing',
 'corner_kick_outswing',
 'corner_kick_straigth',
 'ground_level_passes',
 'low_level_passes',
 'high_level_passes',
 'passes_with_left_foot',
 'passes_with_right_foot',
 'passes_with_head',
 'throw_ins',
 'pass_with_other_parts',
 'passes_completed',
 'passes_offsides',
 'passes_out_of_plays',
 'passes_intercepted',
 'passes_blocked',
 'match_report']

#  %%                  
df_all_player = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-std-20192020.csv', header=1, names=player_std_col)
df_all_player_shot = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-shots-20192020.csv', header=1, names=player_shot_col)
df_all_player_pass = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-passing-20192020.csv', header=1, names=player_pass_col)
df_all_player_pass_type = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-pass_type-20192020.csv', header=1, names=player_pass_type_col)

# %%
bool_min = (df_all_player.minute_played > df_all_player.minute_played.median())
bool_not_gk = (df_all_player.position != 'GK')
bool_not_df = (df_all_player.position != 'DF')
bool_filter = (bool_min) & (bool_not_df) & (bool_not_df)
epl_big_joe = []
dfb_big_joe = []
epl_firmino = []
epl_vardy = []

big_joe = 'Joelinton'
firmino = 'Roberto Firmino'
vardy = 'Jamie Vardy'

# %%

col_list = ['goals', 'assists', 'penalties', 'penalty_attempts',
 'xg', 'npxg', 'xa',]

# for col in col_list:
#     df_goals = df_all_player.loc[bool_filter, ['Player', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
#     num_player = df_goals.shape[0]
#     df_goals.loc[:, 'Player'] = df_goals.Player.str.split('\\').str[0]
#     df_goals['percentile'] = df_goals.index * (100/num_player)
#     lst_3.append((df_goals.loc[(df_goals.Player == 'Joelinton'), 'percentile']).tolist()[0]/100)

col_list = ['goals', 'shots', 'shot_on_target', 
'shot_on_target_percentage', 'goal_per_shot',
 'goal_per_shot_on_target',
  'npxg', 'npxg_per_shot',]
for col in col_list:
    df_goals = df_all_player_shot.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    epl_big_joe.append((df_goals.loc[(df_goals.player_name == big_joe), 'percentile']).tolist()[0]/100)

col_list = ['key_passes', 'pass_to_final_third', 'pass_to_penalty_area',
'cross_to_penalty_area', 'progressive_pass']
for col in col_list:
    df_goals = df_all_player_pass.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    epl_big_joe.append((df_goals.loc[(df_goals.player_name == big_joe), 'percentile']).tolist()[0]/100)

# %%
df_all_player = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/dfb/individual-std-20182019.csv', header=1, names=player_std_col)
df_all_player_shot = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/dfb/individual-shots-20182019.csv', header=1, names=player_shot_col)
df_all_player_pass = pd.read_csv('/Users/Mai/Projects/ideas/open-data/fbref/individuals/dfb/individual-passing-20182019.csv', header=1, names=player_pass_col)

col_list = ['goals', 'assists', 'penalties', 'penalty_attempts',
 'xg', 'npxg', 'xa',]

# for col in col_list:
#     df_goals = df_all_player.loc[bool_filter, ['Player', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
#     num_player = df_goals.shape[0]
#     df_goals.loc[:, 'Player'] = df_goals.Player.str.split('\\').str[0]
#     df_goals['percentile'] = df_goals.index * (100/num_player)
#     lst_3.append((df_goals.loc[(df_goals.Player == 'Joelinton'), 'percentile']).tolist()[0]/100)

col_list = ['goals', 'shots', 'shot_on_target', 
'shot_on_target_percentage', 'goal_per_shot',
 'goal_per_shot_on_target',
  'npxg', 'npxg_per_shot',]
for col in col_list:
    df_goals = df_all_player_shot.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    dfb_big_joe.append((df_goals.loc[(df_goals.player_name == big_joe), 'percentile']).tolist()[0]/100)

col_list = ['key_passes', 'pass_to_final_third', 'pass_to_penalty_area',
'cross_to_penalty_area', 'progressive_pass']
for col in col_list:
    df_goals = df_all_player_pass.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    dfb_big_joe.append((df_goals.loc[(df_goals.player_name == big_joe), 'percentile']).tolist()[0]/100)

# %%
col_list = ['goals', 'assists', 'penalties', 'penalty_attempts',
 'xg', 'npxg', 'xa',]

# for col in col_list:
#     df_goals = df_all_player.loc[bool_filter, ['Player', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
#     num_player = df_goals.shape[0]
#     df_goals.loc[:, 'Player'] = df_goals.Player.str.split('\\').str[0]
#     df_goals['percentile'] = df_goals.index * (100/num_player)
#     lst_3.append((df_goals.loc[(df_goals.Player == 'Joelinton'), 'percentile']).tolist()[0]/100)

col_list = ['goals', 'shots', 'shot_on_target', 
'shot_on_target_percentage', 'goal_per_shot',
 'goal_per_shot_on_target',
  'npxg', 'npxg_per_shot',]
for col in col_list:
    df_goals = df_all_player_shot.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    epl_firmino.append((df_goals.loc[(df_goals.player_name == firmino), 'percentile']).tolist()[0]/100)

col_list = ['key_passes', 'pass_to_final_third', 'pass_to_penalty_area',
'cross_to_penalty_area', 'progressive_pass']
for col in col_list:
    df_goals = df_all_player_pass.loc[bool_filter, ['player_name', col]].sort_values(by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df_goals.shape[0]
    df_goals.loc[:, 'player_name'] = df_goals.player_name.str.split('\\').str[0]
    df_goals['percentile'] = df_goals.index * (100/num_player)
    epl_firmino.append((df_goals.loc[(df_goals.player_name == firmino), 'percentile']).tolist()[0]/100)

# %%
N = 13
data = [0]
title = 'Joelinton Stats Comparison - Newcastle Utd. 19/20 vs. Hoffenheim 18/19'
theta = radar_factory(N, 'circle')
fig, axes = plt.subplots(figsize=(9, 9), nrows=1, ncols=1,
                             subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
for ax, _ in zip([axes], data):
    # ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8])
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=360)
    ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(data, 'r'):
        ax.plot(theta, dfb_big_joe, color='#1C63B7')
        ax.fill(theta, dfb_big_joe, facecolor='#1C63B7', alpha=0.25)
        ax.plot(theta, epl_big_joe, color='#241F20')
        ax.fill(theta, epl_big_joe , facecolor='#241F20', alpha=0.25)
        ax.scatter([0] * 11, np.arange(0, 1.1, 0.1), s=1)
    ax.set_varlabels(['Goals', 'Shots', 'Shot on Target', 
'% Shot on Target', 'Goal/Shot',
 'Goal/Shot on Target', 'Non-Penalty xG', 'Non-Penalty xG/Shot',
 'Key Pass', 'Pass to Final Third', 'Pass to Penalty Area',
'Cross to Penalty Area', 'Progressvie Pass'])

labels = ('Joelinton - Newcastle Utd.', 'Joelinton - Hoffenheim')
legend = ax.legend(labels, loc=(0.9, .95),
                   labelspacing=0.1, fontsize='medium')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: Statsbomb vis FBRef', color='#555555')
plt.savefig('bigjoe_nufc_hoff_comparison.jpg')
plt.show()

# %%
N = 13
data = [0]
title = 'Player Stats: Joelinton vs Roberto Firmino'
theta = radar_factory(N, 'circle')
fig, axes = plt.subplots(figsize=(9, 9), nrows=1, ncols=1,
                             subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
for ax, _ in zip([axes], data):
    # ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8])
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=360)
    ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1),
                 horizontalalignment='center', verticalalignment='center')
    for d, color in zip(data, 'r'):
        ax.plot(theta, epl_firmino, color='#C8102E')
        ax.fill(theta, epl_firmino, facecolor='#C8102E', alpha=0.25)
        ax.plot(theta, epl_big_joe, color='#241F20')
        ax.fill(theta, epl_big_joe , facecolor='#241F20', alpha=0.25)
        ax.scatter([0] * 11, np.arange(0, 1.1, 0.1), s=1)
    ax.set_varlabels(['Goals', 'Shots', 'Shot on Target', 
'% Shot on Target', 'Goal/Shot',
 'Goal/Shot on Target', 'Non-Penalty xG', 'Non-Penalty xG/Shot',
 'Key Pass', 'Pass to Final Third', 'Pass to Penalty Area',
'Cross to Penalty Area', 'Progressvie Pass'])

labels = ('R. Firmino', 'Joelinton')
legend = ax.legend(labels, loc=(0.9, .95),
                   labelspacing=0.1, fontsize='medium')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: Statsbomb via FBRef', color='#555555')
plt.savefig('bigjoe_firmino_comparison.jpg')
plt.show()

# %%
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
fig, ax = pitch.draw()

# %%
matplotsoccer.field("white",figsize=12, show=False)
plt.vlines(35, ymin=0, ymax=68, ls='--')
plt.vlines(70, ymin=0, ymax=68, ls='--')
plt.vlines(105, ymin=0, ymax=68, ls='--')
plt.axis("off")
plt.show()

# %%
