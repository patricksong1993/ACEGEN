from classes.match import Match
from classes.player import Player
from classes.prediction import Prediction
import models.investor as investor

# m = Match('2016-ausopen-1701',2014,'usopen',1402,'','')
#
# print m
Player.start_year = 2013
Player.end_year = 2016
Player.surface = 'clay'


prediction = Prediction('Gael Monfils','Rafael Nadal','game_iid_model',bo=3)
prediction.predict_set_score()


print prediction.match_score_prob['2:0']
print prediction.match_score_prob['2:1']
print prediction.match_score_prob['0:2']
print prediction.match_score_prob['1:2']

print prediction.match_winner_prob['p1']

print prediction.match_winner_prob['p2']
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
