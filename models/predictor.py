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
    set_7_6 = set_matrix[6][6] * tiebreak(p1_serv, p2_serv)
    set_6_7 = set_matrix[6][6] * (1-tiebreak(p1_serv, p2_serv))

    p1_win_odd = set_matrix[6][1] + set_matrix[6][3] + set_7_6
    p1_win_even = set_matrix[6][0] + set_matrix[6][2] + set_matrix[6][4] + set_7_5
    p2_win_odd = set_matrix[1][6] + set_matrix[3][6] + set_6_7
    p2_win_even = set_matrix[0][6] + set_matrix[2][6] + set_matrix[4][6] + set_5_7

    p1_win_odd_length = {7: set_matrix[6][1], 9: set_matrix[6][3], 13: set_7_6}
    p1_win_even_length = {6: set_matrix[6][0], 8: set_matrix[6][2], 10: set_matrix[6][4], 12: set_7_5}
    p2_win_odd_length = {7: set_matrix[1][6], 9: set_matrix[3][6], 13: set_6_7}
    p2_win_even_length = {6: set_matrix[0][6], 8: set_matrix[2][6], 10: set_matrix[4][6], 12: set_5_7}

    return [p1_win_odd, p1_win_even, p2_win_odd, p2_win_even, p1_win_odd_length, p1_win_even_length, p2_win_odd_length, p2_win_even_length]


def game_only_idd(p1_game_pct, p1_game_pct_std, p2_game_pct, p2_game_pct_std):
    # assume p1 serve first
    set_matrix = [[0] * 7 for i in range(7)]
    set_matrix[0][0] = 1
    # i is p1 score, j is p2 score
    # i+j % 2 == 1, p1 served last game
    # score is wrt to p1, check!
    p1_win_game_pct = {}
    p2_win_game_pct = {}
    for break_num in p1_game_pct:
        p1_win_game_pct[break_num] = iid_win_game(p1_game_pct[break_num])
        p2_win_game_pct[break_num] = iid_win_game(p2_game_pct[break_num])

    for i in range(7):
        for j in range(7):
            p1_temp_game_pct = p1_win_game_pct[(i - j) / 2]
            p2_temp_game_pct = p2_win_game_pct[(1 + j - i) / 2]
            if i == 0 and j == 0:
                continue
            elif i == 0:
                if j % 2 == 0:
                    set_matrix[0][j] = set_matrix[0][j - 1] * p2_temp_game_pct
                else:
                    set_matrix[0][j] = set_matrix[0][j - 1] * (1 - p1_temp_game_pct)
            elif j == 0:
                if i % 2 == 0:
                    set_matrix[i][0] = set_matrix[i - 1][0] * (1 - p2_temp_game_pct)
                else:
                    set_matrix[i][0] = set_matrix[i - 1][0] * p1_temp_game_pct
            elif i == 6 and j != 6:
                if (i + j) % 2 == 0:
                    set_matrix[6][j] = set_matrix[5][j] * (1 - p2_temp_game_pct)
                else:
                    set_matrix[6][j] = set_matrix[5][j] * p1_temp_game_pct
            elif j == 6 and i != 6:
                if (i + j) % 2 == 0:
                    set_matrix[i][6] = set_matrix[i][5] * p2_temp_game_pct
                else:
                    set_matrix[i][6] = set_matrix[i][5] * (1 - p1_temp_game_pct)
            else:
                # including i == 6 and j == 6
                if (i + j) % 2 == 0:
                    set_matrix[i][j] = set_matrix[i][j - 1] * p2_temp_game_pct + set_matrix[i - 1][j] * (
                        1 - p2_temp_game_pct)
                else:
                    set_matrix[i][j] = set_matrix[i][j - 1] * (1 - p1_temp_game_pct) + set_matrix[i - 1][
                                                                                           j] * p1_temp_game_pct
    # 7-5 5-7
    set_7_5 = set_matrix[6][5] * (1 - p2_win_game_pct[0])
    set_5_7 = set_matrix[5][6] * p2_win_game_pct[1]
    # 6-6
    # hacky, unfinished on tiebreak
    set_7_6 = set_matrix[6][6] * tiebreak(p1_game_pct[0], p2_game_pct[0])
    set_6_7 = set_matrix[6][6] * (1-tiebreak(p1_game_pct[0], p2_game_pct[0]))

    p1_win_odd = set_matrix[6][1] + set_matrix[6][3] + set_7_6
    p1_win_even = set_matrix[6][0] + set_matrix[6][2] + set_matrix[6][4] + set_7_5
    p2_win_odd = set_matrix[1][6] + set_matrix[3][6] + set_6_7
    p2_win_even = set_matrix[0][6] + set_matrix[2][6] + set_matrix[4][6] + set_5_7

    total_prob = p1_win_odd + p1_win_even + p2_win_odd + p2_win_even

    p1_win_odd_length = {7: set_matrix[6][1]/total_prob, 9: set_matrix[6][3]/total_prob, 13: set_7_6/total_prob}
    p1_win_even_length = {6: set_matrix[6][0]/total_prob, 8: set_matrix[6][2]/total_prob, 10: set_matrix[6][4]/total_prob, 12: set_7_5/total_prob}
    p2_win_odd_length = {7: set_matrix[1][6]/total_prob, 9: set_matrix[3][6]/total_prob, 13: set_6_7/total_prob}
    p2_win_even_length = {6: set_matrix[0][6]/total_prob, 8: set_matrix[2][6]/total_prob, 10: set_matrix[4][6]/total_prob, 12: set_5_7/total_prob}

    return [p1_win_odd / total_prob, p1_win_even / total_prob, p2_win_odd / total_prob, p2_win_even / total_prob, p1_win_odd_length, p1_win_even_length, p2_win_odd_length, p2_win_even_length]


