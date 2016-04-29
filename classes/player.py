from classes.match import Match
import numpy as np
from scipy import stats
import math as math
import utils.db_conn as db_conn
import tabulate


class Player:
    cached_players = {}
    start_year = 0
    end_year = 9999
    surface = 'hard'

    def __init__(self, name):
        self.name = name
        Player.cached_players[name] = self
        self.match_ids = 0

        # baselines
        self.match_baseline = 0
        self.set_baseline = {}
        self.set_baseline_3 = {}
        self.game_baseline = {}
        self.point_baseline = {}

        # impacts
        self.match_impact = 0
        self.set_impact = {}
        self.set_impact_3 = {}
        self.game_impact = {}
        self.point_impact = {}

        # # baseline diff against match level
        # self.match_baseline_diff = PlayerStats([0],[0])
        # self.set_baseline_diff = {}
        # self.set_baseline_diff_3 = {}
        # self.game_baseline_diff = {}
        # self.point_baseline_diff = {}
        #
        # # impact diff against match level
        # self.match_impact_diff = PlayerStats([0], [0])
        # self.set_impact_diff = {}
        # self.set_impact_diff_3 = {}
        # self.game_impact_diff = {}
        # self.point_impact_diff = {}

        self.enrich_matches()
        self.calculate_baseline()
        # self.calculate_baseline_diff()
        self.calculate_impact()
        # self.calculate_impact_diff()

    def print_table(self):
        print self.name
        print '--Baseline--'
        baselines = []
        baselines.append(['match', '', self.match_baseline.serv_counts, self.match_baseline.serv_mean,
                          self.match_baseline.serv_std, self.match_baseline.retn_counts,
                          self.match_baseline.retn_mean, self.match_baseline.retn_std])
        for set in self.set_baseline:
            baselines.append(['set', set, self.set_baseline[set].serv_counts, self.set_baseline[set].serv_mean,
                              self.set_baseline[set].serv_std, self.set_baseline[set].retn_counts,
                              self.set_baseline[set].retn_mean, self.set_baseline[set].retn_std])
        for set in self.set_baseline_3:
            baselines.append(['set_3', set, self.set_baseline_3[set].serv_counts, self.set_baseline_3[set].serv_mean,
                              self.set_baseline_3[set].serv_std, self.set_baseline_3[set].retn_counts,
                              self.set_baseline_3[set].retn_mean, self.set_baseline_3[set].retn_std])
        for game in self.game_baseline:
            baselines.append(['game', game, self.game_baseline[game].serv_counts, self.game_baseline[game].serv_mean,
                              self.game_baseline[game].serv_std, self.game_baseline[game].retn_counts,
                              self.game_baseline[game].retn_mean, self.game_baseline[game].retn_std])
        for point in self.point_baseline:
            baselines.append(['point', point, self.point_baseline[point].serv_counts, self.point_baseline[point].serv_mean,
                              self.point_baseline[point].serv_std, self.point_baseline[point].retn_counts,
                              self.point_baseline[point].retn_mean, self.point_baseline[point].retn_std])
        print tabulate.tabulate(baselines, headers=['', '', 'Sdp', 'Smean', 'Sstd', 'Rdp', 'Rmean', 'Rstd'])

        print '--Impact--'
        impacts = []
        impacts.append(['match', '', self.match_impact.serv_counts, self.match_impact.serv_mean,
                        self.match_impact.serv_std, self.match_impact.retn_counts,
                        self.match_impact.retn_mean, self.match_impact.retn_std])
        for set in self.set_impact:
            impacts.append(['set', set, self.set_impact[set].serv_counts, self.set_impact[set].serv_mean,
                            self.set_impact[set].serv_std, self.set_impact[set].retn_counts,
                            self.set_impact[set].retn_mean, self.set_impact[set].retn_std])
        for set in self.set_impact_3:
            impacts.append(['set_3', set, self.set_impact_3[set].serv_counts, self.set_impact_3[set].serv_mean,
                            self.set_impact_3[set].serv_std, self.set_impact_3[set].retn_counts,
                            self.set_impact_3[set].retn_mean, self.set_impact_3[set].retn_std])
        for game in self.game_impact:
            impacts.append(['game', game, self.game_impact[game].serv_counts, self.game_impact[game].serv_mean,
                            self.game_impact[game].serv_std, self.game_impact[game].retn_counts,
                            self.game_impact[game].retn_mean, self.game_impact[game].retn_std])
        for point in self.point_impact:
            impacts.append(['point', point, self.point_impact[point].serv_counts, self.point_impact[point].serv_mean,
                            self.point_impact[point].serv_std, self.point_impact[point].retn_counts,
                            self.point_impact[point].retn_mean, self.point_impact[point].retn_std])
        print tabulate.tabulate(impacts, headers=['', '', 'Sdp', 'Smean', 'Sstd', 'Rdp', 'Rmean', 'Rstd'])

        # print '--Baseline Diff--'
        # baselines_diff = []
        #
        # for set in self.set_baseline_diff:
        #     baselines_diff.append(['set', set, self.set_baseline_diff[set].serv_counts, self.set_baseline_diff[set].serv_mean,
        #                       self.set_baseline_diff[set].serv_std, self.set_baseline_diff[set].retn_counts,
        #                       self.set_baseline_diff[set].retn_mean, self.set_baseline_diff[set].retn_std])
        # for game in self.game_baseline_diff:
        #     baselines_diff.append(['game', game, self.game_baseline_diff[game].serv_counts, self.game_baseline_diff[game].serv_mean,
        #                       self.game_baseline_diff[game].serv_std, self.game_baseline_diff[game].retn_counts,
        #                       self.game_baseline_diff[game].retn_mean, self.game_baseline_diff[game].retn_std])
        # for point in self.point_baseline_diff:
        #     baselines_diff.append(['point', point, self.point_baseline_diff[point].serv_counts, self.point_baseline_diff[point].serv_mean,
        #                       self.point_baseline_diff[point].serv_std, self.point_baseline_diff[point].retn_counts,
        #                       self.point_baseline_diff[point].retn_mean, self.point_baseline_diff[point].retn_std])
        # print tabulate.tabulate(baselines_diff, headers=['', '', 'Sdp', 'Smean', 'Sstd', 'Rdp', 'Rmean', 'Rstd'])
        #
        # print '--Impact Diff--'
        # impacts_diff = []
        #
        # for set in self.set_impact_diff:
        #     impacts_diff.append(['set', set, self.set_impact_diff[set].serv_counts, self.set_impact_diff[set].serv_mean,
        #                     self.set_impact_diff[set].serv_std, self.set_impact_diff[set].retn_counts,
        #                     self.set_impact_diff[set].retn_mean, self.set_impact_diff[set].retn_std])
        # for game in self.game_impact_diff:
        #     impacts_diff.append(['game', game, self.game_impact_diff[game].serv_counts, self.game_impact_diff[game].serv_mean,
        #                     self.game_impact_diff[game].serv_std, self.game_impact_diff[game].retn_counts,
        #                     self.game_impact_diff[game].retn_mean, self.game_impact_diff[game].retn_std])
        # for point in self.point_impact_diff:
        #     impacts_diff.append(['point', point, self.point_impact_diff[point].serv_counts, self.point_impact_diff[point].serv_mean,
        #                     self.point_impact_diff[point].serv_std, self.point_impact_diff[point].retn_counts,
        #                     self.point_impact_diff[point].retn_mean, self.point_impact_diff[point].retn_std])
        # print tabulate.tabulate(impacts_diff, headers=['', '', 'Sdp', 'Smean', 'Sstd', 'Rdp', 'Rmean', 'Rstd'])

    def enrich_matches(self):
        self.match_ids = db_conn.all_match_ids_period(self.name, Player.start_year, Player.end_year, Player.surface, bo=3)

    def calculate_baseline(self):
        match_baseline_dp = match_baseline(self.match_ids)
        self.match_baseline = PlayerStats(match_baseline_dp[0], match_baseline_dp[1])

        [set_baseline_dp, set_baseline_3_dp] = set_baseline(self.match_ids)
        for set in set_baseline_dp:
            self.set_baseline[set] = PlayerStats(set_baseline_dp[set][0], set_baseline_dp[set][1])

        for set in set_baseline_3_dp:
            self.set_baseline_3[set] = PlayerStats(set_baseline_3_dp[set][0], set_baseline_3_dp[set][1])

        game_baseline_dp = game_baseline(self.match_ids)
        for game in game_baseline_dp:
            self.game_baseline[game] = PlayerStats2(game_baseline_dp[game][0], game_baseline_dp[game][1])

        # hacking
        scenarios = [3, 2, 1, 0, -1, -2, -3]
        for s in scenarios:
            if self.game_baseline.get(s, 0) == 0:
                self.game_baseline[s] = PlayerStats2([], [])

        point_baseline_dp = point_baseline(self.match_ids)
        for point in point_baseline_dp:
            self.point_baseline[point] = PlayerStats2(point_baseline_dp[point][0], point_baseline_dp[point][1])

    def calculate_impact(self):
        match_impact_dp = match_impact(self.match_ids)
        self.match_impact = PlayerStats(match_impact_dp[0], match_impact_dp[1])

        [set_impact_dp, set_impact_3_dp] = set_impact(self.match_ids)
        for set in set_impact_dp:
            self.set_impact[set] = PlayerStats(set_impact_dp[set][0], set_impact_dp[set][1])

        for set in set_impact_3_dp:
            self.set_impact_3[set] = PlayerStats(set_impact_3_dp[set][0], set_impact_3_dp[set][1])

        game_impact_dp = game_impact(self.match_ids)
        for game in game_impact_dp:
            self.game_impact[game] = PlayerStats2(game_impact_dp[game][0], game_impact_dp[game][1])

        # hacking
        scenarios = [3, 2, 1, 0, -1, -2, -3]
        for s in scenarios:
            if self.game_impact.get(s, 0) == 0:
                self.game_impact[s] = PlayerStats2([], [])

        point_impact_dp = point_impact(self.match_ids)
        for point in point_impact_dp:
            self.point_impact[point] = PlayerStats2(point_impact_dp[point][0], point_impact_dp[point][1])

    # def calculate_baseline_diff(self):
    #     for set in self.set_baseline:
    #         self.set_baseline_diff[set] = PlayerStats(np.array(self.set_baseline[set].serv_pcts) - self.match_baseline.serv_mean,
    #                                                   np.array(self.set_baseline[set].retn_pcts) - self.match_baseline.retn_mean)
    #
    #     for set in self.set_baseline_3:
    #         self.set_baseline_diff_3[set] = PlayerStats(np.array(self.set_baseline_3[set].serv_pcts) - self.match_baseline.serv_mean,
    #                                                     np.array(self.set_baseline_3[set].retn_pcts) - self.match_baseline.retn_mean)
    #
    #     for game in self.game_baseline:
    #         self.game_baseline_diff[game] = PlayerStats(np.array(self.game_baseline[game].serv_pcts) - self.match_baseline.serv_mean,
    #                                                     np.array(self.game_baseline[game].retn_pcts) - self.match_baseline.retn_mean)
    #
    #     for point in self.point_baseline:
    #         self.point_baseline_diff[point] = PlayerStats(np.array(self.point_baseline[point].serv_pcts) - self.match_baseline.serv_mean,
    #                                                       np.array(self.point_baseline[point].retn_pcts) - self.match_baseline.retn_mean)
    #
    # def calculate_impact_diff(self):
    #     for set in self.set_impact:
    #         self.set_impact_diff[set] = PlayerStats(np.array(self.set_impact[set].serv_pcts) - self.match_impact.serv_mean,
    #                                                   np.array(self.set_impact[set].retn_pcts) - self.match_impact.retn_mean)
    #
    #     for set in self.set_impact_3:
    #         self.set_impact_diff_3[set] = PlayerStats(np.array(self.set_impact_3[set].serv_pcts) - self.match_impact.serv_mean,
    #                                                   np.array(self.set_impact_3[set].retn_pcts) - self.match_impact.retn_mean)
    #
    #     for game in self.game_impact:
    #         self.game_impact_diff[game] = PlayerStats(
    #             np.array(self.game_impact[game].serv_pcts) - self.match_impact.serv_mean,
    #             np.array(self.game_impact[game].retn_pcts) - self.match_impact.retn_mean)
    #
    #     for point in self.point_impact:
    #         self.point_impact_diff[point] = PlayerStats(
    #             np.array(self.point_impact[point].serv_pcts) - self.match_impact.serv_mean,
    #             np.array(self.point_impact[point].retn_pcts) - self.match_impact.retn_mean)

    @staticmethod
    def clean_cached_players():
        Player.cached_players = {}

    @staticmethod
    def get_player(name):
        if Player.cached_players.get(name, 0) == 0:
            Player(name)
        return Player.cached_players[name]


