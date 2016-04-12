import utils.db_conn as db_conn
from classes.point import *


class Match:

    cached_matches = {}

    def __init__(self, match_id, year, tournament, match_num, player1, player2, points=0):
        self.match_id = match_id
        self.year = year
        self.tournament = tournament
        self.match_num = match_num
        self.player1 = player1
        self.player2 = player2

        Match.cached_matches[match_id] = self

        # grand slam db
        if points == 0:
            # getting all the points
            self.points = self.point_builder(db_conn.match_points(match_id))

            match_points_won = self.match_pw()
            self.match_pct = PointStats(match_points_won)

            self.set_pct = {}
            set_points_won = self.set_pw()
            for score in set_points_won:
                self.set_pct[score] = PointStats(set_points_won[score])

            self.game_pct = {}
            game_points_won = self.game_pw()
            for break_game in game_points_won:
                self.game_pct[break_game] = PointStats(game_points_won[break_game])

            self.point_pct = {}
            point_points_won = self.point_pw()
            for score in point_points_won:
                self.point_pct[score] = PointStats(point_points_won[score])
        # non grand slam db
        else:
            self.points = points

            match_points_won = self.match_pw_pbp()
            self.match_pct = PointStats(match_points_won)

            self.set_pct = {}
            set_points_won = self.set_pw_pbp()
            for score in set_points_won:
                self.set_pct[score] = PointStats(set_points_won[score])

            self.game_pct = {}
            game_points_won = self.game_pw_pbp()
            for break_game in game_points_won:
                self.game_pct[break_game] = PointStats(game_points_won[break_game])

            self.point_pct = {}
            point_points_won = self.point_pw_pbp()
            for score in point_points_won:
                self.point_pct[score] = PointStats(point_points_won[score])


    def point_builder(self, points_data):
        points = []
        for row in points_data:
            point = Point(row[7], row[9], row[8], row[6], row[4], row[12], row[13])
            points.append(point)
        return points

    def match_pw(self):
        p1_serv = 0
        p1_serv_w = 0
        p2_serv = 0
        p2_serv_w = 0

        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if point.point_server == 1:
                p1_serv += 1
                if point.point_winner == 1:
                    p1_serv_w += 1
            elif point.point_server == 2:
                p2_serv += 1
                if point.point_winner == 2:
                    p2_serv_w += 1

        return [p1_serv, p1_serv_w, p2_serv, p2_serv_w]


    def match_pw_pbp(self):
        p1_serv = 0
        p1_serv_w = 0
        p2_serv = 0
        p2_serv_w = 0

        point_server = 1
        tie_break = False
        tie_break_server = 0
        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if point == ';':
                point_server = 3-point_server
            elif point == '/':
                if not tie_break:
                    tie_break = True
                    tie_break_server = 3-point_server
                else:
                    tie_break_server = 3-tie_break_server
            elif point == '.':
                point_server = 3-point_server
                tie_break = False
                tie_break_server = 0
            else:
                if not tie_break:
                    if point_server == 1:
                        p1_serv += 1
                        if point == 'S' or point == 'A':
                            p1_serv_w += 1
                    if point_server == 2:
                        p2_serv += 1
                        if point == 'S' or point == 'A':
                            p2_serv_w += 1
                else:
                    if tie_break_server == 1:
                        p1_serv += 1
                        if point == 'S' or point == 'A':
                            p1_serv_w += 1
                    if tie_break_server == 2:
                        p2_serv += 1
                        if point == 'S' or point == 'A':
                            p2_serv_w += 1

        return [p1_serv, p1_serv_w, p2_serv, p2_serv_w]



    def set_pw(self):
        set_pcts = {}
        score = [0, 0]
        p1_serv = 0
        p1_serv_w = 0
        p2_serv = 0
        p2_serv_w = 0

        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if point.point_server == 1:
                p1_serv += 1
                if point.point_winner == 1:
                    p1_serv_w += 1
            elif point.point_server == 2:
                p2_serv += 1
                if point.point_winner == 2:
                    p2_serv_w += 1
            if point.set_winner != 0:
                # checking for wrong data points on tie break set
                # if score[0] == 3 or score[1] == 3:
                # print 'wrong data?'
                # print point
                set_pcts[str(score[0]) + ":" + str(score[1])] = [p1_serv, p1_serv_w, p2_serv, p2_serv_w]
                if point.set_winner == 1:
                    score[0] += 1
                elif point.set_winner == 2:
                    score[1] += 1
                p1_serv = 0
                p1_serv_w = 0
                p2_serv = 0
                p2_serv_w = 0

        return set_pcts

    def set_pw_pbp(self):
        set_pcts = {}
        score = [0, 0]
        p1_serv = 0
        p1_serv_w = 0
        p2_serv = 0
        p2_serv_w = 0
        prev_point = 0

        point_server = 1
        tie_break = False
        tie_break_server = 0

        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if point == ';':
                point_server = 3 - point_server
            elif point == '/':
                if not tie_break:
                    tie_break = True
                    tie_break_server = 3 - point_server
                else:
                    tie_break_server = 3 - tie_break_server
            elif point == '.':
                set_pcts[str(score[0]) + ":" + str(score[1])] = [p1_serv, p1_serv_w, p2_serv, p2_serv_w]
                if prev_point == 'S' or prev_point == 'A':
                    if tie_break:
                        score[tie_break_server-1] += 1
                    else:
                        score[point_server-1] += 1
                elif prev_point == 'R' or prev_point == 'D':
                    # opponent of server win set
                    if tie_break:
                        score[2-tie_break_server] += 1
                    else:
                        score[2-point_server] += 1
                point_server = 3 - point_server
                tie_break = False
                tie_break_server = 0
                p1_serv = 0
                p1_serv_w = 0
                p2_serv = 0
                p2_serv_w = 0
            else:
                if not tie_break:
                    if point_server == 1:
                        p1_serv += 1
                        if point == 'S' or point == 'A':
                            p1_serv_w += 1
                    if point_server == 2:
                        p2_serv += 1
                        if point == 'S' or point == 'A':
                            p2_serv_w += 1
                else:
                    if tie_break_server == 1:
                        p1_serv += 1
                        if point == 'S' or point == 'A':
                            p1_serv_w += 1
                    if tie_break_server == 2:
                        p2_serv += 1
                        if point == 'S' or point == 'A':
                            p2_serv_w += 1

            prev_point = point

        # for the last set
        set_pcts[str(score[0]) + ":" + str(score[1])] = [p1_serv, p1_serv_w, p2_serv, p2_serv_w]

        return set_pcts


    def game_pw(self):
        game_pcts = {}
        break_game = 0

        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if game_pcts.get(break_game, 0) == 0:
                # p1_serv, p1_serv_w, p2_serv, p2_serv_w
                game_pcts[break_game] = [0, 0, 0, 0]
            # counting serves and serve wins for p1 and p2
            if point.point_server == 1:
                game_pcts[break_game][0] += 1
                if point.point_winner == 1:
                    game_pcts[break_game][1] += 1
            elif point.point_server == 2:
                game_pcts[break_game][2] += 1
                if point.point_winner == 2:
                    game_pcts[break_game][3] += 1
            # check break game
            if point.point_server == 2 and point.game_winner == 1:
                break_game += 1
            if point.point_server == 1 and point.game_winner == 2:
                break_game -= 1
            # reset for a new set
            if point.set_winner != 0:
                break_game = 0

        return game_pcts

    def game_pw_pbp(self):
        game_pcts = {}
        break_game = 0

        point_server = 1
        tie_break = False
        tie_break_server = 0

        prev_point = 0
        # assume data point are semi-perfect, no point server is non-zero but point winner is zero
        for point in self.points:
            if game_pcts.get(break_game, 0) == 0:
                # p1_serv, p1_serv_w, p2_serv, p2_serv_w
                game_pcts[break_game] = [0, 0, 0, 0]


            if point == ';':
                if prev_point == 'R' or prev_point == 'D':
                    if point_server == 1:
                        break_game -= 1
                    elif point_server == 2:
                        break_game += 1
                point_server = 3 - point_server

            elif point == '/':
                if not tie_break:
                    tie_break = True
                    tie_break_server = 3 - point_server
                else:
                    tie_break_server = 3 - tie_break_server
            elif point == '.':
                break_game = 0
                point_server = 3 - point_server
                tie_break = False
                tie_break_server = 0
            else:
                if not tie_break:
                    if point_server == 1:
                        game_pcts[break_game][0] += 1
                        if point == 'S' or point == 'A':
                            game_pcts[break_game][1] += 1
                    if point_server == 2:
                        game_pcts[break_game][2] += 1
                        if point == 'S' or point == 'A':
                            game_pcts[break_game][3] += 1
                else:
                    if tie_break_server == 1:
                        game_pcts[break_game][0] += 1
                        if point == 'S' or point == 'A':
                            game_pcts[break_game][1] += 1
                    if tie_break_server == 2:
                        game_pcts[break_game][2] += 1
                        if point == 'S' or point == 'A':
                            game_pcts[break_game][3] += 1

            prev_point = point

        return game_pcts

    def point_pw(self):
        point_pcts = {}
        prev_point = Point(0, 0, 0, 0, 0, '0', '0')

        for point in self.points:
            if point.point_winner == '0' or point.point_winner == '':
                prev_point = point
                continue
            if point.p1_score in ['0', '15', '30', '40', 'AD'] and point.p2_score in ['0', '15', '30', '40', 'AD'] \
                    and prev_point.p1_score in ['0', '15', '30', '40', 'AD'] and prev_point.p2_score in ['0', '15',
                                                                                                         '30', '40',
                                                                                                         'AD']:
                if prev_point.p1_score == '':
                    scores = '0:0'
                else:
                    scores = prev_point.p1_score + ':' + prev_point.p2_score
                if point_pcts.get(scores, 0) == 0:
                    point_pcts[scores] = [0, 0, 0, 0]
                if point.point_server == 1:
                    point_pcts[scores][0] += 1
                    if point.point_winner == 1:
                        point_pcts[scores][1] += 1
                elif point.point_server == 2:
                    point_pcts[scores][2] += 1
                    if point.point_winner == 2:
                        point_pcts[scores][3] += 1
                prev_point = point

        return point_pcts

    def point_pw_pbp(self):
        point_pcts = {}

        point_server = 1
        games_in_set = 0
        score = ['0','0']

        for point in self.points:
            #tie-break is not considered
            if games_in_set > 11 and point != '.':
                continue

            if point_pcts.get(score[0]+':'+score[1], 0) == 0:
                # p1_serv, p1_serv_w, p2_serv, p2_serv_w
                point_pcts[score[0]+':'+score[1]] = [0, 0, 0, 0]
            if point == ';':
                games_in_set += 1
                score = ['0','0']
                point_server = 3 - point_server
            elif point == '.':
                games_in_set = 0
                point_server = 3 - point_server
            else:
                if point_server == 1:
                    point_pcts[score[0]+':'+score[1]][0] += 1
                    if point == 'S' or point == 'A':
                        point_pcts[score[0]+':'+score[1]][1] += 1
                        score = increment_score(score, 1)
                    else:
                        score = increment_score(score, 2)
                if point_server == 2:
                    point_pcts[score[0]+':'+score[1]][2] += 1
                    if point == 'S' or point == 'A':
                        point_pcts[score[0]+':'+score[1]][3] += 1
                        score = increment_score(score, 2)
                    else:
                        score = increment_score(score, 1)

        return point_pcts

    @staticmethod
    def get_match(match_id):
        if Match.cached_matches.get(match_id, 0) == 0:
            attr = db_conn.match_attributes(match_id)
            Match.cached_matches[match_id] = Match(attr[0], attr[1], attr[2], attr[3], attr[4], attr[5])
        return Match.cached_matches[match_id]

    @staticmethod
    def get_match_pbp(match_id):
        if Match.cached_matches.get(match_id, 0) == 0:
            attr = db_conn.match_attributes_pbp(match_id)
            Match.cached_matches[match_id] = Match(attr[0], attr[1], attr[2], attr[3], attr[5], attr[6], attr[8])
        return Match.cached_matches[match_id]

    @staticmethod
    def get_matches(match_ids):
        matches = {}
        for match_id in match_ids:
            matches[match_id] = Match.get_match(match_id)
        return matches


    @staticmethod
    def get_matches_pbp(match_ids):
        matches = {}
        for match_id in match_ids:
            matches[match_id] = Match.get_match_pbp(match_id)
        return matches


def increment_score(score, player):
    if score[0] == '40' and score[1] == '40':
        if player == 1:
            return ['AD','40']
        else:
            return ['40','AD']
    elif score[0] == 'AD' and score[1] == '40':
        if player == 2:
            return ['40', '40']
    elif score[0] == '40' and score[1] == 'AD':
        if player == 1:
            return ['40', '40']
    elif player == 1:
        if score[0] == '0':
            return ['15', score[1]]
        if score[0] == '15':
            return ['30', score[1]]
        if score[0] == '30':
            return ['40', score[1]]
        if score[0] == '40':
            return ['0', '0']
    elif player == 2:
        if score[1] == '0':
            return [score[0], '15']
        if score[1] == '15':
            return [score[0], '30']
        if score[1] == '30':
            return [score[0], '40']
        if score[1] == '40':
            return ['0', '0']
    return ['0', '0']

