# %%
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as clr
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.lines import Line2D

plt.style.use('ggplot')

color_map = clr.LinearSegmentedColormap.from_list(
    "intensity", [(0.0, '#EAE2B7'),
                #  (0.25, '#8080FF'),
                #  (0.5, '#FCBF49'),
                #  (0.75, '#FF8080'),
                 (1, '#D62828')])

# %%
csv_path = 'fbref'
csv_files = [os.path.join(csv_path, f) for f in os.listdir(csv_path)]

# %%
standard_col_name = ['squad', 'player_used', 'posession', 'match_played',
                    'starts', 'min_played', 'goals', 'assists', 
                    'penalties', 'penalty_attemps', 'yellow_cards', 'red_cards',
                    'goals-per-90', 'assists-per-90', 'goal-plus-assist-per-90',
                    'non-penalty-goals-per-90', 'non-penalty-goal-plus-assist-per-90',
                    'xG', 'npxG', 'xA', 'xG-per-90', 'xA-per-90', 'xG-plus-xA-per-90',
                    'npxG-per-90', 'npxG-plus-xA-per-90'
                    ]
df_std = pd.read_csv('fbref/teams/epltable-std-20192020.csv', header=1, names=standard_col_name)
df_std.columns

# %%
goalkeeper_col_name = ['squad', 'keeper_used', 'match_played', 'starts', 'min_played',
                        'goal-against', 'goal-against-per-90', 'shot-on-target-against',
                        'saves', 'percent-save', 'wins', 'draws', 'losses', 'clean-sheet', 'percent-clean-sheet',
                        'penalty-attemp', 'penalty-allow', 'penalty-saved', 'penalty-missed']

df_std_gk = pd.read_csv('fbref/teams/epltable-std-gk-20192020.csv', header=1, names=goalkeeper_col_name)
df_std_gk.columns
# %%
adv_gk_col_name = ['squad','keeper_used','number_of_90',
                    'goal-against', 'penalty-goal-against','freekick-goal-against', 'coner-goal-against', 'own-goal-against',
                    'post-shot-xG', 'post-shot-xG-to-shot-on-target', 'post-shot-xG-diff','post-shot-xG-diff-per-90',
                   'launch-complete', 'launch-attempt', 'percent-launch-complete',
                   'pass-attempt','throws', 'percent-launch', 'avg-pass-length',
                   'goal-kick-attempt', 'percent-of-goal-kick-launch', 'avg-goal-kick-length',
                   'opponent-cross', 'opponent-cross-stopped', 'percent-opponent-cross-stopped',
                   'action-outside-penalty-area', 'percent-action-outside-penalty-area', 'average-distance-action-outside-penalty-area']

df_adv_gk = pd.read_csv('fbref/teams/epltable-adv-gk-20192020.csv', header=1, names=adv_gk_col_name)
df_adv_gk.columns

# %%
shot_col_name = ['squad', 'player_used', 'goal-scored', 'penalty-scored',
                  'penalty-attempted', 'total-shots', 'shot-on-target', 'freekicks',
                  'percent-shot-on-target', 'shot-per-90', 'shot-on-target-per-90',
                  'goal-per-shot', 'goal-per-shot-on-target', 'xG', 'npxG', 'npxG-per-shot',
                  'goals-xG-diff', 'np-goal-npxG-diff']

df_shot = pd.read_csv('fbref/teams/epltable-shot-20192020.csv', header=1, names=shot_col_name)
df_shot.columns

# %%
df_gk = df_std_gk.merge(df_adv_gk.loc[:, ['squad', 'penalty-goal-against', 'freekick-goal-against',
                                  'coner-goal-against','own-goal-against',
                                  'post-shot-xG']],
                left_on='squad', right_on='squad')

df_overall = df_std.merge(df_shot, left_on='squad', right_on='squad')
df_overall.columns

