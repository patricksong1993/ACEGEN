import csv

import tabulate

import evaluations.investor as investor
from classes.player import Player
from classes.prediction import Prediction

# m = Match('2016-ausopen-1701',2014,'usopen',1402,'','')
#
# print m
Player.start_year = 2012
Player.end_year = 2015
Player.surface = 'hard'

matches = []

with open('data/2016-ausopen-atp.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        if row != []:
            matches.append(row)

ps = []
pss = []

for match in matches:
    prediction = Prediction(match[0],match[1],'game_iid_model',match,bo=5)
    prediction.predict_set_score()
    ps.append(prediction)
    pss.append(prediction.to_list())
    # p = match
    # p.extend([prediction.match_winner_prob['p1'], prediction.match_winner_prob['p2'],
    #           prediction.match_score_prob['3:0'], prediction.match_score_prob['3:1'], prediction.match_score_prob['3:2'],
    #           prediction.match_score_prob['0:3'], prediction.match_score_prob['1:3'], prediction.match_score_prob['2:3']])
    # if match[3][0] == '3' and prediction.match_winner_prob['p1']>0.5:
    #     p.insert(0, '+')
    # elif match[3][2] == '3' and prediction.match_winner_prob['p2']>0.5:
    #     p.insert(0, '+')
    # else:
    #     p.insert(0, '-')
    # ps.append(p)


print tabulate.tabulate(pss, headers=['P1','P2','Score','W','Wp','P2p','P2p','2:0p','2:1p','0:2p','1:2p','p1o','p2o','2:0o','2:1o','0:2o','1:2o'])
print investor.winner_only_re(ps)
print investor.winner_hedge_re(ps)
print investor.set_winner_only_re(ps)
print investor.winner_only_br(ps)
#
# for player in Player.cached_players:
#     print player+' '+str(Player.cached_players[player].match_baseline.serv_mean)+','+str(Player.cached_players[player].match_baseline.serv_std)+','+str(Player.cached_players[player].match_baseline.retn_mean)+','+str(Player.cached_players[player].match_baseline.retn_std)
# p = Player('Andy Murray')
# p = Player('Roger Federer')
#
# ps = Player.cached_players.keys()
# for p in ps:
#     Player.cached_players[p].calculate_impact()
# print p