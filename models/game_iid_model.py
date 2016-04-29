import predictor


class GameIIDModel():

    def __init__(self, match_exp, set_exp, game_exp, point_exp, bo=5):
        self.game_exp = game_exp
        self.bo = bo

    def match_matrix(self):
        p1_game_pct = {}
        p2_game_pct = {}
        p1_game_pct_std = {}
        p2_game_pct_std = {}
        for game in self.game_exp:
            p1_game_pct[game] = self.game_exp[game].p1_pct
            p2_game_pct[game] = self.game_exp[game].p2_pct
            p1_game_pct_std[game] = self.game_exp[game].p1_pct_std
            p2_game_pct_std[game] = self.game_exp[game].p2_pct_std

        [p1_sf_p1_wo, p1_sf_p1_we, p1_sf_p2_wo, p1_sf_p2_we] = predictor.game_only_idd(p1_game_pct, p1_game_pct_std, p2_game_pct, p2_game_pct_std)

        # inverse score for p2 serve first
        p1_game_pct = {}
        p2_game_pct = {}
        p1_game_pct_std = {}
        p2_game_pct_std = {}
        for game in self.game_exp:
            p1_game_pct[inverse_score(game)] = self.game_exp[game].p1_pct
            p2_game_pct[inverse_score(game)] = self.game_exp[game].p2_pct
            p1_game_pct_std[inverse_score(game)] = self.game_exp[game].p1_pct_std
            p2_game_pct_std[inverse_score(game)] = self.game_exp[game].p2_pct_std
        [p2_sf_p2_wo, p2_sf_p2_we, p2_sf_p1_wo, p2_sf_p1_we] = predictor.game_only_idd(p2_game_pct, p2_game_pct_std, p1_game_pct, p1_game_pct_std)

        if self.bo == 5:
            match_matrix = [[0] * 4 for i in range(4)]
            match_matrix[0][0] = [0.5, 0.5]
            for i in range(3):
                for j in range(3):
                    if match_matrix[i + 1][j] == 0:
                        match_matrix[i + 1][j] = [0, 0]
                    if match_matrix[i][j + 1] == 0:
                        match_matrix[i][j + 1] = [0, 0]
                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * p1_sf_p1_we + \
                                                 match_matrix[i][j][1] * p2_sf_p1_wo
                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * p1_sf_p1_wo + \
                                                 match_matrix[i][j][1] * p2_sf_p1_we
                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * p1_sf_p2_we + \
                                                 match_matrix[i][j][1] * p2_sf_p2_wo
                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * p1_sf_p2_wo + \
                                                 match_matrix[i][j][1] * p2_sf_p2_we
        elif self.bo == 3:
            match_matrix = [[0] * 3 for i in range(3)]
            match_matrix[0][0] = [0.5, 0.5]
            for i in range(2):
                for j in range(2):
                    if match_matrix[i + 1][j] == 0:
                        match_matrix[i + 1][j] = [0, 0]
                    if match_matrix[i][j + 1] == 0:
                        match_matrix[i][j + 1] = [0, 0]
                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * p1_sf_p1_we + \
                                                 match_matrix[i][j][1] * p2_sf_p1_wo
                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * p1_sf_p1_wo + \
                                                 match_matrix[i][j][1] * p2_sf_p1_we
                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * p1_sf_p2_we + \
                                                 match_matrix[i][j][1] * p2_sf_p2_wo
                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * p1_sf_p2_wo + \
                                                 match_matrix[i][j][1] * p2_sf_p2_we

        return match_matrix

def inverse_score(score):
    if type(score) is str:
        scores = score.split(':')
        return scores[1] + ":" + scores[0]
    if type(score) is int:
        return 0 - score