class PlayerStats:
    def __init__(self, serv_pcts, retn_pcts):
        self.serv_pcts = [x for x in serv_pcts if not math.isnan(x)]
        self.retn_pcts = [x for x in retn_pcts if not math.isnan(x)]
        self.serv_counts = len(self.serv_pcts)
        self.retn_counts = len(self.retn_pcts)
        self.serv_mean = np.nanmean(serv_pcts)
        self.serv_std = np.nanstd(serv_pcts)
        self.retn_mean = np.nanmean(retn_pcts)
        self.retn_std = np.nanstd(retn_pcts)


class PlayerStats2:
    def __init__(self, serv_dp, retn_dp):
        self.serv_mean = np.nanmean(serv_dp)
        self.retn_mean = np.nanmean(retn_dp)
        self.serv_counts = len(serv_dp)
        self.retn_counts = len(retn_dp)
        self.serv_std = stats.sem(serv_dp)
        self.retn_std = stats.sem(retn_dp)


def match_baseline(match_ids):
    serv = []
    retn = []
    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        serv.append(matches_1[match].match_pct.p1_serv_pct)
        retn.append(matches_1[match].match_pct.p1_retn_pct)
    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        serv.append(matches_2[match].match_pct.p2_serv_pct)
        retn.append(matches_2[match].match_pct.p2_retn_pct)
    matches_3 = Match.get_matches_pbp(match_ids[3])
    for match in matches_3:
        serv.append(matches_3[match].match_pct.p1_serv_pct)
        retn.append(matches_3[match].match_pct.p1_retn_pct)
    matches_4 = Match.get_matches_pbp(match_ids[4])
    for match in matches_4:
        serv.append(matches_4[match].match_pct.p2_serv_pct)
        retn.append(matches_4[match].match_pct.p2_retn_pct)
    return [serv, retn]


