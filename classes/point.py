class Point:

    def __init__(self, point_number, point_server, point_winner, game_winner, set_winner, p1_score, p2_score):
        self.point_number = point_number
        self.point_server = point_server
        self.point_winner = point_winner
        self.game_winner = game_winner
        self.set_winner = set_winner
        self.p1_score = p1_score
        self.p2_score = p2_score


class PointStats:

    def __init__(self, points_won):
        self.p1_serv = points_won[0]
        self.p1_serv_w = points_won[1]
        self.p2_serv = points_won[2]
        self.p2_serv_w = points_won[3]
        self.p1_retn = self.p2_serv
        self.p1_retn_w = self.p2_serv - self.p2_serv_w
        self.p2_retn = self.p1_serv
        self.p2_retn_w = self.p1_serv - self.p1_serv_w

        if self.p1_serv == 0:
            self.p1_serv_pct = float('nan')
        else:
            self.p1_serv_pct = float(self.p1_serv_w) / self.p1_serv
        if self.p1_retn == 0:
            self.p1_retn_pct = float('nan')
        else:
            self.p1_retn_pct = float(self.p1_retn_w) / self.p1_retn
        if self.p2_serv == 0:
            self.p2_serv_pct = float('nan')
        else:
            self.p2_serv_pct = float(self.p2_serv_w) / self.p2_serv
        if self.p2_retn == 0:
            self.p2_retn_pct = float('nan')
        else:
            self.p2_retn_pct = float(self.p2_retn_w) / self.p2_retn
