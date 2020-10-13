# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

plt.style.use('ggplot')

# %%
crest_dir = '/Users/Mai/Projects/football-analytics/resources/english-club-icons/epl/2020-2021'
nufc = 'Newcastle Utd'
df = pd.read_csv(
    '/Users/Mai/Projects/football-analytics/data/epl_fixture_20202021.csv')
nufc_fixtures = df[(df.home_team == nufc) | (df.away_team == nufc)]
nufc_fixtures['is_home'] = 'A'
nufc_fixtures.loc[nufc_fixtures.home_team == nufc, 'is_home'] = 'H'

finished_place = {
    'Liverpool': 1,
    'Manchester City': 2,
    'Manchester Utd': 3,
    'Chelsea': 4,
    'Leicester City': 5,
    'Tottenham': 6,
    'Wolves': 7,
    'Arsenal': 8,
    'Sheffield Utd': 9,
    'Burnley': 10,
    'Everton': 11,
    'Southampton': 12,
    'Newcastle Utd': 13,
    'Crystal Palace': 14,
    'Brighton': 15,
    'West Ham': 16,
    'Aston Villa': 17,
    'Leeds United': 18,
    'West Brom': 19,
    'Fulham': 20
}

season_mapping = {
    27: '1993-1994',
    28: '1994-1995',
    29: '1995-1996',
    31: '1996-1997',
    33: '1997-1998',
    35: '1998-1999',
    38: '1999-2000',
    47: '2000-2001',
    63: '2001-2002',
    84: '2002-2003',
    112: '2003-2004',
    146: '2004-2005',
    183: '2005-2006',
    229: '2006-2007',
    282: '2007-2008',
    338: '2008-2009',
    400: '2009-2010',
    467: '2010-2011',
    534: '2011-2012',
    602: '2012-2013',
    669: '2013-2014',
    733: '2014-2015',
    1467: '2015-2016',
    1526: '2016-2017',
    1631: '2017-2018',
    1889: '2018-2019',
    9999: '2019-2020',
}

season_order = dict([(v, idx)
                     for idx, (k, v) in enumerate(season_mapping.items())])
# %%
team_names = sorted(set(nufc_fixtures.home_team.tolist()))
team_crests = sorted(set(os.listdir(crest_dir)))
team_crest_mapping = dict([(n, os.path.join(crest_dir, p))
                           for n, p in zip(team_names, team_crests)])
# %%
opponentes = []
for idx, row in nufc_fixtures.iterrows():
    home = row.home_team
    away = row.away_team
    if home == nufc:
        opponentes.append(away)
    else:
        opponentes.append(home)
# %%
data = [finished_place[team] for team in opponentes]

# %%
result_path = '/Users/Mai/Projects/football-analytics/data/match_records/epl'
result_files = [os.path.join(result_path, f) for f in os.listdir(result_path)]

# %%
selected_cols = [
    'match_id', 'gameweek', 'home_team', 'score_home', 'score_away',
    'away_team'
]
results = []
for f in result_files:
    season_id = f.split('_')[-1][:-4]
    tmp_df = pd.read_csv(f).loc[:, selected_cols]
    tmp_df['season'] = season_mapping[int(season_id)]
    results.append(tmp_df)

f = '/Users/Mai/Projects/football-analytics/data/epl/20172018/fixtures.csv'
tmp_df = pd.read_csv(f).loc[:, selected_cols]
tmp_df['season'] = '2017-2018'
results.append(tmp_df)

f = '/Users/Mai/Projects/football-analytics/data/epl/20182019/fixtures.csv'
tmp_df = pd.read_csv(f).loc[:, selected_cols]
tmp_df['season'] = '2018-2019'
results.append(tmp_df)

f = '/Users/Mai/Projects/football-analytics/data/epl/20192020/fixtures.csv'
tmp_df = pd.read_csv(f).loc[:, selected_cols]
tmp_df['season'] = '2019-2020'
results.append(tmp_df)
# %%
results = pd.concat(results, ignore_index=True)

# %%
result_mapping = {'1': 'b', '0': 'k', '-1': 'r'}
plot = nufc_fixtures.reset_index(drop=True, inplace=False)
# fig = plt.figure(figsize=(16,9))
# for idx, row in plot.iterrows():
#     home_team = row.home_team
#     away_team = row.away_team
#     home_bool = (results.home_team == home_team)
#     away_bool = (results.away_team == away_team)
#     # tmp_df = results[(home_bool & away_team)]
#     tmp_df = results[((results.home_team == home_team) & (results.away_team == away_team))]
#     for i, r in tmp_df.iterrows():
#         result = '0'
#         season = r.season
#         home_score = r.score_home
#         away_score = r.score_away
#         if home_score > away_score:
#             if home_team == nufc:
#                 result = '1'
#             else:
#                 result = '-1'
#         elif home_score < away_score:
#             if away_team == nufc:
#                 result = '1'
#             else:
#                 result = '-1'
#         else:
#             pass
#         plt.scatter(x=idx, y=season_order[season],
#         c=result_mapping[result])