def set_baseline(match_ids):
    set_baseline_dp = {}
    set_baseline_3_dp = {}

    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        for set in matches_1[match].set_pct:
            cur = set_baseline_dp.get(set, [[], []])
            cur[0].append(matches_1[match].set_pct[set].p1_serv_pct)
            cur[1].append(matches_1[match].set_pct[set].p1_retn_pct)
            set_baseline_dp[set] = cur
    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        for set in matches_2[match].set_pct:
            # inversing score as player 2
            cur = set_baseline_dp.get(inv_scr(set), [[], []])
            cur[0].append(matches_2[match].set_pct[set].p2_serv_pct)
            cur[1].append(matches_2[match].set_pct[set].p2_retn_pct)
            set_baseline_dp[inv_scr(set)] = cur
    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        for set in matches_3[match].set_pct:
            cur = set_baseline_3_dp.get(set, [[], []])
            cur[0].append(matches_3[match].set_pct[set].p1_serv_pct)
            cur[1].append(matches_3[match].set_pct[set].p1_retn_pct)
            set_baseline_3_dp[set] = cur
    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        for set in matches_4[match].set_pct:
            # inversing score as player 2
            cur = set_baseline_3_dp.get(inv_scr(set), [[], []])
            cur[0].append(matches_4[match].set_pct[set].p2_serv_pct)
            cur[1].append(matches_4[match].set_pct[set].p2_retn_pct)
            set_baseline_3_dp[inv_scr(set)] = cur
    return [set_baseline_dp, set_baseline_3_dp]


