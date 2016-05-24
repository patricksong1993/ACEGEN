from classes.player import Player
import utils.db_conn as db_conn
from classes.prediction import Prediction
import numpy as np
import sys
import datetime


sys.setrecursionlimit(10000)



def brier(matches, model):
    c = 0
    prob = 0
    right = 0
    for match in matches:
        end_date = match[3] + datetime.timedelta(days=0)
        start_date = end_date + datetime.timedelta(days=-730)
        if not Player.end_year == end_date.__str__():
            Player.start_year = start_date.__str__()
            Player.end_year = end_date.__str__()
            Player.surface = 'hard'
            Player.clean_cached_players()

        p = Prediction(match[0], match[1], model, bo=3, ts=True)
        if not p.minMreached:
            continue
        p.predict_set_score()
        if not np.isnan(p.match_winner_prob['p1']):
            c += 1
            if match[2] == 1:
                if p.match_winner_prob['p1'] > 0.5:
                    right += 1
                prob += 1-p.match_winner_prob['p1']
            else:
                if p.match_winner_prob['p2'] > 0.5:
                    right += 1
                prob += 1-p.match_winner_prob['p2']

    return [c, right, prob]





matches = db_conn.all_matches_year(2015,2015,'hard')


[c, right, prob] = brier(matches, 'match_iid_model')
print '2015 hard match 730'
print prob, c, right
print prob/c
print float(right)/c

[c, right, prob] = brier(matches, 'set_iid_model')
print '2015 hard set'
print prob, c, right
print prob/c
print float(right)/c



