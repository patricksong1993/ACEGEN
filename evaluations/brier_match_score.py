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

        winner = match[2]
        score = match[4]
        set_length = score.split().__len__()

        ms = ''
        if winner == 1:
            if set_length == 3:
                ms = '2:1'
            else:
                ms = '2:0'
        else:
            if set_length == 3:
                ms = '1:2'
            else:
                ms = '0:2'

        p = Prediction(match[0], match[1], model, bo=3, ts=ts)
        p.predict_set_score()

        ms_20 = p.match_score_prob['2:0']
        ms_21 = p.match_score_prob['2:1']
        ms_02 = p.match_score_prob['0:2']
        ms_12 = p.match_score_prob['1:2']

        if not np.isnan(p.match_winner_prob['p1']):
            c += 1
            prob += (1 - p.match_score_prob[ms])**2
            if ms == '2:0' and ms_20 >= ms_21 and ms_20 >= ms_02 and ms_20 >= ms_12:
                right += 1
            if ms == '2:1' and ms_21 >= ms_20 and ms_21 >= ms_02 and ms_21 >= ms_12:
                right += 1
            if ms == '1:2' and ms_12 >= ms_21 and ms_12 >= ms_02 and ms_12 >= ms_20:
                right += 1
            if ms == '0:2' and ms_02 >= ms_20 and ms_02 >= ms_21 and ms_02 >= ms_12:
                right += 1

    return [c, right, prob]

def runone(model, surface, sy, ey, ts, r):
    [c, right, prob] = brier(model, surface, sy, ey, ts, r)
    print model, surface, sy, ey, ts, r
    print prob, c, right
    print prob / c
    print float(right) / c

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