# %%
club_crest_path = 'english-club-icons/epl/2019-2020'
club_crest_path = [os.path.join(club_crest_path, file) for file in sorted(os.listdir(club_crest_path)) if not file.startswith('.')]
# 2019-2020
colours = ['#DB0007', '#95BFE5', '#DA291C', '#0057B8',
           '#6C1D45', '#034694', '#1B458F', '#003399',
           '#003090', '#C8102E', '#6CABDD', '#DA291C',
           '#241F20', '#FFF200', '#EE2737', '#D71920',
           '#FFFFFF', '#FBEE23', '#7A263A', '#FDB913']
# 2019-2020
accents = ['#9C824A', '#670E36', '#000000', '#FFCD00',
           '#99D6EA', '#D1D3D4', '#C4122E', '#FFFFFF',
           '#FDBE11', '#00B2A9', '#FFC659', '#FBE122',
           '#BBBCBC', '#00A650', '#0D171A', '#00AEEF',
           '#132257', '#ED2127', '#1BB1E7', '#231F20']

values = zip(club_crest_path, colours, accents)
items = [dict(zip(('crest', 'colour', 'accent'), value)) for value in values]
team_identities = dict(zip(df_overall.squad.tolist(), items))

# %%
df_plot = pd.concat([df_overall.loc[:, ['squad', 'shot-on-target']],
            df_gk.loc[:, ['shot-on-target-against']]
            ], axis=1)
match_played = 38
x_median = df_plot.loc[:, 'shot-on-target'].median()
y_median = df_plot.loc[:, 'shot-on-target-against'].median()
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.scatter(df_plot.iloc[:, 1]/match_played, df_plot.iloc[:, 2]/match_played, s=1)
for idx, row in df_plot.iterrows():
    crest_path = team_identities[(row.iloc[0])]['crest']
    ab = AnnotationBbox(OffsetImage(plt.imread(crest_path), zoom=0.4,
                                    interpolation='bilinear'),
                        (row.iloc[1]/match_played, row.iloc[2]/match_played),
                        frameon=False)
    ax.add_artist(ab)

ax.axvline(x=x_median/match_played, ls='--', lw='1', color='#3a164f')
ax.axhline(y=y_median/match_played, ls='--', lw='1', color='#3a164f')
ax.set_title('Actual Performance, EPL 2019/2020',
              color='#555555', fontweight='bold')
ax.set_xlabel('Shot per match')
ax.set_ylabel('Shot faced per match')
ax.set_xticks(np.arange(2.5, 7, 0.5))
ax.set_yticks(np.arange(2.5, 6, 0.5))
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', label='League Median')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.03, 'data: fbref & statsbomb', color='#555555')
plt.show()

# %%
df_plot = pd.concat([df_overall.loc[:, ['squad', 'npxG_x']],
            df_gk.loc[:, ['post-shot-xG']]
            ], axis=1)
match_played = 38
x_median = df_plot.loc[:, 'npxG_x'].median()
y_median = df_plot.loc[:, 'post-shot-xG'].median()
fig = plt.figure(figsize=(16,9), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.scatter(df_plot.iloc[:, 1]/match_played, df_plot.iloc[:, 2]/match_played, s=1)
for idx, row in df_plot.iterrows():
    crest_path = team_identities[(row.iloc[0])]['crest']
    ab = AnnotationBbox(OffsetImage(plt.imread(crest_path), zoom=0.4,
                                    interpolation='bilinear'),
                        (row.iloc[1]/match_played, row.iloc[2]/match_played),
                        frameon=False)
    ax.add_artist(ab)

ax.axvline(x=x_median/match_played, ls='--', lw='1', color='#3a164f')
ax.axhline(y=y_median/match_played, ls='--', lw='1', color='#3a164f')
ax.set_title('Overall Performance, EPL 2019/2020',
              color='#555555', fontweight='bold')
ax.set_xlabel('Chance quality (xG)')
ax.set_ylabel('Chance quality faced (post-shot-xG)')
# ax.set_xticks(np.arange(2.5, 7, 0.5))
# ax.set_yticks(np.arange(2.5, 6, 0.5))
ax.annotate('', xy=(0.8, 0.82), xytext=(0.8, 1.02), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '->', 'color':'#555555', 'linewidth':1.5})
# ax.text(2.58, 2.18, 'Conceded Easily', rotation = 90, rotation_mode="anchor")
ax.annotate('', xy=(2.0, 1.8), xytext=(2.2, 1.8), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '<-', 'color':'#555555', 'linewidth':1.5})
# ax.text(4.83, 2.13, 'Defensive Minded', rotation = 0, rotation_mode="anchor")
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', label='League Median')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.895, 0.003, 'created by @bkktimber', color='#555555')
plt.figtext(0.895, 0.017, 'data: fbref & statsbomb', color='#555555')
# plt.savefig('20192020_EPL_xg-xga.jpg')
plt.show()

