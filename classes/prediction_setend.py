import classes.player as player
import math as math
import numpy as np
from models.set_iid_model_setend import SetIIDModelSetend
from models.match_iid_model_setend import MatchIIDModelSetend
from classes.match import Match


class PredictionSetend:

    def __init__(self, p1_name, p2_name, model, points_played='', mixture=0, ts=False, setend=1):
        self.p1 = player.Player.get_player(p1_name)
        if self.p1.match_impact == 0:
            self.p1.calculate_impact()
        self.p2 = player.Player.get_player(p2_name)
        if self.p2.match_impact == 0:
            self.p2.calculate_impact()

        self.ts = ts

        if self.ts:
            player.Player.calculate_all_ts()

        self.points_played = points_played.split('.')

        self.match_exp = 0
        self.set_exp = {}
        self.game_exp = {}
        self.point_exp = {}

        self.calculate_exp(self.p1, self.p2, 3, self.ts)


        if mixture != 0:
            m = Match(0,0,0,0,0,0,self.points_played[0])
            p1_ingame_pct = m.match_pct.p1_serv_pct
            p2_ingame_pct = m.match_pct.p2_serv_pct

            self.match_exp.p1_pct = self.match_exp.p1_pct * (1 - mixture) + p1_ingame_pct * mixture
            self.match_exp.p2_pct = self.match_exp.p2_pct * (1 - mixture) + p2_ingame_pct * mixture

            self.set_exp['0:0'].p1_pct = self.set_exp['0:0'].p1_pct * (1 - mixture) + p1_ingame_pct * mixture
            self.set_exp['0:0'].p2_pct = self.set_exp['0:0'].p2_pct * (1 - mixture) + p2_ingame_pct * mixture

            self.set_exp['1:0'].p1_pct = self.set_exp['1:0'].p1_pct * (1 - mixture) + p1_ingame_pct * mixture
            self.set_exp['1:0'].p2_pct = self.set_exp['1:0'].p2_pct * (1 - mixture) + p2_ingame_pct * mixture

            self.set_exp['1:1'].p1_pct = self.set_exp['1:1'].p1_pct * (1 - mixture) + p1_ingame_pct * mixture
            self.set_exp['1:1'].p2_pct = self.set_exp['1:1'].p2_pct * (1 - mixture) + p2_ingame_pct * mixture

            self.set_exp['0:1'].p1_pct = self.set_exp['0:1'].p1_pct * (1 - mixture) + p1_ingame_pct * mixture
            self.set_exp['0:1'].p2_pct = self.set_exp['0:1'].p2_pct * (1 - mixture) + p2_ingame_pct * mixture

        # for set 1 end
        set1_length = self.points_played[0].split(';').__len__()
        if set1_length % 2 == 1:
            next_set_server = 2
        else:
            next_set_server = 1

        # tiebreak
        if self.points_played[0].__contains__('/'):
            if self.points_played[0].split(';')[12].split('/').__len__() % 2 == 1:
                if self.points_played[0][self.points_played[0].__len__()-1] == 'S' or self.points_played[0][self.points_played[0].__len__()-1] == 'A':
                    set_score = '1:0'
                else:
                    set_score = '0:1'
            else:
                if self.points_played[0][self.points_played[0].__len__() - 1] == 'S' or self.points_played[0][self.points_played[0].__len__() - 1] == 'A':
                    set_score = '0:1'
                else:
                    set_score = '1:0'
        else:
            if self.points_played[0].split(';').__len__() % 2 == 1:
                if self.points_played[0][self.points_played[0].__len__() - 1] == 'S' or self.points_played[0][self.points_played[0].__len__() - 1] == 'A':
                    set_score = '1:0'
                else:
                    set_score = '0:1'
            else:
                if self.points_played[0][self.points_played[0].__len__() - 1] == 'S' or self.points_played[0][self.points_played[0].__len__() - 1] == 'A':
                    set_score = '0:1'
                else:
                    set_score = '1:0'

        if model == 'set_iid_model':
            self.model = SetIIDModelSetend(self.match_exp, self.set_exp, self.game_exp, self.point_exp, set_score, next_set_server, 3)
        elif model == 'match_iid_model':
            self.model = MatchIIDModelSetend(self.match_exp, self.set_exp, self.game_exp, self.point_exp, set_score, next_set_server, 3)

        self.match_score_prob = {}
        self.match_winner_prob = {}

    def predict_set_score(self):
        match_matrix = self.model.match_matrix()
        match_matrix = match_matrix[0]

        self.match_score_prob['2:0'] = np.sum(match_matrix[2][0])
        self.match_score_prob['2:1'] = np.sum(match_matrix[2][1])
        self.match_score_prob['0:2'] = np.sum(match_matrix[0][2])
        self.match_score_prob['1:2'] = np.sum(match_matrix[1][2])

        self.match_winner_prob['p1'] = self.match_score_prob['2:0'] + self.match_score_prob['2:1']
        self.match_winner_prob['p2'] = self.match_score_prob['0:2'] + self.match_score_prob['1:2']

    def calculate_exp(self, p1, p2, bo=5, ts=False):
        self.match_exp = PredictionStats(p1.match_baseline, p1.match_impact, p2.match_baseline, p2.match_impact)
        if ts:
            self.match_exp = PredictionStats(p1.match_baseline_ts, p1.match_impact_ts, p2.match_baseline_ts, p2.match_impact_ts)

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