def tiebreak(p1_serv, p2_serv):
    # assuming p1 serve first as the whole set
    tiebreak_matrix = [[0] * 7 for i in range(7)]
    tiebreak_matrix[0][0] = 1

    for i in range(7):
        for j in range(7):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                if (i+j) in [1,4,5,8,9,12]:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j-1] * (1-p1_serv)
                else:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j - 1] * p2_serv
            elif j == 0:
                if (i + j) in [1, 4, 5, 8, 9, 12]:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i-1][j] * p1_serv
                else:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i-1][j] * (1-p2_serv)
            elif i == 6 and j != 6:
                if (i + j) in [1, 4, 5, 8, 9, 12]:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i-1][j] * p1_serv
                else:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i-1][j] * (1-p2_serv)
            elif j == 6 and i != 6:
                if (i + j) in [1, 4, 5, 8, 9, 12]:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j-1] * (1-p1_serv)
                else:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j-1] * p2_serv
            else:
                if (i + j) in [1, 4, 5, 8, 9, 12]:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j-1] * (1 - p1_serv)+tiebreak_matrix[i-1][j]*p1_serv
                else:
                    tiebreak_matrix[i][j] = tiebreak_matrix[i][j - 1] * p2_serv+tiebreak_matrix[i-1][j] * (1-p2_serv)
            p1_win_on_66 = p1_serv*(1-p2_serv)/(1-p1_serv*p2_serv-(1-p1_serv)*(1-p2_serv))

    p1_win_tb = tiebreak_matrix[6][0]+tiebreak_matrix[6][1]+tiebreak_matrix[6][2]+tiebreak_matrix[6][3]+tiebreak_matrix[6][4]+tiebreak_matrix[6][5]+tiebreak_matrix[6][6]*p1_win_on_66
    p2_win_tb = tiebreak_matrix[0][6] + tiebreak_matrix[1][6] + tiebreak_matrix[2][6] + tiebreak_matrix[3][6] + tiebreak_matrix[4][6] + tiebreak_matrix[5][6] + tiebreak_matrix[6][
                                                                                                                                                                    6] * (1-p1_win_on_66)
    return p1_win_tb/(p1_win_tb+p2_win_tb)