# %%
df_plot = df_overall.loc[:, ['squad', 'total-shots', 'goals']]
df_plot['shot-per-goal'] = df_plot.loc[:, 'total-shots']/df_plot.loc[:, 'goals']
match_played = 38
x_median = df_plot.loc[:, 'total-shots'].median()
y_median = df_plot.loc[:, 'shot-per-goal'].median()
fig = plt.figure(figsize=(16,9), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.scatter(df_plot.iloc[:, 1]/match_played, df_plot.iloc[:, 3], s=1)
for idx, row in df_plot.iterrows():
    crest_path = team_identities[(row.iloc[0])]['crest']
    ab = AnnotationBbox(OffsetImage(plt.imread(crest_path), zoom=0.5,
                                    interpolation='bilinear'),
                        (row.iloc[1]/match_played, row.iloc[3]),
                        frameon=False)
    ax.add_artist(ab)

ax.axvline(x=x_median/match_played, ls='--', lw='1', color='#3a164f')
ax.axhline(y=y_median, ls='--', lw='1', color='#3a164f')
ax.set_title('Attack Effectiveness, EPL 2019/2020',
              color='#555555', fontweight='bold')
ax.set_xlabel('Shots taken per match')
ax.set_ylabel('Shot per goal scored')
ax.set_xticks(np.arange(9, 21, 1))
ax.set_yticks(np.arange(7, 18, 1))
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', label='League Median')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.03, 'data: fbref & statsbomb', color='#555555')
plt.show()

# %%
df_plot = df_gk.loc[:, ['squad', 'shot-on-target-against', 'goal-against']]
df_plot['shot-per-goal'] = df_plot.loc[:, 'shot-on-target-against']/df_plot.loc[:, 'goal-against']
match_played = 38
x_median = df_plot.loc[:, 'shot-on-target-against'].median()
y_median = df_plot.loc[:, 'shot-per-goal'].median()
fig = plt.figure(figsize=(16,9), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.scatter(df_plot.iloc[:, 1]/match_played, df_plot.iloc[:, 3], s=1)
for idx, row in df_plot.iterrows():
    crest_path = team_identities[(row.iloc[0])]['crest']
    ab = AnnotationBbox(OffsetImage(plt.imread(crest_path), zoom=0.6,
                                    interpolation='bilinear'),
                        (row.iloc[1]/match_played, row.iloc[3]),
                        frameon=False)
    ax.add_artist(ab)

ax.axvline(x=x_median/match_played, ls='--', lw='1', color='#3a164f')
ax.axhline(y=y_median, ls='--', lw='1', color='#3a164f')
ax.set_title('Defense Efficency, EPL 2019/2020',
              color='#555555', fontweight='bold')
ax.set_xlabel('Shots faced per match')
ax.set_ylabel('Shot per goal scored')
ax.set_xticks(np.arange(2.5, 6, 0.5))
ax.set_yticks(np.arange(2, 5, 0.5))
ax.annotate('', xy=(2.6, 2.1), xytext=(2.6, 2.9), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '->', 'color':'#555555', 'linewidth':1.5})
ax.text(2.58, 2.18, 'Conceded Easily', rotation = 90, rotation_mode="anchor")
ax.annotate('', xy=(4.5, 2.1), xytext=(5.4, 2.1), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '<-', 'color':'#555555', 'linewidth':1.5})
ax.text(4.83, 2.13, 'Defensive Minded', rotation = 0, rotation_mode="anchor")
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', label='League Median')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.895, 0.003, 'created by @bkktimber', color='#555555')
plt.figtext(0.895, 0.017, 'data: fbref & statsbomb', color='#555555')
plt.savefig('defensive-efficency.jpg')
plt.show()

