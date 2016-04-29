import predictor


class MatchIIDModel():

    def __init__(self, match_exp, set_exp, game_exp, point_exp, bo=5):
        self.match_exp = match_exp
        self.bo = bo

    def match_matrix(self):
        win_set_p1_sf = predictor.set_only_iid(self.match_exp.p1_pct, self.match_exp.p1_pct_std, self.match_exp.p2_pct, self.match_exp.p2_pct_std)
        win_set_p2_sf = predictor.set_only_iid(self.match_exp.p2_pct, self.match_exp.p2_pct_std, self.match_exp.p1_pct, self.match_exp.p1_pct_std)

        if self.bo == 5:
            match_matrix = [[0] * 4 for i in range(4)]
            match_matrix[0][0] = [0.5, 0.5]
            for i in range(3):
                for j in range(3):
                    if match_matrix[i + 1][j] == 0:
                        match_matrix[i + 1][j] = [0, 0]
                    if match_matrix[i][j + 1] == 0:
                        match_matrix[i][j + 1] = [0, 0]
                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * win_set_p1_sf[1] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[2]
                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * win_set_p1_sf[0] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[3]
                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * win_set_p1_sf[3] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[0]
                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * win_set_p1_sf[2] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[1]
        elif self.bo == 3:
            match_matrix = [[0] * 3 for i in range(3)]
            match_matrix[0][0] = [0.5, 0.5]
            for i in range(2):
                for j in range(2):
                    if match_matrix[i + 1][j] == 0:
                        match_matrix[i + 1][j] = [0, 0]
                    if match_matrix[i][j + 1] == 0:
                        match_matrix[i][j + 1] = [0, 0]
                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * win_set_p1_sf[1] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[2]
                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * win_set_p1_sf[0] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[3]
                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * win_set_p1_sf[3] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[0]
                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * win_set_p1_sf[2] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[1]

        return match_matrix