def point_win_game(point_exp):
    situation = {}
    end = {}
    situation['0:0'] = 1

    situation['15:0'] = situation['0:0']*point_exp['0:0']
    situation['0:15'] = situation['0:0']*(1-point_exp['0:0'])

    situation['15:15'] = situation['15:0'] * (1 - point_exp['15:0'])+situation['0:15'] * point_exp['0:15']
    situation['30:0'] = situation['15:0'] * point_exp['15:0']
    situation['0:30'] = situation['0:15'] * (1 - point_exp['0:15'])

    situation['30:15'] = situation['15:15'] * point_exp['15:15'] + situation['30:0'] * (1-point_exp['30:0'])
    situation['15:30'] = situation['15:15'] * (1 - point_exp['15:15'])+situation['0:30'] * point_exp['0:30']
    situation['40:0'] = situation['30:0'] * point_exp['30:0']
    situation['0:40'] = situation['0:30'] * (1 - point_exp['0:30'])

    situation['30:30'] = situation['15:30'] * point_exp['15:30'] + situation['30:15'] * (1 - point_exp['30:15'])
    situation['40:15'] = situation['30:15'] * point_exp['30:15'] + situation['40:0'] * (1-point_exp['40:0'])
    situation['15:40'] = situation['15:30'] * (1 - point_exp['15:30'])+situation['0:40'] * point_exp['0:40']
    end['40:0'] = situation['40:0'] * point_exp['40:0']
    end['0:40'] = situation['0:40'] * (1 - point_exp['0:40'])

    situation['40:30'] = situation['30:30'] * point_exp['30:30'] + situation['40:15'] * (1 - point_exp['40:15'])
    situation['30:40'] = situation['15:40'] * point_exp['15:40'] + situation['30:30'] * (1 - point_exp['30:30'])
    end['40:15'] = situation['40:15'] * point_exp['40:15']
    end['15:40'] = situation['15:40'] * (1 - point_exp['15:40'])

    situation['40:40'] = situation['30:40'] * point_exp['30:40'] + situation['40:30'] * (1 - point_exp['40:30'])
    end['40:30'] = situation['40:30'] * point_exp['40:30']
    end['30:40'] = situation['30:40'] * (1 - point_exp['30:40'])

    end['AD:40'] = situation['40:40'] * point_exp['40:40'] * point_exp['AD:40'] / (1-point_exp['40:40']*(1-point_exp['AD:40'])-(1-point_exp['40:40'])*point_exp['40:AD'])
    end['40:AD'] = situation['40:40'] * (1-point_exp['40:40']) * (1-point_exp['AD:40']) / (1-point_exp['40:40']*(1-point_exp['AD:40'])-(1-point_exp['40:40'])*point_exp['40:AD'])

    return end['40:0']+end['40:15']+end['40:30']+end['AD:40']/(end['40:0']+end['40:15']+end['40:30']+end['AD:40']+end['0:40']+end['15:40']+end['30:40']+end['40:AD'])


def point_win_set(p1_win_game_pct, p2_win_game_pct):
    # assume p1 serve first
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
    set_7_6 = set_matrix[6][6] * tiebreak(p1_win_game_pct, p2_win_game_pct)
    set_6_7 = set_matrix[6][6] * (1-tiebreak(p1_win_game_pct, p2_win_game_pct))

    p1_win_odd = set_matrix[6][1] + set_matrix[6][3] + set_7_6
    p1_win_even = set_matrix[6][0] + set_matrix[6][2] + set_matrix[6][4] + set_7_5
    p2_win_odd = set_matrix[1][6] + set_matrix[3][6] + set_6_7
    p2_win_even = set_matrix[0][6] + set_matrix[2][6] + set_matrix[4][6] + set_5_7

    p1_win_odd_length = {7: set_matrix[6][1], 9: set_matrix[6][3], 13: set_7_6}
    p1_win_even_length = {6: set_matrix[6][0], 8: set_matrix[6][2], 10: set_matrix[6][4], 12: set_7_5}
    p2_win_odd_length = {7: set_matrix[1][6], 9: set_matrix[3][6], 13: set_6_7}
    p2_win_even_length = {6: set_matrix[0][6], 8: set_matrix[2][6], 10: set_matrix[4][6], 12: set_5_7}

    return [p1_win_odd, p1_win_even, p2_win_odd, p2_win_even, p1_win_odd_length, p1_win_even_length, p2_win_odd_length, p2_win_even_length]


def iid_win_game(serv_pct):
    return (serv_pct ** 4) * (1 + 4 * (1 - serv_pct) + 10 * (1 - serv_pct) ** 2) + (20 * (
    serv_pct * (1 - serv_pct)) ** 3) * (serv_pct ** 2) * ((1 - 2 * serv_pct * (1 - serv_pct)) ** (-1))