def game_baseline(match_ids):
    game_baseline_dp = {}
    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        for game in matches_1[match].game_pct:
            cur = game_baseline_dp.get(game, [[], []])
            cur[0].extend([1] * matches_1[match].game_pct[game].p1_serv_w + [0] * (matches_1[match].game_pct[game].p1_serv - matches_1[match].game_pct[game].p1_serv_w))
            cur[1].extend([1] * matches_1[match].game_pct[game].p1_retn_w + [0] * (matches_1[match].game_pct[game].p1_retn - matches_1[match].game_pct[game].p1_retn_w))
            game_baseline_dp[game] = cur
    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        for game in matches_2[match].game_pct:
            # inversing score as player 2
            cur = game_baseline_dp.get(inv_scr(game), [[], []])
            cur[0].extend([1] * matches_2[match].game_pct[game].p2_serv_w + [0] * (matches_2[match].game_pct[game].p2_serv - matches_2[match].game_pct[game].p2_serv_w))
            cur[1].extend([1] * matches_2[match].game_pct[game].p2_retn_w + [0] * (matches_2[match].game_pct[game].p2_retn - matches_2[match].game_pct[game].p2_retn_w))
            game_baseline_dp[inv_scr(game)] = cur
    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        for game in matches_3[match].game_pct:
            cur = game_baseline_dp.get(game, [[], []])
            cur[0].extend([1] * matches_3[match].game_pct[game].p1_serv_w + [0] * (matches_3[match].game_pct[game].p1_serv - matches_3[match].game_pct[game].p1_serv_w))
            cur[1].extend([1] * matches_3[match].game_pct[game].p1_retn_w + [0] * (matches_3[match].game_pct[game].p1_retn - matches_3[match].game_pct[game].p1_retn_w))
            game_baseline_dp[game] = cur
    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        for game in matches_4[match].game_pct:
            # inversing score as player 2
            cur = game_baseline_dp.get(inv_scr(game), [[], []])
            cur[0].extend([1] * matches_4[match].game_pct[game].p2_serv_w + [0] * (matches_4[match].game_pct[game].p2_serv - matches_4[match].game_pct[game].p2_serv_w))
            cur[1].extend([1] * matches_4[match].game_pct[game].p2_retn_w + [0] * (matches_4[match].game_pct[game].p2_retn - matches_4[match].game_pct[game].p2_retn_w))
            game_baseline_dp[inv_scr(game)] = cur
    return game_baseline_dp


