from classes.player import Player
from classes.prediction import Prediction
import tabulate

Player.start_year = 2014
Player.end_year = 2016
Player.surface = 'clay'

player1 = 'Kei Nishikori'
player2 = 'Rafael Nadal'

table = []

row = []
row.append('match')
prediction = Prediction(player1, player2, 'match_iid_model',bo=3)
prediction.predict_set_score()
row.append(prediction.match_winner_prob['p1'])
row.append(prediction.match_winner_prob['p2'])
row.append(prediction.match_score_prob['2:0'])
row.append(prediction.match_score_prob['2:1'])
row.append(prediction.match_score_prob['0:2'])
row.append(prediction.match_score_prob['1:2'])
table.append(row)

row = []
row.append('set')
prediction = Prediction(player1, player2, 'set_iid_model',bo=3)
prediction.predict_set_score()
row.append(prediction.match_winner_prob['p1'])
row.append(prediction.match_winner_prob['p2'])
row.append(prediction.match_score_prob['2:0'])
row.append(prediction.match_score_prob['2:1'])
row.append(prediction.match_score_prob['0:2'])
row.append(prediction.match_score_prob['1:2'])
table.append(row)

row = []
row.append('game')
prediction = Prediction(player1, player2, 'game_iid_model',bo=3)
prediction.predict_set_score()
row.append(prediction.match_winner_prob['p1'])
row.append(prediction.match_winner_prob['p2'])
row.append(prediction.match_score_prob['2:0'])
row.append(prediction.match_score_prob['2:1'])
row.append(prediction.match_score_prob['0:2'])
row.append(prediction.match_score_prob['1:2'])
table.append(row)

print tabulate.tabulate(table, headers=['','P1p','P2p','2:0p','2:1p','0:2p','1:2p'])
