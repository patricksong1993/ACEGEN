import classes.player as player
import math as math
import numpy as np
from models.game_iid_model import GameIIDModel
from models.set_iid_model import SetIIDModel
from models.match_iid_model import MatchIIDModel

class Prediction:

    def __init__(self, p1_name, p2_name, model, data='', bo=5):
        self.p1 = player.Player.get_player(p1_name)
        if self.p1.match_impact == 0:
            self.p1.calculate_impact()
        self.p2 = player.Player.get_player(p2_name)
        if self.p2.match_impact == 0:
            self.p2.calculate_impact()


        self.bo = bo

        self.match_exp = 0
        self.set_exp = {}
        self.game_exp = {}
        self.point_exp = {}

        self.calculate_exp(self.p1, self.p2, self.bo)

        if model == 'set_iid_model':
            self.model = SetIIDModel(self.match_exp, self.set_exp, self.game_exp, self.point_exp, bo=self.bo)
        elif model == 'game_iid_model':
            self.model = GameIIDModel(self.match_exp, self.set_exp, self.game_exp, self.point_exp, bo=self.bo)
        elif model == 'match_iid_model':
            self.model = MatchIIDModel(self.match_exp, self.set_exp, self.game_exp, self.point_exp, bo=self.bo)

        self.match_score_prob = {}
        self.match_winner_prob = {}

        self.match_winner_odds = {}
        self.match_score_odds = {}

        if data != '':
            if self.bo == 5:
                self.match_score = data[3]
                if self.match_score[0] > self.match_score[2]:
                    self.match_winner = 'p1'
                else:
                    self.match_winner = 'p2'

                self.match_winner_odds['p1'] = float(data[4])
                self.match_winner_odds['p2'] = float(data[5])

                self.match_score_odds['3:0'] = float(data[6])
                self.match_score_odds['3:1'] = float(data[7])
                self.match_score_odds['3:2'] = float(data[8])
                self.match_score_odds['0:3'] = float(data[9])
                self.match_score_odds['1:3'] = float(data[10])
                self.match_score_odds['2:3'] = float(data[11])

                self.round = int(data[2])
            elif self.bo == 3:
                self.match_score = data[3]
                if self.match_score[0] > self.match_score[2]:
                    self.match_winner = 'p1'
                else:
                    self.match_winner = 'p2'

                self.match_winner_odds['p1'] = float(data[4])
                self.match_winner_odds['p2'] = float(data[5])

                self.match_score_odds['2:0'] = float(data[6])
                self.match_score_odds['2:1'] = float(data[7])
                self.match_score_odds['0:2'] = float(data[8])
                self.match_score_odds['1:2'] = float(data[9])

                self.round = int(data[2])

    def to_list(self):
        all_attr = []
        all_attr.extend([self.p1.name, self.p2.name, self.match_score, self.match_winner])
        all_attr.append('p1' if self.match_winner_prob['p1']>0.5 else 'p2')
        all_attr.extend([self.match_winner_prob['p1'], self.match_winner_prob['p2']])

        if self.bo == 5:
            all_attr.extend([self.match_score_prob['3:0'], self.match_score_prob['3:1'], self.match_score_prob['3:2'],
                            self.match_score_prob['0:3'], self.match_score_prob['1:3'], self.match_score_prob['2:3']])
        elif self.bo == 3:
            all_attr.extend([self.match_score_prob['2:0'], self.match_score_prob['2:1'],
                             self.match_score_prob['0:2'], self.match_score_prob['1:2']])

        all_attr.extend([self.match_winner_odds['p1'], self.match_winner_odds['p2']])
        if self.bo == 5:
            all_attr.extend([self.match_score_odds['3:0'], self.match_score_odds['3:1'], self.match_score_odds['3:2'],
                            self.match_score_odds['0:3'], self.match_score_odds['1:3'], self.match_score_odds['2:3']])
        elif self.bo == 3:
            all_attr.extend([self.match_score_odds['2:0'], self.match_score_odds['2:1'],
                             self.match_score_odds['0:2'], self.match_score_odds['1:2']])

        return all_attr

    def predict_set_score(self):
        match_matrix = self.model.match_matrix()

        if self.bo == 5:
            self.match_score_prob['3:0'] = np.sum(match_matrix[3][0])
            self.match_score_prob['3:1'] = np.sum(match_matrix[3][1])
            self.match_score_prob['3:2'] = np.sum(match_matrix[3][2])
            self.match_score_prob['0:3'] = np.sum(match_matrix[0][3])
            self.match_score_prob['1:3'] = np.sum(match_matrix[1][3])
            self.match_score_prob['2:3'] = np.sum(match_matrix[2][3])

            self.match_winner_prob['p1'] = self.match_score_prob['3:0'] + self.match_score_prob['3:1'] + self.match_score_prob['3:2']
            self.match_winner_prob['p2'] = self.match_score_prob['0:3'] + self.match_score_prob['1:3'] + self.match_score_prob['2:3']

        elif self.bo == 3:
            self.match_score_prob['2:0'] = np.sum(match_matrix[2][0])
            self.match_score_prob['2:1'] = np.sum(match_matrix[2][1])
            self.match_score_prob['0:2'] = np.sum(match_matrix[0][2])
            self.match_score_prob['1:2'] = np.sum(match_matrix[1][2])

            self.match_winner_prob['p1'] = self.match_score_prob['2:0'] + self.match_score_prob['2:1']
            self.match_winner_prob['p2'] = self.match_score_prob['0:2'] + self.match_score_prob['1:2']

    def calculate_exp(self, p1, p2, bo=5):
        self.match_exp = PredictionStats(p1.match_baseline, p1.match_impact, p2.match_baseline, p2.match_impact)

        if bo == 5:
            scenarios = ['0:0', '0:1', '1:0', '1:1', '1:2', '2:1', '2:2', '0:2', '2:0']
            for s in scenarios:
                p1_baseline = p1.set_baseline.get(s, p1.match_baseline)
                p1_impact = p1.set_impact.get(s, p1.match_impact)
                p2_baseline = p2.set_baseline.get(inverse_score(s), p2.match_baseline)
                p2_impact = p2.set_impact.get(inverse_score(s), p2.match_impact)
                # solve nan, match baseline and impact
                p1_baseline = solve_nan(p1_baseline, p1.match_baseline)
                p1_impact = solve_nan(p1_impact, p1.match_impact)
                p2_baseline = solve_nan(p2_baseline, p2.match_baseline)
                p2_impact = solve_nan(p2_impact, p2.match_impact)

                set_exp_temp = PredictionStats(p1_baseline, p1_impact, p2_baseline, p2_impact)
                self.set_exp[s] = set_exp_temp
        elif bo == 3:
            scenarios = ['0:0', '0:1', '1:0', '1:1']
            for s in scenarios:
                p1_baseline = p1.set_baseline_3.get(s, p1.match_baseline)
                p1_impact = p1.set_impact_3.get(s, p1.match_impact)
                p2_baseline = p2.set_baseline_3.get(inverse_score(s), p2.match_baseline)
                p2_impact = p2.set_impact_3.get(inverse_score(s), p2.match_impact)
                # solve nan, match baseline and impact
                p1_baseline = solve_nan(p1_baseline, p1.match_baseline)
                p1_impact = solve_nan(p1_impact, p1.match_impact)
                p2_baseline = solve_nan(p2_baseline, p2.match_baseline)
                p2_impact = solve_nan(p2_impact, p2.match_impact)

                set_exp_temp = PredictionStats(p1_baseline, p1_impact, p2_baseline, p2_impact)
                self.set_exp[s] = set_exp_temp

        scenarios = [3, 2, 1, 0, -1, -2, -3]
        for s in scenarios:
            p1_baseline = p1.game_baseline.get(s, p1.match_baseline)
            p1_impact = p1.game_impact.get(s, p1.match_impact)
            p2_baseline = p2.game_baseline.get(inverse_score(s), p2.match_baseline)
            p2_impact = p2.game_impact.get(inverse_score(s), p2.match_impact)
            # solve nan, match baseline and impact
            p1_baseline = solve_nan(p1_baseline, p1.match_baseline)
            p1_impact = solve_nan(p1_impact, p1.match_impact)
            p2_baseline = solve_nan(p2_baseline, p2.match_baseline)
            p2_impact = solve_nan(p2_impact, p2.match_impact)

            game_exp_temp = PredictionStats(p1_baseline, p1_impact, p2_baseline, p2_impact)
            self.game_exp[s] = game_exp_temp

        scenarios = ['30:40', '30:30', '30:15', '15:40', '0:40', '15:15', '15:0', '0:0', '40:30', '40:AD', '40:15',
                     '0:30', '15:30', '40:0', '30:0', '0:15', 'AD:40', '40:40']
        for s in scenarios:
            p1_baseline = p1.point_baseline.get(s, p1.match_baseline)
            p1_impact = p1.point_impact.get(s, p1.match_impact)
            p2_baseline = p2.point_baseline.get(inverse_score(s), p2.match_baseline)
            p2_impact = p2.point_impact.get(inverse_score(s), p2.match_impact)
            # solve nan, match baseline and impact
            p1_baseline = solve_nan(p1_baseline, p1.match_baseline)
            p1_impact = solve_nan(p1_impact, p1.match_impact)
            p2_baseline = solve_nan(p2_baseline, p2.match_baseline)
            p2_impact = solve_nan(p2_impact, p2.match_impact)

            point_exp_temp = PredictionStats(p1_baseline, p1_impact, p2_baseline, p2_impact)
            self.point_exp[s] = point_exp_temp