# def point_baseline(match_ids):
#     point_baseline_dp = {}
#     matches_1 = Match.get_matches(match_ids[1])
#     for match in matches_1:
#         for point in matches_1[match].point_pct:
#             cur = point_baseline_dp.get(point, [[], []])
#             cur[0].append(matches_1[match].point_pct[point].p1_serv_pct)
#             cur[1].append(matches_1[match].point_pct[point].p1_retn_pct)
#             point_baseline_dp[point] = cur
#     matches_2 = Match.get_matches(match_ids[2])
#     for match in matches_2:
#         for point in matches_2[match].point_pct:
#             # inversing score as player 2
#             cur = point_baseline_dp.get(inv_scr(point), [[], []])
#             cur[0].append(matches_2[match].point_pct[point].p2_serv_pct)
#             cur[1].append(matches_2[match].point_pct[point].p2_retn_pct)
#             point_baseline_dp[inv_scr(point)] = cur
#     matches_3 = Match.get_matches(match_ids[3])
#     for match in matches_3:
#         for point in matches_3[match].point_pct:
#             cur = point_baseline_dp.get(point, [[], []])
#             cur[0].append(matches_3[match].point_pct[point].p1_serv_pct)
#             cur[1].append(matches_3[match].point_pct[point].p1_retn_pct)
#             point_baseline_dp[point] = cur
#     matches_4 = Match.get_matches(match_ids[4])
#     for match in matches_4:
#         for point in matches_4[match].point_pct:
#             # inversing score as player 2
#             cur = point_baseline_dp.get(inv_scr(point), [[], []])
#             cur[0].append(matches_4[match].point_pct[point].p2_serv_pct)
#             cur[1].append(matches_4[match].point_pct[point].p2_retn_pct)
#             point_baseline_dp[inv_scr(point)] = cur
#     return point_baseline_dp

#
# def point_baseline(match_ids):
#     point_baseline_dp = {}
#     matches_1 = Match.get_matches(match_ids[1])
#     for match in matches_1:
#         for point in matches_1[match].point_pct:
#             cur = point_baseline_dp.get(point, [0, 0, 0, 0])
#             cur[0] += matches_1[match].point_pct[point].p1_serv_w
#             cur[1] += matches_1[match].point_pct[point].p1_serv
#             cur[2] += matches_1[match].point_pct[point].p1_retn_w
#             cur[3] += matches_1[match].point_pct[point].p1_retn
#             point_baseline_dp[point] = cur
#     matches_2 = Match.get_matches(match_ids[2])
#     for match in matches_2:
#         for point in matches_2[match].point_pct:
#             # inversing score as player 2
#             cur = point_baseline_dp.get(inv_scr(point), [0, 0, 0, 0])
#             cur[0] += matches_2[match].point_pct[point].p2_serv_w
#             cur[1] += matches_2[match].point_pct[point].p2_serv
#             cur[2] += matches_2[match].point_pct[point].p2_retn_w
#             cur[3] += matches_2[match].point_pct[point].p2_retn
#             point_baseline_dp[inv_scr(point)] = cur
#     matches_3 = Match.get_matches(match_ids[3])
#     for match in matches_3:
#         for point in matches_3[match].point_pct:
#             cur = point_baseline_dp.get(point, [0, 0, 0, 0])
#             cur[0] += matches_3[match].point_pct[point].p1_serv_w
#             cur[1] += matches_3[match].point_pct[point].p1_serv
#             cur[2] += matches_3[match].point_pct[point].p1_retn_w
#             cur[3] += matches_3[match].point_pct[point].p1_retn
#             point_baseline_dp[point] = cur
#     matches_4 = Match.get_matches(match_ids[4])
#     for match in matches_4:
#         for point in matches_4[match].point_pct:
#             # inversing score as player 2
#             cur = point_baseline_dp.get(inv_scr(point), [0, 0, 0, 0])
#             cur[0] += matches_4[match].point_pct[point].p2_serv_w
#             cur[1] += matches_4[match].point_pct[point].p2_serv
#             cur[2] += matches_4[match].point_pct[point].p2_retn_w
#             cur[3] += matches_4[match].point_pct[point].p2_retn
#             point_baseline_dp[inv_scr(point)] = cur
#     return point_baseline_dp