# %%
individua_stg_gk_col = ['rank', 'player', 'national', 'position', 'squad', 
                        'age', 'born', 'match-played', 'match-started', 'minute-played',
                        'goal-against', 'goal-against-per-90', 'shot-on-target-against', 'saves',
                        'percent-save', 'win', 'draw', 'loss', 'clean-sheet', 'percent-clean-sheet',
                        'pk-attempted', 'pk-allowed', 'pk-saved', 'pk-missed', 'match-report']
df_individual_gk = pd.read_csv('fbref/individuals/individual-std-gk-20192020.csv', header=1, names=individua_stg_gk_col)
# %%
df_plot = df_individual_gk.loc[:, ['player', 'squad', 'minute-played', 'goal-against', 'saves', 'percent-save', 'goal-against-per-90', 'pk-attempted']]
df_plot['save-per-90'] = df_plot['saves'] / (df_plot['minute-played']/90)
df_plot = df_plot[df_plot['minute-played'] >= 1807]
vline_value = df_plot['save-per-90'].mean()

fig = plt.figure(figsize=(16, 9), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ytick_labels = []
for idx, row in df_plot.sort_values(by='percent-save').iterrows():
    team_identity = team_identities[row.iloc[1]]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[0].split('\\')[0]
    num_save = row.iloc[-1]
    if player == 'Martin Dúbravka':
        ax.barh(player, num_save, color=team_color,
                edgecolor=team_accent, linewidth=1)
    else:
        ax.barh(player, num_save, color=team_color,
        edgecolor=team_accent, linewidth=1,
        alpha=0.9)
    label = f"{player} ({(row.iloc[5] * 100):.2f}%)"
    ytick_labels.append(label)
ax.axvline(vline_value, lw=1, ls='--', color='#3a164f')
ax.set_title('GK Saves Ranked by Save Percentage EPL 2019/2020', loc='center',
              color='#555555', fontweight='bold')
ax.set_xlabel('Saves')
ax.set_xticks(np.arange(0, 4, 0.5))
ax.set_yticklabels(ytick_labels)
ax.get_yticklabels()[9].set_weight("bold")
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', 
                      label=f'League Average: {int(vline_value)}')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.05),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.895, 0.003, 'created by @bkktimber', color='#555555')
plt.figtext(0.895, 0.017, 'data: fbref & statsbomb', color='#555555')
plt.savefig('individual-gk-saves-per-90.jpg')
plt.show()

# %%
df_plot = df_overall.loc[:, ['squad', 'goals-per-90', 'xG-per-90']]
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ci = 0.143912
ax = fig.add_subplot(spec[0,0])
ax.plot(np.arange(0, 4, 1), np.arange(0, 4, 1), ls='--', color='b')
ax.fill_between(np.arange(0, 4, 1),
                (np.arange(0, 4, 1) - ci),
                (np.arange(0, 4, 1) + ci),
                color='b', alpha=0.3)
for idx, row in df_plot.iterrows():
    team = row.iloc[0]
    team_identity = team_identities[team]
    color = team_identity['colour']
    accent = team_identity['accent']
    xg = row.iloc[2]
    goals = row.iloc[1]
    ax.scatter(xg, goals, color=color, edgecolor=accent,
                s=80)
    ax.annotate(team, (xg, goals))
plt.show()


