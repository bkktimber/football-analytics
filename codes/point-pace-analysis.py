# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs

plt.style.use('ggplot')
# %%
base_path = '/Users/Mai/Projects/football-analytics/data/fixtures'
seasons = ['20202021',
           '20192020', '20182019', '20172018', '20162017', '20152016',
           '20142015', '20132014', '20122013', '20112012', '20102011']
current_season = seasons[0]
previous_seasons = seasons[1:]
competition = 'epl'
team_groups = {'winner': (0, 1),
               'qualified': (1, 7),
               'relageted': (17, 20)}
winners = pd.DataFrame()
qualifiers = pd.DataFrame()
relagators = pd.DataFrame()

# %%
for season in previous_seasons:
    target_filename = os.path.join(base_path, season,
                                   f'{competition}_fixture.pkl')
    data_df = pd.read_pickle(target_filename)
    data_df.head()

    data_slices = data_df.loc[:, ['gameweek', 'home_team', 'score_home', 'away_team', 'score_away']]
    data_slices['home_team_goal_diff'] = data_slices.score_home - data_slices.score_away
    data_slices['results'] = 'D'
    data_slices.loc[data_slices['home_team_goal_diff'] > 0, 'results'] = 'W'
    data_slices.loc[data_slices['home_team_goal_diff'] < 0, 'results'] = 'L'

    team_dict = dict(zip(pd.unique(data_slices.home_team.sort_values()).tolist(),
                         [0] * pd.unique(data_slices.home_team.sort_values()).shape[0]))
    groupped = data_slices.groupby('gameweek')

    league_table_dict = {}
    league_gd_dict = {}
    for grp, frame in groupped:
        gw_point_dict = team_dict.copy()
        gw_goals_diff_dict = team_dict.copy()
        for _, row in frame.iterrows():
            if row.results == 'W':
                gw_point_dict[row.home_team] = 3
            elif row.results == 'L':
                gw_point_dict[row.away_team] = 3
            else:
                gw_point_dict[row.home_team] = 1
                gw_point_dict[row.away_team] = 1
            gw_goals_diff_dict[row.home_team] = row.home_team_goal_diff
            gw_goals_diff_dict[row.away_team] = -1 * row.home_team_goal_diff
        league_table_dict[grp] = gw_point_dict
        league_gd_dict[grp] = gw_goals_diff_dict

    league_table_points = pd.DataFrame(league_table_dict)
    league_table_gd = pd.DataFrame(league_gd_dict)
    league_table_points.reset_index(inplace=True)
    melted = pd.melt(league_table_points,
                    id_vars=['index'],
                    value_vars=range(1, 39, 1))
    season_points_table = melted.groupby('index').agg({'variable': max,
                                                        'value': sum})
    season_points_table.reset_index(inplace=True)
    
    league_table_gd.reset_index(inplace=True)
    melted = pd.melt(league_table_gd,
                    id_vars=['index'],
                    value_vars=range(1, 39, 1))
    season_gd_table = melted.groupby('index').agg({'variable': max,
                                                        'value': sum})
    season_gd_table.reset_index(inplace=True)
    season_table = pd.merge(season_points_table,
                            season_gd_table,
                            on=['index', 'variable'],
                            how='left')
    season_table.sort_values(by=['value_x', 'value_y'],
                            ascending=False,
                            inplace=True)
    season_table.columns = ['team', 'match_play', 'points', 'gd']
    season_table['season'] = season
    season_table = season_table.reset_index(drop=True)
    col_names = ['team', 'season', 'points', 'gd'] + list(range(1, 39, 1))
    for k, (u, l) in team_groups.items():
        selected = season_table.iloc[u:l ,:]
        selected = pd.merge(selected,
                            league_table_points,
                            left_on='team', right_on='index',
                            how='left')
        selected = selected.loc[:, col_names]
        if k == 'winner':
            winners = winners.append(selected, ignore_index=True)
        elif k == 'qualified':
            qualifiers = qualifiers.append(selected, ignore_index=True)
        else:
            relagators = relagators.append(selected, ignore_index=True)
# %%
season = '20202021'
target_filename = os.path.join(base_path, season,
                               f'{competition}_fixture.pkl')
data_df = pd.read_pickle(target_filename)
data_df.head()
data_slices = data_df.loc[:, ['gameweek', 'home_team', 'score_home', 'away_team', 'score_away']]
data_slices['home_team_goal_diff'] = data_slices.score_home - data_slices.score_away
data_slices['results'] = 'D'
data_slices.loc[data_slices['home_team_goal_diff'] > 0, 'results'] = 'W'
data_slices.loc[data_slices['home_team_goal_diff'] < 0, 'results'] = 'L'
team_dict = dict(zip(pd.unique(data_slices.home_team.sort_values()).tolist(),
                     [0] * pd.unique(data_slices.home_team.sort_values()).shape[0]))
groupped = data_slices.groupby('gameweek')
league_table_dict = {}
league_gd_dict = {}
for grp, frame in groupped:
    gw_point_dict = team_dict.copy()
    gw_goals_diff_dict = team_dict.copy()
    for _, row in frame.iterrows():
        if row.results == 'W':
            gw_point_dict[row.home_team] = 3
        elif row.results == 'L':
            gw_point_dict[row.away_team] = 3
        else:
            gw_point_dict[row.home_team] = 1
            gw_point_dict[row.away_team] = 1
        gw_goals_diff_dict[row.home_team] = row.home_team_goal_diff
        gw_goals_diff_dict[row.away_team] = -1 * row.home_team_goal_diff
    league_table_dict[grp] = gw_point_dict
    league_gd_dict[grp] = gw_goals_diff_dict