def point_baseline(match_ids):
    point_baseline_dp = {}
    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        for point in matches_1[match].point_pct:
            cur = point_baseline_dp.get(point, [[], []])
            cur[0].extend([1] * matches_1[match].point_pct[point].p1_serv_w + [0] * (matches_1[match].point_pct[point].p1_serv - matches_1[match].point_pct[point].p1_serv_w))
            cur[1].extend([1] * matches_1[match].point_pct[point].p1_retn_w + [0] * (matches_1[match].point_pct[point].p1_retn - matches_1[match].point_pct[point].p1_retn_w))
            point_baseline_dp[point] = cur
    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        for point in matches_2[match].point_pct:
            # inversing score as player 2
            cur = point_baseline_dp.get(inv_scr(point), [[], []])
            cur[0].extend([1] * matches_2[match].point_pct[point].p2_serv_w + [0] * (matches_2[match].point_pct[point].p2_serv - matches_2[match].point_pct[point].p2_serv_w))
            cur[1].extend([1] * matches_2[match].point_pct[point].p2_retn_w + [0] * (matches_2[match].point_pct[point].p2_retn - matches_2[match].point_pct[point].p2_retn_w))
            point_baseline_dp[inv_scr(point)] = cur
    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        for point in matches_3[match].point_pct:
            cur = point_baseline_dp.get(point, [[], []])
            cur[0].extend([1] * matches_3[match].point_pct[point].p1_serv_w + [0] * (matches_3[match].point_pct[point].p1_serv - matches_3[match].point_pct[point].p1_serv_w))
            cur[1].extend([1] * matches_3[match].point_pct[point].p1_retn_w + [0] * (matches_3[match].point_pct[point].p1_retn - matches_3[match].point_pct[point].p1_retn_w))
            point_baseline_dp[point] = cur
    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        for point in matches_4[match].point_pct:
            # inversing score as player 2
            cur = point_baseline_dp.get(inv_scr(point), [[], []])
            cur[0].extend([1] * matches_4[match].point_pct[point].p2_serv_w + [0] * (matches_4[match].point_pct[point].p2_serv - matches_4[match].point_pct[point].p2_serv_w))
            cur[1].extend([1] * matches_4[match].point_pct[point].p2_retn_w + [0] * (matches_4[match].point_pct[point].p2_retn - matches_4[match].point_pct[point].p2_retn_w))
            point_baseline_dp[inv_scr(point)] = cur
    return point_baseline_dp


def match_impact(match_ids):
    serv = []
    retn = []

    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        oppo = Player.get_player(matches_1[match].player2)
        serv.append(1.0 - matches_1[match].match_pct.p1_retn_pct - oppo.match_baseline.serv_mean)
        retn.append(1.0 - matches_1[match].match_pct.p1_serv_pct - oppo.match_baseline.retn_mean)

    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        oppo = Player.get_player(matches_2[match].player1)
        serv.append(1.0 - matches_2[match].match_pct.p2_retn_pct - oppo.match_baseline.serv_mean)
        retn.append(1.0 - matches_2[match].match_pct.p2_serv_pct - oppo.match_baseline.retn_mean)

    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        oppo = Player.get_player(matches_3[match].player2)
        serv.append(1.0 - matches_3[match].match_pct.p1_retn_pct - oppo.match_baseline.serv_mean)
        retn.append(1.0 - matches_3[match].match_pct.p1_serv_pct - oppo.match_baseline.retn_mean)

    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        oppo = Player.get_player(matches_4[match].player1)
        serv.append(1.0 - matches_4[match].match_pct.p2_retn_pct - oppo.match_baseline.serv_mean)
        retn.append(1.0 - matches_4[match].match_pct.p2_serv_pct - oppo.match_baseline.retn_mean)
    return [serv, retn]


