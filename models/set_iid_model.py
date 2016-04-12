import predictor


class SetIIDModel():

    def __init__(self, match_exp, set_exp, game_exp, point_exp):
        self.match_exp = match_exp
        self.set_exp = set_exp

    def match_matrix(self):
        win_set_p1_sf = {}
        win_set_p2_sf = {}
        for set in self.set_exp:
            win_set_p1_sf[set] = predictor.set_only_iid(self.set_exp[set].p1_pct, self.set_exp[set].p1_pct_std, self.set_exp[set].p2_pct, self.set_exp[set].p2_pct_std)
            win_set_p2_sf[set] = predictor.set_only_iid(self.set_exp[set].p2_pct, self.set_exp[set].p2_pct_std, self.set_exp[set].p1_pct, self.set_exp[set].p1_pct_std)

        match_matrix = [[0] * 4 for i in range(4)]
        match_matrix[0][0] = [0.5, 0.5]
        for i in range(3):
            for j in range(3):
                if match_matrix[i + 1][j] == 0:
                    match_matrix[i + 1][j] = [0, 0]
                if match_matrix[i][j + 1] == 0:
                    match_matrix[i][j + 1] = [0, 0]
                match_matrix[i + 1][j][0] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][1] + \
                                             match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][2]
                match_matrix[i + 1][j][1] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][0] + \
                                             match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][3]
                match_matrix[i][j + 1][0] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][3] + \
                                             match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][0]
                match_matrix[i][j + 1][1] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][2] + \
                                             match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][1]

        return match_matrix