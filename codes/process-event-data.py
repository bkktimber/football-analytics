# %%
import json
import os
import pickle
import pandas as pd
import matplotsoccer as mps
import matplotlib.pyplot as plt
from tqdm import tqdm

base_dir = '/Users/Mai/Projects/football-analytics/data/whoscored/epl/20202021'
os.chdir(base_dir)
# %%
# filename = '1485326/data.pkl'
filename = '1485208/data.pkl'
os.path.isfile(filename)
# %%
with open(filename, 'rb') as f:
    data = pickle.load(f)

print(len(data))

# data keys:
# data[0] = event data
# data[1] = event description dict
# data[0] = match id
# data[0] = formation description dict
# %%
# 'playerIdNameDictionary' = mapping player with his ID,
# 'periodMinuteLimits' = time limit of each period,
# 'timeStamp' = 'Timestamp,
# 'attendance' = number of attendance,
# 'venueName' = Venue Name,
# 'referee' = Referee info (id, firstname, lastname, status, full name),
# 'weatherCode',
# 'elapsed' = match status,
# 'startTime' = match time in UTC,
# 'startDate' = match date,
# 'score' = Score,
# 'htScore' = Half Time score,
# 'htScore' = Full Time score,
# 'etScore' = Extra Time score,
# 'pkScore' = PK shotout score,
# 'statusCode',
# 'periodCode',
# 'home' = Home tema count events,
# 'away' = Away tema count events,
# 'maxMinute' = Total Match time (90 + added time),
# 'minuteExpanded' = Total time (actual play time),
# 'maxPeriod' = number of halves,
# 'expandedMinutes' = Max game time,
# 'expandedMaxMinute' = Max actual play time,
# 'periodEndMinutes' = Game times where periods end,
# 'commonEvents',
# 'events',
# 'timeoutInSeconds'
# %%
def getEventName(event_id: int=None):
    event_id_dict = {'shotSixYardBox': 0,
                     'shotPenaltyArea': 1,
                     'shotOboxTotal': 2,
                     'shotOpenPlay': 3,
                     'shotCounter': 4,
                     'shotSetPiece': 5,
                     'shotOffTarget': 6,
                     'shotOnPost': 7,
                     'shotOnTarget': 8,
                     'shotsTotal': 9,
                     'shotBlocked': 10,
                     'shotRightFoot': 11,
                     'shotLeftFoot': 12,
                     'shotHead': 13,
                     'shotObp': 14,
                     'goalSixYardBox': 15,
                     'goalPenaltyArea': 16,
                     'goalObox': 17,
                     'goalOpenPlay': 18,
                     'goalCounter': 19,
                     'goalSetPiece': 20,
                     'penaltyScored': 21,
                     'goalOwn': 22,
                     'goalNormal': 23,
                     'goalRightFoot': 24,
                     'goalLeftFoot': 25,
                     'goalHead': 26,
                     'goalObp': 27,
                     'shortPassInaccurate': 28,
                     'shortPassAccurate': 29,
                     'passCorner': 30,
                     'passCornerAccurate': 31,
                     'passCornerInaccurate': 32,
                     'passFreekick': 33,
                     'passBack': 34,
                     'passForward': 35,
                     'passLeft': 36,
                     'passRight': 37,
                     'keyPassLong': 38,
                     'keyPassShort': 39,
                     'keyPassCross': 40,
                     'keyPassCorner': 41,
                     'keyPassThroughball': 42,
                     'keyPassFreekick': 43,
                     'keyPassThrowin': 44,
                     'keyPassOther': 45,
                     'assistCross': 46,
                     'assistCorner': 47,
                     'assistThroughball': 48,
                     'assistFreekick': 49,
                     'assistThrowin': 50,
                     'assistOther': 51,
                     'dribbleLost': 52,
                     'dribbleWon': 53,
                     'challengeLost': 54,
                     'interceptionWon': 55,
                     'clearanceHead': 56,
                     'outfielderBlock': 57,
                     'passCrossBlockedDefensive': 58,
                     'outfielderBlockedPass': 59,
                     'offsideGiven': 60,
                     'offsideProvoked': 61,
                     'foulGiven': 62,
                     'foulCommitted': 63,
                     'yellowCard': 64,
                     'voidYellowCard': 65,
                     'secondYellow': 66,
                     'redCard': 67,
                     'turnover': 68,
                     'dispossessed': 69,
                     'saveLowLeft': 70,
                     'saveHighLeft': 71,
                     'saveLowCentre': 72,
                     'saveHighCentre': 73,
                     'saveLowRight': 74,
                     'saveHighRight': 75,
                     'saveHands': 76,
                     'saveFeet': 77,
                     'saveObp': 78,
                     'saveSixYardBox': 79,
                     'savePenaltyArea': 80,
                     'saveObox': 81,
                     'keeperDivingSave': 82,
                     'standingSave': 83,
                     'closeMissHigh': 84,
                     'closeMissHighLeft': 85,
                     'closeMissHighRight': 86,
                     'closeMissLeft': 87,
                     'closeMissRight': 88,
                     'shotOffTargetInsideBox': 89,
                     'touches': 90,
                     'assist': 91,
                     'ballRecovery': 92,
                     'clearanceEffective': 93,
                     'clearanceTotal': 94,
                     'clearanceOffTheLine': 95,
                     'dribbleLastman': 96,
                     'errorLeadsToGoal': 97,
                     'errorLeadsToShot': 98,
                     'intentionalAssist': 99,
                     'interceptionAll': 100,
                     'interceptionIntheBox': 101,
                     'keeperClaimHighLost': 102,
                     'keeperClaimHighWon': 103,
                     'keeperClaimLost': 104,
                     'keeperClaimWon': 105,
                     'keeperOneToOneWon': 106,
                     'parriedDanger': 107,
                     'parriedSafe': 108,
                     'collected': 109,
                     'keeperPenaltySaved': 110,
                     'keeperSaveInTheBox': 111,
                     'keeperSaveTotal': 112,
                     'keeperSmother': 113,
                     'keeperSweeperLost': 114,
                     'keeperMissed': 115,
                     'passAccurate': 116,
                     'passBackZoneInaccurate': 117,
                     'passForwardZoneAccurate': 118,
                     'passInaccurate': 119,
                     'passAccuracy': 120,
                     'cornerAwarded': 121,
                     'passKey': 122,
                     'passChipped': 123,
                     'passCrossAccurate': 124,
                     'passCrossInaccurate': 125,
                     'passLongBallAccurate': 126,
                     'passLongBallInaccurate': 127,
                     'passThroughBallAccurate': 128,
                     'passThroughBallInaccurate': 129,
                     'passThroughBallInacurate': 130,
                     'passFreekickAccurate': 131,
                     'passFreekickInaccurate': 132,
                     'penaltyConceded': 133,
                     'penaltyMissed': 134,
                     'penaltyWon': 135,
                     'passRightFoot': 136,
                     'passLeftFoot': 137,
                     'passHead': 138,
                     'sixYardBlock': 139,
                     'tackleLastMan': 140,
                     'tackleLost': 141,
                     'tackleWon': 142,
                     'cleanSheetGK': 143,
                     'cleanSheetDL': 144,
                     'cleanSheetDC': 145,
                     'cleanSheetDR': 146,
                     'cleanSheetDML': 147,
                     'cleanSheetDMC': 148,
                     'cleanSheetDMR': 149,
                     'cleanSheetML': 150,
                     'cleanSheetMC': 151,
                     'cleanSheetMR': 152,
                     'cleanSheetAML': 153,
                     'cleanSheetAMC': 154,
                     'cleanSheetAMR': 155,
                     'cleanSheetFWL': 156,
                     'cleanSheetFW': 157,
                     'cleanSheetFWR': 158,
                     'cleanSheetSub': 159,
                     'goalConcededByTeamGK': 160,
                     'goalConcededByTeamDL': 161,
                     'goalConcededByTeamDC': 162,
                     'goalConcededByTeamDR': 163,
                     'goalConcededByTeamDML': 164,
                     'goalConcededByTeamDMC': 165,
                     'goalConcededByTeamDMR': 166,
                     'goalConcededByTeamML': 167,
                     'goalConcededByTeamMC': 168,
                     'goalConcededByTeamMR': 169,
                     'goalConcededByTeamAML': 170,
                     'goalConcededByTeamAMC': 171,
                     'goalConcededByTeamAMR': 172,
                     'goalConcededByTeamFWL': 173,
                     'goalConcededByTeamFW': 174,
                     'goalConcededByTeamFWR': 175,
                     'goalConcededByTeamSub': 176,
                     'goalConcededOutsideBoxGoalkeeper': 177,
                     'goalScoredByTeamGK': 178,
                     'goalScoredByTeamDL': 179,
                     'goalScoredByTeamDC': 180,
                     'goalScoredByTeamDR': 181,
                     'goalScoredByTeamDML': 182,
                     'goalScoredByTeamDMC': 183,
                     'goalScoredByTeamDMR': 184,
                     'goalScoredByTeamML': 185,
                     'goalScoredByTeamMC': 186,
                     'goalScoredByTeamMR': 187,
                     'goalScoredByTeamAML': 188,
                     'goalScoredByTeamAMC': 189,
                     'goalScoredByTeamAMR': 190,
                     'goalScoredByTeamFWL': 191,
                     'goalScoredByTeamFW': 192,
                     'goalScoredByTeamFWR': 193,
                     'goalScoredByTeamSub': 194,
                     'aerialSuccess': 195,
                     'duelAerialWon': 196,
                     'duelAerialLost': 197,
                     'offensiveDuel': 198,
                     'defensiveDuel': 199,
                     'bigChanceMissed': 200,
                     'bigChanceScored': 201,
                     'bigChanceCreated': 202,
                     'overrun': 203,
                     'successfulFinalThirdPasses': 204,
                     'punches': 205,
                     'penaltyShootoutScored': 206,
                     'penaltyShootoutMissedOffTarget': 207,
                     'penaltyShootoutSaved': 208,
                     'penaltyShootoutSavedGK': 209,
                     'penaltyShootoutConcededGK': 210,
                     'throwIn': 211,
                     'subOn': 212,
                     'subOff': 213,
                     'defensiveThird': 214,
                     'midThird': 215,
                     'finalThird': 216,
                     'pos': 217}
    _keys = list(event_id_dict.keys())
    _values = list(event_id_dict.values())
    return _keys[_values.index(event_id)]