league_table_points = pd.DataFrame(league_table_dict)
league_table_gd = pd.DataFrame(league_gd_dict)
league_table_points.reset_index(inplace=True)
melted = pd.melt(league_table_points,
                id_vars=['index'],
                value_vars=range(1, 18, 1))
season_points_table = melted.groupby('index').agg({'variable': max,
                                                    'value': sum})
season_points_table.reset_index(inplace=True)

league_table_gd.reset_index(inplace=True)
melted = pd.melt(league_table_gd,
                id_vars=['index'],
                value_vars=range(1, 18, 1))
season_gd_table = melted.groupby('index').agg({'variable': max,
                                                    'value': sum})
season_gd_table.reset_index(inplace=True)
season_table = pd.merge(season_points_table,
                        season_gd_table,
                        on=['index', 'variable'],
                        how='left')
season_table.sort_values(by=['value_x', 'value_y'],
                        ascending=False,
                        inplace=True)
season_table.columns = ['team', 'match_play', 'points', 'gd']
season_table['season'] = season
season_table = season_table.reset_index(drop=True)
col_names = ['team', 'season', 'points', 'gd'] + list(range(1, 18, 1))
selected = pd.merge(season_table,
                    league_table_points,
                    left_on='team', right_on='index',
                    how='left')
selected = selected.loc[:, col_names]
    # if k == 'winner':
    #     winners = winners.append(selected, ignore_index=True)
    # elif k == 'qualified':
    #     qualifiers = qualifiers.append(selected, ignore_index=True)
    # else:
    #     relagators = relagators.append(selected, ignore_index=True)
# %%
plt.figure(figsize=(16, 9), constrained_layout=True, dpi=250)
plt.rc('axes', titlesize=14)
plt.rc('axes', labelsize=14)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
# plt.plot(np.arange(1, 39, 1), relagators.iloc[:, -38:].T.cumsum().mean(axis=1), ls='--', c='k')
plt.plot(np.arange(1, 39, 1), thrs_drop, ls=(0, (3, 1, 1, 1)), c='#c00')
# plt.plot(np.arange(1, 39, 1), relagators.iloc[:, -38:].T.cumsum().mean(axis=1)-5.814073, ls='dotted', c='k')
plt.fill_between(np.arange(1, 39, 1), 0, thrs_drop, facecolor='#c00', alpha=0.15)
for i in range(relagators.shape[0]):
    if i == 12:
        plt.scatter(np.arange(1, 39, 1), relagators.iloc[:, -38:].T.cumsum().iloc[:, i], alpha=0.75, c='#241F20')
    else:
        plt.scatter(np.arange(1, 39, 1), relagators.iloc[:, -38:].T.cumsum().iloc[:, i], alpha=0.15, c='grey')

# for i in range(qualifiers.shape[0]):
#     plt.scatter(np.arange(1, 39, 1), qualifiers.iloc[:, -38:].T.cumsum().iloc[:, i])
plt.plot(np.arange(1, 39, 1), qualifiers.iloc[:, -38:].T.cumsum().mean(axis=1), ls='--', c='#E85C24', lw=2, alpha=0.5)
# plt.plot(np.arange(1, 39, 1), winners.iloc[:, -38:].T.cumsum().mean(axis=1), ls='--', c='k')

plt.plot(np.arange(1, 18, 1), selected[selected.team == 'Newcastle Utd'].iloc[:, -17:].T.cumsum(),
         color='#241F20', lw=4)
plt.plot(np.arange(1, 39, 1), pjt, color='#241F20', ls=(0, (1, 1)), lw=3)

plt.axhline(39, c='#c00', lw=3, ls=(0, (1, 10)))
plt.axvline(17, c='#3d195b', lw=3)
plt.xticks(np.arange(1, 39, 1))
plt.yticks(np.arange(0, 101, 5))
plt.xlabel('Game Week')
plt.ylabel('Points')
plt.xlim([0.5, 38.5])
plt.ylim([0, 60])
plt.grid(axis='x')

plt.text(26, 50, "Europe Competitions: 1.82 Points/match",
        ha="center", va="center", rotation=32, size=12,
        color='#E85C24', weight='bold')

plt.text(23, 28, "Newcastle Utd. : 1.12 Points/match",
        ha="center", va="center", rotation=21, size=12,
        color='#241F20', weight='bold')

plt.text(2, 34, "Most Points Got Relagated: 39 Points\nBirmingham City & Blackpool 2009/2010",
        ha="left", va="baseline", rotation=0, size=12,
        color='#c00', weight='bold')

plt.text(36.5, 18, "90% Drop Zone!",
        ha="center", va="center", rotation=270, size=15,
        color='#c00', weight='bold')

plt.text(17.5, 55, "Today",
         ha="center", va="center", c='#3d195b', size=15, rotation=270)

plt.title('Will Newcastle Utd. survies?: Point Pace Analysis', weight='bold')
plt.savefig('/Users/Mai/Projects/football-analytics/charts/20210111_nufc_half_season_point_pace.jpg')
plt.show()
# %%
plt.rc('axes', titlesize=12)
plt.rc('axes', labelsize=12)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)