class PredictionStats:

    def __init__(self, p1_baseline, p1_impact, p2_baseline, p2_impact):
        p1_serv_pct = p1_baseline.serv_mean + p2_impact.serv_mean
        p1_serv_pct_std = math.sqrt(p1_baseline.serv_std ** 2 + p2_impact.serv_std ** 2)
        if p1_serv_pct_std == 0.0:
            p1_serv_pct_std = 0.2
        p1_retn_pct = p1_baseline.retn_mean + p2_impact.retn_mean
        p1_retn_pct_std = math.sqrt(p1_baseline.retn_std ** 2 + p2_impact.retn_std ** 2)
        if p1_retn_pct_std == 0.0:
            p1_retn_pct_std = 0.2
        p2_serv_pct = p2_baseline.serv_mean + p1_impact.serv_mean
        p2_serv_pct_std = math.sqrt(p2_baseline.serv_std ** 2 + p1_impact.serv_std ** 2)
        if p2_serv_pct_std == 0.0:
            p2_serv_pct_std = 0.2
        p2_retn_pct = p2_baseline.retn_mean + p1_impact.retn_mean
        p2_retn_pct_std = math.sqrt(p2_baseline.retn_std ** 2 + p1_impact.retn_std ** 2)
        if p2_retn_pct_std == 0.0:
            p2_retn_pct_std = 0.2

        # weighted ave, norm?
        # serving percentage using p1_serv and 1-p2_serv
        self.p1_pct = (p1_serv_pct / (p1_serv_pct_std ** 2) + (1 - p2_retn_pct) / (p2_retn_pct_std ** 2)) / \
                 (1 / (p1_serv_pct_std ** 2) + 1 / (p2_retn_pct_std ** 2))
        self.p1_pct_std = math.sqrt((p1_serv_pct_std / (1 + p1_serv_pct_std ** 2 / p2_retn_pct_std ** 2)) ** 2 + (
            p2_retn_pct_std / (1 + p2_retn_pct_std ** 2 / p1_serv_pct_std ** 2)) ** 2)
        self.p2_pct = (p2_serv_pct / (p2_serv_pct_std ** 2) + (1 - p1_retn_pct) / (p1_retn_pct_std ** 2)) / \
                 (1 / (p2_serv_pct_std ** 2) + 1 / (p1_retn_pct_std ** 2))
        self.p2_pct_std = math.sqrt((p2_serv_pct_std / (1 + p2_serv_pct_std ** 2 / p1_retn_pct_std ** 2)) ** 2 + (
            p1_retn_pct_std / (1 + p1_retn_pct_std ** 2 / p2_serv_pct_std ** 2)) ** 2)


def solve_nan(other_stats, match_stats):
    if math.isnan(other_stats.serv_mean):
        other_stats.serv_mean = match_stats.serv_mean
        other_stats.serv_std = match_stats.serv_std
    if math.isnan(other_stats.retn_mean):
        other_stats.retn_mean = match_stats.retn_mean
        other_stats.retn_std = match_stats.retn_std
    return other_stats

def inverse_score(score):
    if type(score) is str:
        scores = score.split(':')
        return scores[1] + ":" + scores[0]
    if type(score) is int:
        return 0 - score
