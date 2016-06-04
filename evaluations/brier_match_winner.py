from classes.player import Player
import utils.db_conn as db_conn
from classes.prediction import Prediction
import numpy as np
import sys
import datetime


sys.setrecursionlimit(10000)



def brier(models, surface, sy, ey, ts, r):
    matches = db_conn.all_matches_year(sy, ey, surface)
    rs = {}
    for model in models:
        rs[model] = [0,0,0]

    for match in matches:
        end_date = match[3] + datetime.timedelta(days=-1)
        start_date = end_date + datetime.timedelta(days=-r)
        if not Player.end_year == end_date.__str__():
            Player.start_year = start_date.__str__()
            Player.end_year = end_date.__str__()
            Player.surface = surface
            Player.clean_cached_players()

        for model in models:
            p = Prediction(match[0], match[1], model, bo=3, ts=ts)
            p.predict_set_score()

            if p.match_winner_prob['p1'] > 1 or p.match_winner_prob['p1'] < 0:
                print p.match_winner_prob['p1']
                continue
            if not np.isnan(p.match_winner_prob['p1']):
                rs[model][0] += 1
                if match[2] == 1:
                    if p.match_winner_prob['p1'] > 0.5:
                        rs[model][1] += 1
                    rs[model][2] += (1-p.match_winner_prob['p1'])**2
                else:
                    if p.match_winner_prob['p2'] > 0.5:
                        rs[model][1] += 1
                    rs[model][2] += (1-p.match_winner_prob['p2'])**2

    return rs

def runone(model, surface, sy, ey, ts, r):
    rs = brier(model, surface, sy, ey, ts, r)
    for rs_ in rs:
        print rs_, surface, sy, ey, ts, r
        print rs[rs_][0], rs[rs_][1], rs[rs_][2]
        print rs[rs_][2]/rs[rs_][0]
        print float(rs[rs_][1])/rs[rs_][0]

runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'hard', 2013, 2015, False, 300)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'hard', 2013, 2015, False, 365)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'hard', 2013, 2015, False, 200)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'hard', 2013, 2015, False, 500)

runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'grass', 2013, 2015, False, 730)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'clay', 2013, 2015, False, 365)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'indoor', 2013, 2015, False, 500)

runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'hard', 2013, 2015, True, 300)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'grass', 2013, 2015, True, 730)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'clay', 2013, 2015, True, 365)
runone(['set_iid_model', 'match_iid_model', 'game_iid_model'], 'indoor', 2013, 2015, True, 500)