# %%
def_act_col_name = ['squad', 'num_player', 'tackle_attempt', 'tackle_won',
                    'tackle_def_3rd', 'tackle_mid_3rd', 'tackle_att_3rd',
                    'tackle_v_dribbles_won', 'tackle_v_dribbles_attempt', 'tackle_v_dribbles_percent', 'dribbled_past',
                    'pressure', 'pressure_success', 'pressure_percentage',
                    'pressure_def_3rd', 'pressure_mid_3rd', 'pressure_att_3rd',
                    'blocks', 'block_shots', 'shot_saved', 'block_pass',
                    'interception', 'clearance', 'error']
df_def_act = pd.read_csv('fbref/teams/epltable-def_action-20192020.csv', header=1, names=def_act_col_name)
df_def_act.columns

# %%
df_league_table = pd.read_csv('fbref/teams/epltable-league-table-20192020.csv', header=1).iloc[:, :2]
df_league_table.columns = ['rank', 'squad']

# %%

# %%
df_plot = df_def_act.loc[:, ['squad', 'pressure', 'pressure_success', 'pressure_def_3rd', 'pressure_mid_3rd', 'pressure_att_3rd']]
df_plot = df_plot.merge(df_league_table, left_on='squad', right_on='squad')
p_mean = df_plot.loc[:, 'pressure'].mean()
p_def_mean = df_plot.loc[:, 'pressure_def_3rd'].mean()
p_mid_mean = df_plot.loc[:, 'pressure_mid_3rd'].mean()
p_atk_mean = df_plot.loc[:, 'pressure_att_3rd'].mean()
data_normalizer = clr.Normalize(vmin=-0.1, vmax=0.1)
fig = plt.figure(figsize=(8, 6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])

for idx, row in df_plot.sort_values(by='rank', ascending=False).iterrows():
    team = row.iloc[0]
    team_identity = team_identities[team]
    color = team_identity['colour']
    accent = team_identity['accent']
    p_total = row.iloc[1]
    p_def = (row.iloc[3]/p_total) - (p_def_mean/p_mean)
    p_mid = row.iloc[4]/p_total - (p_mid_mean/p_mean)
    p_atk = row.iloc[5]/p_total - (p_atk_mean/p_mean)
    ax.barh(team, 1, color=color_map(data_normalizer(p_def)),
            edgecolor='k')
    ax.barh(team, 1, color=color_map(data_normalizer(p_mid)),
            edgecolor='k', left=1)
    ax.barh(team, 1, color=color_map(data_normalizer(p_atk)),
            edgecolor='k', left=2)
    ax.annotate(f'{(p_def * 100):.1f} %', (0.5, 20 - row.iloc[-1]),
                horizontalalignment='center', verticalalignment='center')
    ax.annotate(f'{(p_mid * 100):.1f} %', (1.5, 20 - row.iloc[-1]),
                horizontalalignment='center', verticalalignment='center')
    ax.annotate(f'{(p_atk * 100):.1f} %', (2.5, 20 - row.iloc[-1]),
                horizontalalignment='center', verticalalignment='center')
ax.set_title('Pressure Activity Compare to League Average \nRanked by League Position', loc='left',
              color='#555555', fontweight='bold')
ax.set_xlabel('Pitch Zones')
ax.set_xticklabels(['', 'Own Area', '', 'Middle', '', 'Opponent Area', ''])
ax.get_yticklabels()[7].set_weight("bold")
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: fbref & statsbomb', color='#555555')
plt.grid(False)
plt.show()
# %%

# %%
df_plot = df_overall.loc[:, ['squad', 'goals', 'penalties', 'npxG_x']]
df_plot['non-penalty_goals'] = df_overall.loc[:, 'goals'] - df_overall.loc[:, 'penalties']
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.plot(np.arange(20, 105, 5), np.arange(20, 105, 5), ls='--', color='#3a164f')

