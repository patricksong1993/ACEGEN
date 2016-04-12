def set_only_iid(p1_serv, p1_serv_std, p2_serv, p2_serv_std):
    # assume p1 serve first
    p1_win_game_pct = iid_win_game(p1_serv)
    p2_win_game_pct = iid_win_game(p2_serv)
    set_matrix = [[0] * 7 for i in range(7)]
    set_matrix[0][0] = 1
    # i is p1 score, j is p2 score
    # i+j % 2 == 1, p1 served last game
    for i in range(7):
        for j in range(7):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                if j % 2 == 0:
                    set_matrix[0][j] = set_matrix[0][j - 1] * p2_win_game_pct
                else:
                    set_matrix[0][j] = set_matrix[0][j - 1] * (1 - p1_win_game_pct)
            elif j == 0:
                if i % 2 == 0:
                    set_matrix[i][0] = set_matrix[i - 1][0] * (1 - p2_win_game_pct)
                else:
                    set_matrix[i][0] = set_matrix[i - 1][0] * p1_win_game_pct
            elif i == 6 and j != 6:
                if (i + j) % 2 == 0:
                    set_matrix[6][j] = set_matrix[5][j] * (1 - p2_win_game_pct)
                else:
                    set_matrix[6][j] = set_matrix[5][j] * p1_win_game_pct
            elif j == 6 and i != 6:
                if (i + j) % 2 == 0:
                    set_matrix[i][6] = set_matrix[i][5] * p2_win_game_pct
                else:
                    set_matrix[i][6] = set_matrix[i][5] * (1 - p1_win_game_pct)
            else:
                # including i == 6 and j == 6
                if (i + j) % 2 == 0:
                    set_matrix[i][j] = set_matrix[i][j - 1] * p2_win_game_pct + set_matrix[i - 1][j] * (
                        1 - p2_win_game_pct)
                else:
                    set_matrix[i][j] = set_matrix[i][j - 1] * (1 - p1_win_game_pct) + set_matrix[i - 1][
                                                                                          j] * p1_win_game_pct

    # 7-5 5-7
    set_7_5 = set_matrix[6][5] * (1 - p2_win_game_pct)
    set_5_7 = set_matrix[5][6] * p2_win_game_pct
    # 6-6
    # hacky, unfinished on tiebreak
    set_7_6 = set_matrix[6][6] * p1_serv / (p1_serv + p2_serv)
    set_6_7 = set_matrix[6][6] * p2_serv / (p1_serv + p2_serv)

    p1_win_odd = set_matrix[6][1] + set_matrix[6][3] + set_7_6
    p1_win_even = set_matrix[6][0] + set_matrix[6][2] + set_matrix[6][4] + set_7_5
    p2_win_odd = set_matrix[1][6] + set_matrix[3][6] + set_6_7
    p2_win_even = set_matrix[0][6] + set_matrix[2][6] + set_matrix[4][6] + set_5_7

    return [p1_win_odd, p1_win_even, p2_win_odd, p2_win_even]



def iid_win_game(serv_pct):
    return (serv_pct ** 4) * (1 + 4 * (1 - serv_pct) + 10 * (1 - serv_pct) ** 2) + (20 * (
    serv_pct * (1 - serv_pct)) ** 3) * (serv_pct ** 2) * ((1 - 2 * serv_pct * (1 - serv_pct)) ** (-1))
