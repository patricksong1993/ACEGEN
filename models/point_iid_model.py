import predictor
from utils.model_utils import populate_length

class PointIIDModel():

    def __init__(self, match_exp, set_exp, game_exp, point_exp, bo=5):
        self.point_exp = point_exp
        self.bo = bo

    def match_matrix(self):
        p1_point_exp = {}
        p2_point_exp = {}
        for point in self.point_exp:
            p1_point_exp[point] = self.point_exp[point].p1_pct
            p2_point_exp[point] = self.point_exp[point].p2_pct

        p1_win_game_pct = predictor.point_win_game(p1_point_exp)
        p2_win_game_pct = predictor.point_win_game(p2_point_exp)

        win_set_p1_sf = predictor.point_win_set(p1_win_game_pct, p2_win_game_pct)
        win_set_p2_sf = predictor.point_win_set(p2_win_game_pct, p1_win_game_pct)

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

                    match_matrix[i + 1][j][0] += match_matrix[i][j][0] * win_set_p1_sf[1] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[2]
                    populate_length(match_matrix_length[i + 1][j][0], match_matrix_length[i][j][0], win_set_p1_sf[5])
                    populate_length(match_matrix_length[i + 1][j][0], match_matrix_length[i][j][1], win_set_p2_sf[6])

                    match_matrix[i + 1][j][1] += match_matrix[i][j][0] * win_set_p1_sf[0] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[3]
                    populate_length(match_matrix_length[i + 1][j][1], match_matrix_length[i][j][0], win_set_p1_sf[4])
                    populate_length(match_matrix_length[i + 1][j][1], match_matrix_length[i][j][1], win_set_p2_sf[7])

                    match_matrix[i][j + 1][0] += match_matrix[i][j][0] * win_set_p1_sf[3] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[0]
                    populate_length(match_matrix_length[i][j + 1][0], match_matrix_length[i][j][0], win_set_p1_sf[7])
                    populate_length(match_matrix_length[i][j + 1][0], match_matrix_length[i][j][1], win_set_p2_sf[4])

                    match_matrix[i][j + 1][1] += match_matrix[i][j][0] * win_set_p1_sf[2] + \
                                                 match_matrix[i][j][1] * win_set_p2_sf[1]
        populate_length(match_matrix_length[i][j + 1][1], match_matrix_length[i][j][0], win_set_p1_sf[6])
        populate_length(match_matrix_length[i][j + 1][1], match_matrix_length[i][j][1], win_set_p2_sf[5])

        return [match_matrix, match_matrix_length]