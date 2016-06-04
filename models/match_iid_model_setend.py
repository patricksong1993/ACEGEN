import predictor
from utils.model_utils import populate_length

class MatchIIDModelSetend():

    def __init__(self, match_exp, set_exp, game_exp, point_exp, set_score, next_set_server, bo=5):
        self.match_exp = match_exp
        self.bo = bo

        self.set_score = set_score
        self.next_set_server = next_set_server

    def match_matrix(self):
        win_set_p1_sf = predictor.set_only_iid(self.match_exp.p1_pct, self.match_exp.p1_pct_std, self.match_exp.p2_pct, self.match_exp.p2_pct_std)
        win_set_p2_sf = predictor.set_only_iid(self.match_exp.p2_pct, self.match_exp.p2_pct_std, self.match_exp.p1_pct, self.match_exp.p1_pct_std)

        if self.bo == 3:
            match_matrix = [[0] * 3 for i in range(3)]
            match_matrix[0][0] = [0.5, 0.5]

            if self.set_score == '1:0':
                if self.next_set_server == 1:
                    match_matrix[1][0] = [1, 0]
                else:
                    match_matrix[1][0] = [0, 1]
                match_matrix[0][1] = [0, 0]
            elif self.set_score == '0:1':
                if self.next_set_server == 1:
                    match_matrix[0][1] = [1, 0]
                else:
                    match_matrix[0][1] = [0, 1]
                match_matrix[1][0] = [0, 0]
            elif self.set_score == '1:1':
                if self.next_set_server == 1:
                    match_matrix[1][1] = [1, 0]
                else:
                    match_matrix[1][1] = [0, 1]
                match_matrix[2][0] = [0, 0]
                match_matrix[0][2] = [0, 0]

            for i in range(2):
                for j in range(2):
                    if self.set_score == '1:0' or self.set_score == '0:1':
                        if i == 0 and j == 0:
                            continue
                    elif self.set_score == '1:1':
                        if (i == 0 and j == 0) or (i == 1 and j == 0) or (i == 0 and j == 1):
                            continue

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

        return [match_matrix, 0]