def set_impact(match_ids):
    impact = {}
    impact_3 = {}

    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        oppo = Player.get_player(matches_1[match].player2)
        for set in matches_1[match].set_pct:
            serv = 1.0 - matches_1[match].set_pct[set].p1_retn_pct - oppo.set_baseline[inv_scr(set)].serv_mean
            retn = 1.0 - matches_1[match].set_pct[set].p1_serv_pct - oppo.set_baseline[inv_scr(set)].retn_mean
            cur = impact.get(set, [[], []])
            cur[0].append(serv)
            cur[1].append(retn)
            impact[set] = cur

    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        oppo = Player.get_player(matches_2[match].player1)
        for set in matches_2[match].set_pct:
            serv = 1.0 - matches_2[match].set_pct[set].p2_retn_pct - oppo.set_baseline[set].serv_mean
            retn = 1.0 - matches_2[match].set_pct[set].p2_serv_pct - oppo.set_baseline[set].retn_mean
            cur = impact.get(inv_scr(set), [[], []])
            cur[0].append(serv)
            cur[1].append(retn)
            impact[inv_scr(set)] = cur

    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        oppo = Player.get_player(matches_3[match].player2)
        for set in matches_3[match].set_pct:
            serv = 1.0 - matches_3[match].set_pct[set].p1_retn_pct - oppo.set_baseline_3[inv_scr(set)].serv_mean
            retn = 1.0 - matches_3[match].set_pct[set].p1_serv_pct - oppo.set_baseline_3[inv_scr(set)].retn_mean
            cur = impact_3.get(set, [[], []])
            cur[0].append(serv)
            cur[1].append(retn)
            impact_3[set] = cur

    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        oppo = Player.get_player(matches_4[match].player1)
        for set in matches_4[match].set_pct:
            serv = 1.0 - matches_4[match].set_pct[set].p2_retn_pct - oppo.set_baseline_3[set].serv_mean
            retn = 1.0 - matches_4[match].set_pct[set].p2_serv_pct - oppo.set_baseline_3[set].retn_mean
            cur = impact_3.get(inv_scr(set), [[], []])
            cur[0].append(serv)
            cur[1].append(retn)
            impact_3[inv_scr(set)] = cur
    return [impact, impact_3]