for idx, row in df_plot.iterrows():
    team = row.iloc[0]
    team_identity = team_identities[team]
    color = team_identity['colour']
    accent = team_identity['accent']
    xg = row.iloc[3]
    goals = row.iloc[-1]
    ax.scatter(xg, goals, color=color, edgecolor=accent,
                s=100)
    if team == 'Newcastle Utd':
        ax.annotate(team, (xg, goals))

ax.set_title('Attacking Performance', loc='left',
              color='#555555', fontweight='bold')
ax.set_xlabel('Non-Penalty xG')
ax.set_ylabel('Non-Penalty Goals')
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', 
                      label='Expected Performance')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: fbref & statsbomb', color='#555555')
plt.show()

# %%
individual_standard_col_name = ['rank', 'player', 'national', 'position',
                                'squad', 'age', 'born', 'match_played', 'match_started',
                                'min_played', 'goals', 'assists', 'penalties', 'penalty_attempt',
                                'yellow_card', 'red_card', 'goal-per-90', 'assist-per-90',
                                'g_and_a-per-90', 'non-pen-goal-per-90', 'g_and_a_non_pen-per-90',
                                'xG', 'npxG', 'xA', 'xG-per-90', 'xA-per-90', 'xG_and_xA-per-90',
                                'npxG-per-90', 'npxG_and_xA-per-90', 'matches']
df_individual_std = pd.read_csv('fbref/individuals/individual-std-20192020.csv', header=1, names=individual_standard_col_name, usecols=range(len(standard_col_name)))
team_name = 'Newcastle Utd'
df_nufc = df_individual_std.groupby(by='squad').get_group('Newcastle Utd')
df_plot = df_individual_std.copy()
df_plot = df_plot.loc[:, ['squad', 'player', 'min_played', 'goals', 'penalties', 'xG', 'npxG']]
df_total_goals = df_overall.loc[:, ['squad', 'goals', 'penalties']]
df_total_goals['total_goals'] = df_total_goals.loc[:, 'goals'] - df_total_goals.loc[:, 'penalties']
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.plot(np.arange(0, 23, 1), np.arange(0, 23, 1), ls='--', color='#3a164f')
for idx, row in df_plot.iterrows():
    team = row.iloc[0]
    team_identity = team_identities[team]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[1].split('\\')[0]
    min_played = row.iloc[1]
    goals = row.iloc[3] - row.iloc[4]
    total = df_total_goals[df_total_goals.squad == team].loc[:, 'total_goals']
    xg = row.iloc[6]
    contribution = float(goals/total)
    if team in ['Manchester Utd']:
        ax.scatter(xg, goals, color=team_color, edgecolor=team_accent,
        alpha=0.4, s=int(4000 * contribution))
        if row.goals > 5:
            ax.annotate(row.player.split('\\')[0], (xg, goals))
    else:
        ax.scatter(xg, goals, color='white', edgecolor='black',
        alpha=0.2, s=int(4000 * contribution))

for idx, row in df_nufc.iterrows():
    team = team_name
    team_identity = team_identities[team]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[1].split('\\')[0]
    min_played = row.iloc[9]
    goals = row.iloc[10] - row.iloc[12]
    total = df_total_goals[df_total_goals.squad == team].loc[:, 'total_goals']
    xg = row.iloc[-3]
    contribution = float(goals/total)
    ax.scatter(xg, goals, color='white', edgecolor='black',
    s=int(4000 * contribution), alpha=0.2)

ax.set_title('Goal Scoreres Performance', loc='left',
              color='#555555', fontweight='bold')
ax.set_xlabel('Non-Penalty xG')
ax.set_ylabel('Non-Penalty Goals')
ax.set_xticks(np.arange(0, 23, 2))
ax.set_yticks(np.arange(0, 23, 2))
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', 
                      label=f'Expected Performance')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: fbref & statsbomb', color='#555555')
plt.show()

