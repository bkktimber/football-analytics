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

from radar_factory import radar_factory

plt.style.use('ggplot')

color_map = clr.LinearSegmentedColormap.from_list(
    "intensity",
    [
        (0.0, '#EAE2B7'),
        #  (0.25, '#8080FF'),
        #  (0.5, '#FCBF49'),
        #  (0.75, '#FF8080'),
        (1, '#D62828')
    ])
# %%
player_std_col = [
    'rank', 'player_name', 'nationality', 'position', 'squad', 'age',
    'year_of_birth', 'match_played', 'match_started', 'minute_played', 'goals',
    'assists', 'penalties', 'penalty_attempts', 'yellow_card', 'red_card',
    'goals_per_90', 'assists_per_90', 'goal_plus_assist_per_90',
    'goal_minus_penalty_per_90', 'goal_plus_assist_minus_penalty_per_90', 'xg',
    'npxg', 'xa', 'xg_per_90', 'xa_per_90', 'xg_plus_xa_per_90', 'npxg_per_90',
    'npxg_plus_xa_per_90', 'match_report'
]

player_shot_col = [
    'rank', 'player_name', 'nationality', 'position', 'squad', 'age',
    'year_of_birth', '90s', 'goals', 'penalties', 'penalty_attempts', 'shots',
    'shot_on_target', 'freekicks', 'shot_on_target_percentage', 'shot_per_90',
    'shot_on_target_per_90', 'goal_per_shot', 'goal_per_shot_on_target', 'xg',
    'npxg', 'npxg_per_shot', 'goal_minus_xg', 'np_goals_minus_npxg',
    'match_report'
]

player_pass_col = [
    'rank', 'player_name', 'nationality', 'position', 'squad', 'age',
    'year_of_birth', '90s', 'passes_completed', 'pass_attempts',
    'pass_complete_percentage', 'total_pass_distance',
    'progressive_pass_distance', 'short_passes_completed',
    'short_passes_attempts', 'short_pass_complete_percentage',
    'medium_passes_completed', 'medium_passes_attempts',
    'medium_pass_complete_percentage', 'long_passes_completed',
    'long_passes_attempts', 'long_pass_complete_percentage', 'assists', 'xa',
    'assists_minus_xa', 'key_passes', 'pass_to_final_third',
    'pass_to_penalty_area', 'cross_to_penalty_area', 'progressive_pass',
    'match_report'
]

player_def_col = [
    'rank', 'player_name', 'nationality', 'position', 'squad', 'age',
    'year_of_birth', '90s', 'tackles', 'tackle_won', 'tackles_in_def_third',
    'tackles_in_mid_third', 'tackles_in_atk_third', 'tackles_won_dribble',
    'tackle_attempts_dribble', 'tackle_dribble_percentage', 'dribble_passed',
    'pressure', 'pressure_success', 'pressure_percentage',
    'pressure_in_def_third', 'pressure_in_mid_third', 'pressure_in_atk_third',
    'blocks', 'shot_blocked', 'shot_saved', 'pass_blocks', 'interception',
    'clearance', 'error', 'match_report'
]

player_pos_col = [
    'rank', 'player_name', 'nationality', 'position', 'squad', 'age',
    'year_of_birth', '90s', 'touchs', 'touchs_in_def_pen',
    'touchs_in_def_third', 'touchs_in_mid_third', 'touchs_in_atk_third',
    'touchs_in_atk_pen', 'touches_live', 'dribble_success',
    'dribble_attemptps', 'dribble_percnetage', 'num_player_pass', 'nutmegs',
    'carries', 'total_distace', 'progressive_distance', 'receive_taget',
    'receive_success', 'receive_percnetage', 'miscontrolled', 'disposession',
    'match_report'
]

#  %%
df_all_player = pd.read_csv(
    '/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-std-20192020.csv',
    header=1,
    names=player_std_col)
df_all_player_shot = pd.read_csv(
    '/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-shots-20192020.csv',
    header=1,
    names=player_shot_col)
df_all_player_pass = pd.read_csv(
    '/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-passing-20192020.csv',
    header=1,
    names=player_pass_col)
df_all_player_def = pd.read_csv(
    '/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-defense-20192020.csv',
    header=1,
    names=player_def_col)
df_all_player_pos = pd.read_csv(
    '/Users/Mai/Projects/ideas/open-data/fbref/individuals/epl/individual-posession-20192020.csv',
    header=1,
    names=player_pos_col)

# %%
bool_min = (df_all_player.minute_played > df_all_player.minute_played.median())
bool_not_gk = (df_all_player.position != 'GK')
# bool_not_df = (df_all_player.position != 'DF')
bool_filter = (bool_not_gk)

rf = 'Ryan Fraser'
ih = 'Isaac Hayden'
js = 'Jonjo Shelvey'
ma = 'Miguel Almirón'
asm = 'Allan Saint-Maximin'

# %%
epl_rf = []
epl_ih = []
epl_js = []

