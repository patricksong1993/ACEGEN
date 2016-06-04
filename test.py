import sys

from classes.player import Player
from classes.prediction import Prediction
import utils.db_conn as db_conn

import numpy as np
sys.setrecursionlimit(10000)
# m = Match('2016-ausopen-1701',2014,'usopen',1402,'','')
#
# print m
Player.start_year = '2012-01-01'
Player.end_year = '2015-12-31'
Player.surface = 'clay'


# ps = db_conn.all_players()
#
#
#
# for p in ps:
#     Player(p[0])
#
# Player.calculate_all_ts()
#
# serv = []
# retn = []
# for p in Player.cached_players:
#     serv.append(Player.cached_players[p].match_impact_ts.serv_mean)
#     retn.append(Player.cached_players[p].match_impact_ts.retn_mean)
#
# print serv
# print retn
#
# print np.nanmean(serv)
# print np.nanmean(retn)
#
# print np.nanstd(serv)
# print np.nanstd(retn)
#
# serv = []
# retn = []
# for p in Player.cached_players:
#     if '0:0' in Player.cached_players[p].set_impact_3_ts.keys():
#         serv.append(Player.cached_players[p].set_impact_3_ts['0:0'].serv_mean)
#         retn.append(Player.cached_players[p].set_impact_3_ts['0:0'].retn_mean)
# print '0:0'
# print serv
# print retn
#
# print np.nanmean(serv)
# print np.nanmean(retn)
#
# print np.nanstd(serv)
# print np.nanstd(retn)
#
# serv = []
# retn = []
# for p in Player.cached_players:
#     if '1:0' in Player.cached_players[p].set_impact_3_ts.keys():
#         serv.append(Player.cached_players[p].set_impact_3_ts['1:0'].serv_mean)
#         retn.append(Player.cached_players[p].set_impact_3_ts['1:0'].retn_mean)
# print '1:0'
# print serv
# print retn
#
# print np.nanmean(serv)
# print np.nanmean(retn)
#
# print np.nanstd(serv)
# print np.nanstd(retn)
#
# serv = []
# retn = []
# for p in Player.cached_players:
#     if '0:1' in Player.cached_players[p].set_impact_3_ts.keys():
#         serv.append(Player.cached_players[p].set_impact_3_ts['0:1'].serv_mean)
#         retn.append(Player.cached_players[p].set_impact_3_ts['0:1'].retn_mean)
# print '0:1'
# print serv
# print retn
#
# print np.nanmean(serv)
# print np.nanmean(retn)
#
# print np.nanstd(serv)
# print np.nanstd(retn)
#
# serv = []
# retn = []
# for p in Player.cached_players:
#     if '1:1' in Player.cached_players[p].set_impact_3_ts.keys():
#         serv.append(Player.cached_players[p].set_impact_3_ts['1:1'].serv_mean)
#         retn.append(Player.cached_players[p].set_impact_3_ts['1:1'].retn_mean)
# print '1:1'
# print serv
# print retn
#
# print np.nanmean(serv)
# print np.nanmean(retn)
#
# print np.nanstd(serv)
# print np.nanstd(retn)
#

#
Player('Andy Murray')
Player('Novak Djokovic')

Player.calculate_all_ts()

for p in Player.cached_players:
    if -1 in Player.cached_players[p].game_baseline.keys():
        if Player.cached_players[p].match_baseline.serv_counts > 10:
            if Player.cached_players[p].game_baseline[-1].serv_counts > 50:
                if Player.cached_players[p].match_baseline.serv_mean < Player.cached_players[p].game_baseline[-1].serv_mean:
                    if Player.cached_players[p].match_baseline.retn_mean < Player.cached_players[p].game_baseline[-1].retn_mean:
                        if Player.cached_players[p].match_impact.serv_mean > Player.cached_players[p].game_impact[-1].serv_mean:
                            if Player.cached_players[p].match_impact.serv_mean > Player.cached_players[p].game_impact[-1].serv_mean:
                                print p
                                print Player.cached_players[p].match_baseline.serv_counts
                                print Player.cached_players[p].game_baseline[-1].serv_counts
                                print Player.cached_players[p].match_baseline.serv_mean - Player.cached_players[p].game_baseline[-1].serv_mean
                                print Player.cached_players[p].match_baseline.retn_mean - Player.cached_players[p].game_baseline[-1].retn_mean
                                print Player.cached_players[p].match_impact.serv_mean - Player.cached_players[p].game_impact[-1].serv_mean
                                print Player.cached_players[p].match_impact.serv_mean - Player.cached_players[p].game_impact[-1].serv_mean

#
#
#
#
# prediction = Prediction('Andy Murray', 'Roger Federer', 'point_iid_model', bo=3)
# prediction.predict_set_score()
#
# print prediction.match_score_prob['2:0']
# print prediction.match_score_prob['2:1']
# print prediction.match_score_prob['0:2']
# print prediction.match_score_prob['1:2']
#
# print prediction.match_winner_prob['p1']
#
# print prediction.match_winner_prob['p2']
#
# matches = []
#
# with open('data/2015-montecarlo-atp.csv', 'rb') as csvfile:
#     spamreader = csv.reader(csvfile)
#     for row in spamreader:
#         if row != []:
#             matches.append(row)
#
# ps = []
# pss = []
#
# for match in matches:
#     prediction = Prediction(match[0],match[1],'set_iid_model',match, bo=3)
#     prediction.predict_set_score()
#     ps.append(prediction)
#     pss.append(prediction.to_list())
#     # p = match
#     # p.extend([prediction.match_winner_prob['p1'], prediction.match_winner_prob['p2'],
#     #           prediction.match_score_prob['3:0'], prediction.match_score_prob['3:1'], prediction.match_score_prob['3:2'],
#     #           prediction.match_score_prob['0:3'], prediction.match_score_prob['1:3'], prediction.match_score_prob['2:3']])
#     # if match[3][0] == '3' and prediction.match_winner_prob['p1']>0.5:
#     #     p.insert(0, '+')
#     # elif match[3][2] == '3' and prediction.match_winner_prob['p2']>0.5:
#     #     p.insert(0, '+')
#     # else:
#     #     p.insert(0, '-')
#     # ps.append(p)
#
#
# print tabulate.tabulate(pss, headers=['P1','P2','Score','W','Wp','P2p','P2p','3:0p','3:1p','3:2p','0:3p','1:3p','2:3p','p1o','p2o','3:0o','3:1o','3:2o','0:3o','1:3o','2:3o'])
# print investor.winner_only_re(ps)
# print investor.winner_hedge_re(ps)
# print investor.winner_only_br(ps)
# print investor.set_winner_only_re(ps)
#
