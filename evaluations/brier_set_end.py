from classes.player import Player
import utils.db_conn as db_conn
from classes.prediction_setend import PredictionSetend
import numpy as np
import sys
import datetime


sys.setrecursionlimit(10000)



def brier(model, surface, sy, ey, mixture, ts):
    matches = db_conn.all_matches_year(sy, ey, surface)
    c = 0
    prob = 0
    right = 0
    for match in matches:
        end_date = match[3] + datetime.timedelta(days=-1)
        start_date = end_date + datetime.timedelta(days=-365)
        if not Player.end_year == end_date.__str__():
            Player.start_year = start_date.__str__()
            Player.end_year = end_date.__str__()
            Player.surface = surface
            Player.clean_cached_players()

        p = PredictionSetend(match[0], match[1], model, points_played=match[5], mixture=mixture, ts=ts)
        p.predict_set_score()
        # print p.match_winner_prob['p1'], p.match_winner_prob['p2'], match
        if not np.isnan(p.match_winner_prob['p1']):
            c += 1
            if match[2] == 1:
                if p.match_winner_prob['p1'] > 0.5:
                    right += 1
                prob += (1-p.match_winner_prob['p1'])**2
            else:
                if p.match_winner_prob['p2'] > 0.5:
                    right += 1
                prob += (1-p.match_winner_prob['p2'])**2

    return [c, right, prob]

def runone(model, surface, sy, ed, mixture, ts):
    [c, right, prob] = brier(model, surface, sy, ed, mixture, ts)
    print model, surface, sy, ed, mixture
    print prob, c, right
    print prob/c
    print float(right)/c


for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    runone('set_iid_model', 'hard', 2015, 2015, i, ts=False)
    runone('match_iid_model', 'hard', 2015, 2015, i, ts=False)