# %%
def convert_coordinate(values: pd.Series=None, mode='width') -> pd.Series:
    '''
        Opta coordinate data are normalised to [0, 1]
        matplotsoccer coordinates are in metre.
    '''
    if mode == 'length':
        coef = 105/100
    else mode == 'width':
        coef = 68/100
    return values * coef

def getMatchInfo(data):
    return None
# %%
# shows plot of football ptich

ax = mps.field(figsize=8, show=False)
for i in range(len(data[0].get('events'))):
    if data[0].get('events')[i].get('teamId') == 23:
        ax.scatter(_convert_l(data[0].get('events')[i].get('x')), _convert_w(data[0].get('events')[i].get('y')), color='black')
    else:
        ax.scatter(_convert_l(data[0].get('events')[i].get('x')), _convert_w(data[0].get('events')[i].get('y')), color='blue')
plt.show()
# %%
x = []
y = []
for i in range(len(data[0].get('events'))):
    if data[0].get('events')[i].get('teamId') != 23:
        x.append(_convert_l(data[0].get('events')[i].get('x')))
        y.append(_convert_w(data[0].get('events')[i].get('y')))

x = pd.Series(x)
y = pd.Series(y)
# footbal pitch is a 6x3 grid
hm = mps.count(x, y, 6, 3)
mps.heatmap(hm)
plt.show()
# %%

# %%

event_dir = '/Users/Mai/Projects/football-analytics/data/whoscored/epl/20172018'
match_ids = [p for p in os.listdir(event_dir) if len(p.split('.')) == 1]
for ix in tqdm(match_ids):
    dst_dir = os.path.join(event_dir, ix)
    with open(os.path.join(dst_dir, 'data.pkl'), 'rb') as f:
        data = pickle.load(f)
    
    with open(dst_dir + '.pkl', 'wb') as f:
        pickle.dump(data[0], f)
# %%
