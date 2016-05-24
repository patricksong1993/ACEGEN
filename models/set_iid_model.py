import predictor


class SetIIDModel():

    def __init__(self, match_exp, set_exp, game_exp, point_exp, bo=5):
        self.match_exp = match_exp
        self.set_exp = set_exp
        self.bo = bo

    def match_matrix(self):
        win_set_p1_sf = {}
        win_set_p2_sf = {}
        for set in self.set_exp:
            win_set_p1_sf[set] = predictor.set_only_iid(self.set_exp[set].p1_pct, self.set_exp[set].p1_pct_std, self.set_exp[set].p2_pct, self.set_exp[set].p2_pct_std)
            win_set_p2_sf[set] = predictor.set_only_iid(self.set_exp[set].p2_pct, self.set_exp[set].p2_pct_std, self.set_exp[set].p1_pct, self.set_exp[set].p1_pct_std)

        if self.bo == 5:
            match_matrix = [[0] * 4 for i in range(4)]
            # p1 serve first, p2 serve first
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
        elif self.bo == 3:
            match_matrix = [[0] * 3 for i in range(3)]
            match_matrix[0][0] = [0.5, 0.5]
            match_matrix_length = [[0] * 3 for i in range(3)]
            match_matrix_length[0][0] = [{0: 0.5}, {0: 0.5}]
            for i in range(2):
                for j in range(2):
                    if match_matrix[i + 1][j] == 0:
                        match_matrix[i + 1][j] = [0, 0]
                    if match_matrix[i][j + 1] == 0:
                        match_matrix[i][j + 1] = [0, 0]

                    if match_matrix_length[i + 1][j] == 0:
                        match_matrix_length[i + 1][j] = [{}, {}]
                    if match_matrix_length[i][j + 1] == 0:
                        match_matrix_length[i][j + 1] = [{}, {}]

                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][1] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][2]
                    populate_length(match_matrix_length[i + 1][j][0], match_matrix_length[i][j][0], win_set_p1_sf[str(i) + ':' + str(j)][5])
                    populate_length(match_matrix_length[i + 1][j][0], match_matrix_length[i][j][1], win_set_p2_sf[str(i) + ':' + str(j)][6])

                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][0] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][3]
                    populate_length(match_matrix_length[i + 1][j][1], match_matrix_length[i][j][0], win_set_p1_sf[str(i) + ':' + str(j)][4])
                    populate_length(match_matrix_length[i + 1][j][1], match_matrix_length[i][j][1], win_set_p2_sf[str(i) + ':' + str(j)][7])

                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][3] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][0]
                    populate_length(match_matrix_length[i][j + 1][0], match_matrix_length[i][j][0], win_set_p1_sf[str(i) + ':' + str(j)][7])
                    populate_length(match_matrix_length[i][j + 1][0], match_matrix_length[i][j][1], win_set_p2_sf[str(i) + ':' + str(j)][4])

                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * win_set_p1_sf[str(i) + ':' + str(j)][2] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[str(i) + ':' + str(j)][1]
                    populate_length(match_matrix_length[i][j + 1][1], match_matrix_length[i][j][0], win_set_p1_sf[str(i) + ':' + str(j)][6])
                    populate_length(match_matrix_length[i][j + 1][1], match_matrix_length[i][j][1], win_set_p2_sf[str(i) + ':' + str(j)][5])

        return [match_matrix, match_matrix_length]

def populate_length(cur_length, pre_length, set_length):
    for p in pre_length:
        for s in set_length:
            cur_length[p+s] = cur_length.get(p+s, 0)+pre_length[p]*set_length[s]