def game_impact(match_ids):
    impact = {}

    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        oppo = Player.get_player(matches_1[match].player2)
        for game in matches_1[match].game_pct:
            serv = [0.0 - oppo.game_baseline[inv_scr(game)].serv_mean] * matches_1[match].game_pct[game].p1_retn_w + \
                   [1.0 - oppo.game_baseline[inv_scr(game)].serv_mean] * (matches_1[match].game_pct[game].p1_retn - matches_1[match].game_pct[game].p1_retn_w)
            retn = [0.0 - oppo.game_baseline[inv_scr(game)].retn_mean] * matches_1[match].game_pct[game].p1_serv_w + \
                   [1.0 - oppo.game_baseline[inv_scr(game)].retn_mean] * (matches_1[match].game_pct[game].p1_serv - matches_1[match].game_pct[game].p1_serv_w)
            cur = impact.get(game, [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[game] = cur

    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        oppo = Player.get_player(matches_2[match].player1)
        for game in matches_2[match].game_pct:
            serv = [0.0 - oppo.game_baseline[game].serv_mean] * matches_2[match].game_pct[game].p2_retn_w + \
                   [1.0 - oppo.game_baseline[game].serv_mean] * (matches_2[match].game_pct[game].p2_retn - matches_2[match].game_pct[game].p2_retn_w)
            retn = [0.0 - oppo.game_baseline[game].retn_mean] * matches_2[match].game_pct[game].p2_serv_w + \
                   [1.0 - oppo.game_baseline[game].retn_mean] * (matches_2[match].game_pct[game].p2_serv - matches_2[match].game_pct[game].p2_serv_w)
            cur = impact.get(inv_scr(game), [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[inv_scr(game)] = cur

    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        oppo = Player.get_player(matches_3[match].player2)
        for game in matches_3[match].game_pct:
            serv = [0.0 - oppo.game_baseline[inv_scr(game)].serv_mean] * matches_3[match].game_pct[game].p1_retn_w + \
                   [1.0 - oppo.game_baseline[inv_scr(game)].serv_mean] * (matches_3[match].game_pct[game].p1_retn - matches_3[match].game_pct[game].p1_retn_w)
            retn = [0.0 - oppo.game_baseline[inv_scr(game)].retn_mean] * matches_3[match].game_pct[game].p1_serv_w + \
                   [1.0 - oppo.game_baseline[inv_scr(game)].retn_mean] * (matches_3[match].game_pct[game].p1_serv - matches_3[match].game_pct[game].p1_serv_w)
            cur = impact.get(game, [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[game] = cur

    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        oppo = Player.get_player(matches_4[match].player1)
        for game in matches_4[match].game_pct:
            serv = [0.0 - oppo.game_baseline[game].serv_mean] * matches_4[match].game_pct[game].p2_retn_w + \
                   [1.0 - oppo.game_baseline[game].serv_mean] * (matches_4[match].game_pct[game].p2_retn - matches_4[match].game_pct[game].p2_retn_w)
            retn = [0.0 - oppo.game_baseline[game].retn_mean] * matches_4[match].game_pct[game].p2_serv_w + \
                   [1.0 - oppo.game_baseline[game].retn_mean] * (matches_4[match].game_pct[game].p2_serv - matches_4[match].game_pct[game].p2_serv_w)
            cur = impact.get(inv_scr(game), [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[inv_scr(game)] = cur
    return impact


def point_impact(match_ids):
    impact = {}

    matches_1 = Match.get_matches(match_ids[1])
    for match in matches_1:
        oppo = Player.get_player(matches_1[match].player2)
        for point in matches_1[match].point_pct:
            serv = [0.0 - oppo.point_baseline[inv_scr(point)].serv_mean] * matches_1[match].point_pct[point].p1_retn_w + \
                   [1.0 - oppo.point_baseline[inv_scr(point)].serv_mean] * (matches_1[match].point_pct[point].p1_retn - matches_1[match].point_pct[point].p1_retn_w)
            retn = [0.0 - oppo.point_baseline[inv_scr(point)].retn_mean] * matches_1[match].point_pct[point].p1_serv_w + \
                   [1.0 - oppo.point_baseline[inv_scr(point)].retn_mean] * (matches_1[match].point_pct[point].p1_serv - matches_1[match].point_pct[point].p1_serv_w)
            cur = impact.get(point, [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[point] = cur

    matches_2 = Match.get_matches(match_ids[2])
    for match in matches_2:
        oppo = Player.get_player(matches_2[match].player1)
        for point in matches_2[match].point_pct:
            serv = [0.0 - oppo.point_baseline[point].serv_mean] * matches_2[match].point_pct[point].p2_retn_w + \
                   [1.0 - oppo.point_baseline[point].serv_mean] * (matches_2[match].point_pct[point].p2_retn - matches_2[match].point_pct[point].p2_retn_w)
            retn = [0.0 - oppo.point_baseline[point].retn_mean] * matches_2[match].point_pct[point].p2_serv_w + \
                   [1.0 - oppo.point_baseline[point].retn_mean] * (matches_2[match].point_pct[point].p2_serv - matches_2[match].point_pct[point].p2_serv_w)
            cur = impact.get(inv_scr(point), [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[inv_scr(point)] = cur

    matches_3 = Match.get_matches(match_ids[3])
    for match in matches_3:
        oppo = Player.get_player(matches_3[match].player2)
        for point in matches_3[match].point_pct:
            serv = [0.0 - oppo.point_baseline[inv_scr(point)].serv_mean] * matches_3[match].point_pct[point].p1_retn_w + \
                   [1.0 - oppo.point_baseline[inv_scr(point)].serv_mean] * (matches_3[match].point_pct[point].p1_retn - matches_3[match].point_pct[point].p1_retn_w)
            retn = [0.0 - oppo.point_baseline[inv_scr(point)].retn_mean] * matches_3[match].point_pct[point].p1_serv_w + \
                   [1.0 - oppo.point_baseline[inv_scr(point)].retn_mean] * (matches_3[match].point_pct[point].p1_serv - matches_3[match].point_pct[point].p1_serv_w)
            cur = impact.get(point, [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[point] = cur

    matches_4 = Match.get_matches(match_ids[4])
    for match in matches_4:
        oppo = Player.get_player(matches_4[match].player1)
        for point in matches_4[match].point_pct:
            serv = [0.0 - oppo.point_baseline[point].serv_mean] * matches_4[match].point_pct[point].p2_retn_w + \
                   [1.0 - oppo.point_baseline[point].serv_mean] * (matches_4[match].point_pct[point].p2_retn - matches_4[match].point_pct[point].p2_retn_w)
            retn = [0.0 - oppo.point_baseline[point].retn_mean] * matches_4[match].point_pct[point].p2_serv_w + \
                   [1.0 - oppo.point_baseline[point].retn_mean] * (matches_4[match].point_pct[point].p2_serv - matches_4[match].point_pct[point].p2_serv_w)
            cur = impact.get(inv_scr(point), [[], []])
            cur[0].extend(serv)
            cur[1].extend(retn)
            impact[inv_scr(point)] = cur

    return impact


def inv_scr(score):
    if type(score) is str:
        scores = score.split(':')
        return scores[1] + ":" + scores[0]
    if type(score) is int:
        return 0 - score


def baseline_std_mean(win, total):
    if total <= 1:
        return float('nan')
    mean = float(win) / total
    std = math.sqrt((win * (1.0 - mean) ** 2 + (total - win) * mean ** 2) / (total - 1))
    return std / math.sqrt(total)