# plt.xticks(np.arange(38), opponentes, rotation=90)
# plt.yticks(list(season_order.values()), list(season_order.keys()))
# plt.show()
# %%
fig = plt.figure(figsize=(16, 9), constrained_layout=True)
spec = gridspec.GridSpec(figure=fig, nrows=10, ncols=38, wspace=0, hspace=0)

for idx, op in enumerate(opponentes):
    ax_crest = fig.add_subplot(spec[0, idx])
    im = Image.open(team_crest_mapping[op])
    im = im.resize((25, 25))
    ax_crest.imshow(im)
    ax_crest.axis('off')

ax_fixture = fig.add_subplot(spec[1, :])
x = np.array(data).reshape((1, 38))
ax_fixture.imshow(20 - x, cmap="Purples", alpha=0.85, origin="lower", vmin=0)
ax_fixture.set_yticklabels(['', nufc, ''], rotation=0, ha='right')
ax_fixture.set_xticks(np.arange(38))
# ax_fixture.set_xticklabels(opponentes, rotation=30, ha='center')
ax_fixture.xaxis.tick_top()
ax_fixture.axis('off')

im = Image.open(team_crest_mapping[nufc])
im = im.resize((40, 40))
imbox = OffsetImage(im)
ab = AnnotationBbox(imbox, (0.02, 0.8),
                    xycoords='figure fraction',
                    frameon=False)
ax_fixture.add_artist(ab)

for i, status in enumerate(nufc_fixtures.is_home.tolist()):
    ax_fixture.text(i,
                    0,
                    status,
                    ha="center",
                    va="center",
                    color="k",
                    fontweight='bold')
tmp = []
lst = []
plt.rcParams['axes.facecolor'] = '#f9f5e3'
ax_result = fig.add_subplot(spec[2:, :])
for idx, row in plot.iterrows():
    home_team = row.home_team
    away_team = row.away_team
    home_bool = (results.home_team == home_team)
    away_bool = (results.away_team == away_team)
    # tmp_df = results[(home_bool & away_team)]
    tmp_df = results[((results.home_team == home_team) &
                      (results.away_team == away_team))]
    total_result = []
    draw = 0
    win = 0
    lose = 0
    for i, r in tmp_df.iterrows():
        result = 1

        season = r.season
        if season in [
                '2010-2011',
                '2011-2012',
                '2012-2013',
                '2013-2014',
                '2014-2015',
                '2015-2016',
                '2016-2017',
                '2017-2018',
                '2018-2019',
                '2019-2020',
        ]:
            # if True:
            # if season in ['2017-2018','2018-2019','2019-2020',]:
            home_score = r.score_home
            away_score = r.score_away
            if home_score > away_score:
                if home_team == nufc:
                    result = 3
                    win += 1
                else:
                    result = 0
                    lose += 1
            elif home_score < away_score:
                if away_team == nufc:
                    result = 3
                    win += 1
                else:
                    result = 0
                    lose += 1
            else:
                draw += 1
            total_result.append(result)
    if len(total_result) == 0:
        num = 1
    else:
        num = len(total_result)
    lst.append([win / num, draw / num, lose / num])
    avg_score = sum(total_result) / num
    if lst[idx][0] >= 0.5:
        ax_result.scatter(
            x=idx,
            y=avg_score,
            c='#2a8635',
            s=160,
        )
    else:
        ax_result.scatter(x=idx, y=avg_score, c='#2a8635', s=160, alpha=0.3)
    tmp.append(avg_score)
ax_result.margins(0.01)
ax_result.set_xticks([1, 4.5, 8, 12.5, 18.5, 24, 28, 31.5, 35.5])
ax_result.grid(False)
months = [
    'September', 'October', 'November', 'December', 'January', 'Febuary',
    'March', 'April', 'May'
]
ax_result.set_xticklabels(months, fontweight='bold')
ax_result.set_yticklabels([0, 1, 2, 3], fontweight='bold')
ax_result.set_yticks(np.arange(4))
ax_result.set_ylim([-0.2, 3.2])
ax_result.set_ylabel(f'Average Points (last 10 seasons)', fontweight='bold')
# ax_result.set_yticks(list(season_order.values()))
# ax_result.set_yticklabels(list(season_order.keys()))

for _x in [2.5, 6.5, 9.5, 15.5, 21.5, 26.5, 29.5, 33.5]:
    plt.axvline(_x, ls='--', c='#7251a4')

plt.suptitle(
    f'{nufc} Campaign Difficulty\n Expected points {sum(tmp):.2f} points',
    fontweight='bold',
    color='#555555',
    size='x-large')
# plt.figtext(0.8, 0.04, 'created by @bkktimber', color='#555555',
#             fontweight='bold', size='medium')
# plt.figtext(0.8, 0.07, 'data: Statsbomb vis FBRef', color='#555555',
#             fontweight='bold', size='medium')
plt.savefig('demo1.jpg')
plt.show()

# %%