col_list = [
    'xa', 'pass_complete_percentage', 'progressive_pass', 'key_passes',
    'tackle_won', 'pressure', 'pressure_success', 'blocks', 'interception'
]
p_col = 'player_name_pass'

_df = df_all_player_pass.join(df_all_player_def,
                              lsuffix='_pass',
                              rsuffix='_def')
for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_rf.append(
        (df.loc[(df.loc[:, p_col] == rf), 'percentile']).tolist()[0] / 100)

for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_ih.append(
        (df.loc[(df.loc[:, p_col] == ih), 'percentile']).tolist()[0] / 100)

for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_js.append(
        (df.loc[(df.loc[:, p_col] == js), 'percentile']).tolist()[0] / 100)

# %%
N = len(col_list)
data = [0]
title = f'Player Comparison: {rf} vs. NUFC\'s Central Midfielders \n EPL 2019/2020'
theta = radar_factory(N, 'circle')
fig, axes = plt.subplots(figsize=(9, 9),
                         nrows=1,
                         ncols=1,
                         subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
for ax, _ in zip([axes], data):
    # ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8])
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=360)
    ax.set_title(title,
                 weight='bold',
                 size='large',
                 position=(0.5, 1.1),
                 horizontalalignment='center',
                 verticalalignment='center')
    for d, color in zip(data, 'r'):
        ax.plot(theta, epl_ih, color='#241F20')
        ax.fill(theta, epl_ih, facecolor='#BBBCBC', alpha=0.25)
        ax.plot(theta, epl_js, color='#BBBCBC')
        ax.fill(theta, epl_js, facecolor='#241F20', alpha=0.25)
        ax.plot(theta, epl_rf, color='#99D6EA')
        ax.fill(theta, epl_rf, facecolor='#6C1D45', alpha=0.4)
        ax.scatter([0] * 11, np.arange(0, 1.1, 0.1), s=1)
    ax.set_varlabels([col.upper().replace('_', ' ') for col in col_list])

labels = (ih, js, rf)
legend = ax.legend(labels, loc=(0.9, .95), labelspacing=0.1, fontsize='medium')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: Statsbomb via FBRef', color='#555555')
plt.savefig('rf_ih_comparison.jpg')
plt.show()

# %%
epl_rf = []
epl_ma = []
epl_asm = []
col_list = [
    'xa',
    'assists',
    'pass_complete_percentage',
    'progressive_pass',
    'pass_to_final_third',
    'pass_to_penalty_area',
    'key_passes',
    'shot_on_target_percentage',
    'xg',
    'goals',
]
p_col = 'player_name_pass'

_df = df_all_player_pass.join(df_all_player_shot,
                              lsuffix='_pass',
                              rsuffix='_shot')
_df = _df.join(df_all_player_pos, rsuffix='_pos')
for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_rf.append(
        (df.loc[(df.loc[:, p_col] == rf), 'percentile']).tolist()[0] / 100)

for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_ma.append(
        (df.loc[(df.loc[:, p_col] == ma), 'percentile']).tolist()[0] / 100)

for col in col_list:
    df = _df.loc[bool_filter, [p_col, col]].sort_values(
        by=col, ascending=True).reset_index(drop=True, inplace=False)
    num_player = df.shape[0]
    df.loc[:, p_col] = df.loc[:, p_col].str.split('\\').str[0]
    df['percentile'] = df.index * (100 / num_player)
    epl_asm.append(
        (df.loc[(df.loc[:, p_col] == asm), 'percentile']).tolist()[0] / 100)
# %%
N = len(col_list)
data = [0]
title = f'Player Comparison: {rf} vs. NUFC\'s Attacking Midfielders\n EPL 2019/2020'
theta = radar_factory(N, 'circle')
fig, axes = plt.subplots(figsize=(9, 9),
                         nrows=1,
                         ncols=1,
                         subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
for ax, _ in zip([axes], data):
    # ax.set_rgrids([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,0.8])
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], angle=360)
    ax.set_title(title,
                 weight='bold',
                 size='large',
                 position=(0.5, 1.1),
                 horizontalalignment='center',
                 verticalalignment='center')
    for d, color in zip(data, 'r'):
        ax.plot(theta, epl_ma, color='#241F20')
        ax.fill(theta, epl_ma, facecolor='#BBBCBC', alpha=0.25)
        ax.plot(theta, epl_asm, color='#BBBCBC')
        ax.fill(theta, epl_asm, facecolor='#241F20', alpha=0.25)
        ax.plot(theta, epl_rf, color='#DA291C')
        ax.fill(theta, epl_rf, facecolor='#000000', alpha=0.4)
        ax.scatter([0] * 11, np.arange(0, 1.1, 0.1), s=1)
    ax.set_varlabels([col.upper().replace('_', ' ') for col in col_list])

labels = (ma, asm, rf)
legend = ax.legend(labels, loc=(0.9, .95), labelspacing=0.1, fontsize='medium')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: Statsbomb via FBRef', color='#555555')
plt.savefig('rf_ma_comparison.jpg')
plt.show()
# %%

# %%
