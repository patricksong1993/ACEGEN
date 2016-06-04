from classes.player import Player
import utils.db_conn as db_conn
from classes.prediction import Prediction
import numpy as np
import sys
import datetime


sys.setrecursionlimit(10000)



def brier(model, surface, sy, ey, ts, r):
    matches = db_conn.all_matches_year(sy, ey, surface)
    c = 0
    prob = 0
    right = 0
    for match in matches:
        end_date = match[3] + datetime.timedelta(days=-1)
        start_date = end_date + datetime.timedelta(days=-r)
        if not Player.end_year == end_date.__str__():
            Player.start_year = start_date.__str__()
            Player.end_year = end_date.__str__()
            Player.surface = surface
            Player.clean_cached_players()

        p = Prediction(match[0], match[1], model, bo=3, ts=ts)
        p.predict_set_score()

        if p.match_winner_prob['p1'] > 1 or p.match_winner_prob['p1'] < 0:
            print p.match_winner_prob['p1']
            continue
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

def runone(model, surface, sy, ey, ts, r):
    [c, right, prob] = brier(model, surface, sy, ey, ts, r)
    print model, surface, sy, ey, ts, r
    print prob, c, right
    print prob/c
    print float(right)/c

runone('set_iid_model', 'hard', 2015, 2015, False, 300)
runone('match_iid_model', 'hard', 2015, 2015, False, 300)
runone('game_iid_model', 'hard', 2015, 2015, False, 300)

runone('set_iid_model', 'hard', 2015, 2015, True, 300)
runone('match_iid_model', 'hard', 2015, 2015, True, 300)
runone('game_iid_model', 'hard', 2015, 2015, True, 300)

runone('set_iid_model', 'clay', 2015, 2015, False, 365)
runone('match_iid_model', 'clay', 2015, 2015, False, 365)
runone('game_iid_model', 'clay', 2015, 2015, False, 365)

runone('set_iid_model', 'clay', 2015, 2015, True, 365)
runone('match_iid_model', 'clay', 2015, 2015, True, 365)
runone('game_iid_model', 'clay', 2015, 2015, True, 365)

runone('set_iid_model', 'grass', 2015, 2015, False, 730)
runone('match_iid_model', 'grass', 2015, 2015, False, 730)
runone('game_iid_model', 'grass', 2015, 2015, False, 730)

runone('set_iid_model', 'grass', 2015, 2015, True, 730)
runone('match_iid_model', 'grass', 2015, 2015, True, 730)
runone('game_iid_model', 'grass', 2015, 2015, True, 730)

runone('set_iid_model', 'indoor', 2015, 2015, False, 500)
runone('match_iid_model', 'indoor', 2015, 2015, False, 500)
runone('game_iid_model', 'indoor', 2015, 2015, False, 500)

runone('set_iid_model', 'indoor', 2015, 2015, True, 500)
runone('match_iid_model', 'indoor', 2015, 2015, True, 500)
runone('game_iid_model', 'indoor', 2015, 2015, True, 500)