# %%
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.plot(np.arange(0, 8, 1), np.arange(0, 8, 1), ls='--', color='#3a164f')
for idx, row in df_nufc.iterrows():
    team = team_name
    team_identity = team_identities[team]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[1].split('\\')[0]
    min_played = row.iloc[9]
    goals = row.iloc[10] - row.iloc[12]
    total = df_total_goals[df_total_goals.squad == team].loc[:, 'total_goals']
    xg = row.iloc[-3]
    contribution = float(goals/total)
    ax.scatter(xg, goals, color=team_color, edgecolor=team_accent,
    s=int(6000 * contribution))
    if (goals > 2) or (player == 'Joelinton'):
        ax.annotate(player, (xg, goals * 1.08))

ax.set_title('Goal Scoreres Performance', loc='left',
              color='#555555', fontweight='bold')
ax.set_xlabel('Non-Penalty xG')
ax.set_ylabel('Non-Penalty Goals')
ax.set_xticks(np.arange(0, 8, 1))
ax.set_yticks(np.arange(0, 8, 1))
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', 
                      label=f'Expected Performance')]
plt.legend(handles=line_legend, bbox_to_anchor=(1.08, 1.06),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: fbref & statsbomb', color='#555555')
plt.show()
# %%
df_plot = df_individual_std.copy()
df_plot = df_plot.loc[:, ['squad', 'player', 'min_played', 'goals', 'penalties', 'xG', 'npxG']]
df_total_goals = df_overall.loc[:, ['squad', 'goals', 'penalties']]
df_total_goals['total_goals'] = df_total_goals.loc[:, 'goals'] - df_total_goals.loc[:, 'penalties']
fig = plt.figure(figsize=(8,6), constrained_layout=True)
spec = gridspec.GridSpec(ncols=1, nrows=1, figure=fig)
ax = fig.add_subplot(spec[0,0])
ax.plot(np.arange(0, 23, 1), np.arange(0, 23, 1), ls='--', color='#3a164f')
for idx, row in df_plot.iterrows():
    team = row.iloc[0]
    team_identity = team_identities[team]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[1].split('\\')[0]
    min_played = row.iloc[1]
    goals = row.iloc[3] - row.iloc[4]
    total = df_total_goals[df_total_goals.squad == team].loc[:, 'total_goals']
    xg = row.iloc[6]
    contribution = float(goals/total)
    if team in ['Norwich City', 'Watford', 'Crystal Palace']:
        ax.scatter(xg, goals, color='white', edgecolor='black',
        alpha=0.4, s=int(4000 * contribution))
    else:
        ax.scatter(xg, goals, color='white', edgecolor='black',
        alpha=0.2, s=int(4000 * contribution))

for idx, row in df_nufc.iterrows():
    team = team_name
    team_identity = team_identities[team]
    team_color = team_identity['colour']
    team_accent = team_identity['accent']
    player = row.iloc[1].split('\\')[0]
    min_played = row.iloc[9]
    goals = row.iloc[10] - row.iloc[12]
    total = df_total_goals[df_total_goals.squad == team].loc[:, 'total_goals']
    xg = row.iloc[-3]
    contribution = float(goals/total)
    ax.scatter(xg, goals, color=team_color, edgecolor=team_accent,
    s=int(4000 * contribution))

ax.set_title('Goal Scoreres Performance\nNEW v WAT/NOR/CRY', loc='left',
              color='#555555', fontweight='bold')
ax.set_xlabel('Non-Penalty xG')
ax.set_ylabel('Non-Penalty Goals')
ax.set_xticks(np.arange(0, 23, 2))
ax.set_yticks(np.arange(0, 23, 2))
line_legend = [Line2D([0], [0], color='#3a164f',
                      lw=1, ls='--', 
                      label=f'Expected Performance')]
plt.legend(handles=line_legend, bbox_to_anchor=(1, 1.07),
            framealpha=0.1, edgecolor='#555555')
plt.figtext(0.78, 0.001, 'created by @bkktimber', color='#555555')
plt.figtext(0.78, 0.023, 'data: fbref & statsbomb', color='#555555')
plt.show()

# %%
