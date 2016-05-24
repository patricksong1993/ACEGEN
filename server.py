import flask
from classes.player import Player
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import numpy as np
import scipy.stats as stats
import sys

sys.setrecursionlimit(100000)

start_year = Player.start_year
end_year = Player.end_year
surface = Player.surface

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "IMPACT!"

@app.route('/multi_player', methods=['GET'])
@crossdomain(origin='*')
def get_multi_player():
    start_year = int(request.args.get('start_year'))
    end_year = int(request.args.get('end_year'))
    surface = request.args.get('surface')
    two_step = request.args.get('two_step')
    if (start_year != Player.start_year) or (end_year != Player.end_year) or (surface != Player.surface):
        Player.cached_players = {}
        Player.start_year = start_year
        Player.end_year = end_year
        Player.surface = surface
    player_names = request.args.get('player_name')
    player_names = player_names.split(',')
    metrics_level = request.args.get('metrics_level')
    baseline_impact = request.args.get('baseline_impact')
    serve_return = request.args.get('serve_return')
    players = {}
    for player_name in player_names:
        players[player_name] = Player(player_name)

    if two_step == 'true':
        Player.calculate_all_ts()

    all_players_stats = {}

    # grand 5 sets missing

    if metrics_level == 'set':
        for player in players:

            if two_step == 'true':
                if baseline_impact == 'baseline':
                    player_stat = players[player].set_baseline_3_ts
                    player_match_stat = players[player].match_baseline_ts
                elif baseline_impact == 'impact':
                    player_stat = players[player].set_impact_3_ts
                    player_match_stat = players[player].match_impact_ts
            else:
                if baseline_impact == 'baseline':
                    player_stat = players[player].set_baseline_3
                    player_match_stat = players[player].match_baseline
                elif baseline_impact == 'impact':
                    player_stat = players[player].set_impact_3
                    player_match_stat = players[player].match_impact


            if serve_return == 'serve':
                player_stats = [player_match_stat.serv_mean,
                                player_stat['0:0'].serv_mean, player_stat['1:0'].serv_mean, player_stat['0:1'].serv_mean,
                                player_stat['1:1'].serv_mean]
                player_stats_ci = [player_match_stat.serv_std * stats.t._ppf(0.9,player_match_stat.serv_counts),
                                   player_stat['0:0'].serv_std * stats.t._ppf(0.9,player_stat['0:0'].serv_counts),
                                   player_stat['1:0'].serv_std * stats.t._ppf(0.9,player_stat['1:0'].serv_counts),
                                   player_stat['0:1'].serv_std * stats.t._ppf(0.9,player_stat['0:1'].serv_counts),
                                   player_stat['1:1'].serv_std * stats.t._ppf(0.9,player_stat['1:1'].serv_counts)]
            elif serve_return == 'return':
                player_stats = [player_match_stat.retn_mean,
                                player_stat['0:0'].retn_mean, player_stat['1:0'].retn_mean, player_stat['0:1'].retn_mean,
                                player_stat['1:1'].retn_mean]
                player_stats_ci = [player_match_stat.retn_std * stats.t._ppf(0.9, player_match_stat.retn_counts),
                                   player_stat['0:0'].retn_std * stats.t._ppf(0.9, player_stat['0:0'].retn_counts),
                                   player_stat['1:0'].retn_std * stats.t._ppf(0.9, player_stat['1:0'].retn_counts),
                                   player_stat['0:1'].retn_std * stats.t._ppf(0.9, player_stat['0:1'].retn_counts),
                                   player_stat['1:1'].retn_std * stats.t._ppf(0.9, player_stat['1:1'].retn_counts)]
            for x in range(player_stats.__len__()):
                if np.isnan(player_stats[x]):
                    player_stats[x] = float(0.0)
            for x in range(player_stats_ci.__len__()):
                if np.isnan(player_stats_ci[x]):
                    player_stats_ci[x] = float(0.0)
            all_players_stats[player] = {'mean':player_stats,'ci':player_stats_ci}

        header = ['match', '0:0', '1:0', '0:1', '1:1']

    elif metrics_level == 'game':
        for player in players:

            if two_step == 'true':
                if baseline_impact == 'baseline':
                    player_stat = players[player].game_baseline_ts
                    player_match_stat = players[player].match_baseline_ts
                elif baseline_impact == 'impact':
                    player_stat = players[player].game_impact_ts
                    player_match_stat = players[player].match_impact_ts
            else:
                if baseline_impact == 'baseline':
                    player_stat = players[player].game_baseline
                    player_match_stat = players[player].match_baseline
                elif baseline_impact == 'impact':
                    player_stat = players[player].game_impact
                    player_match_stat = players[player].match_impact

            if serve_return == 'serve':
                player_stats = [player_match_stat.serv_mean,
                                player_stat[3].serv_mean, player_stat[2].serv_mean, player_stat[1].serv_mean,
                                player_stat[0].serv_mean, player_stat[-1].serv_mean, player_stat[-2].serv_mean,
                                player_stat[-3].serv_mean]
                player_stats_ci = [player_match_stat.serv_std * stats.t._ppf(0.9, player_match_stat.serv_counts),
                                   player_stat[3].serv_std * stats.t._ppf(0.9, player_stat[3].serv_counts),
                                   player_stat[2].serv_std * stats.t._ppf(0.9, player_stat[2].serv_counts),
                                   player_stat[1].serv_std * stats.t._ppf(0.9, player_stat[1].serv_counts),
                                   player_stat[0].serv_std * stats.t._ppf(0.9, player_stat[0].serv_counts),
                                   player_stat[-1].serv_std * stats.t._ppf(0.9, player_stat[-1].serv_counts),
                                   player_stat[-2].serv_std * stats.t._ppf(0.9, player_stat[-2].serv_counts),
                                   player_stat[-3].serv_std * stats.t._ppf(0.9, player_stat[-3].serv_counts)]
            elif serve_return == 'return':
                player_stats = [player_match_stat.retn_mean,
                                player_stat[3].retn_mean, player_stat[2].retn_mean, player_stat[1].retn_mean,
                                player_stat[0].retn_mean, player_stat[-1].retn_mean, player_stat[-2].retn_mean,
                                player_stat[-3].retn_mean]
                player_stats_ci = [player_match_stat.retn_std * stats.t._ppf(0.9, player_match_stat.retn_counts),
                                   player_stat[3].retn_std * stats.t._ppf(0.9, player_stat[3].retn_counts),
                                   player_stat[2].retn_std * stats.t._ppf(0.9, player_stat[2].retn_counts),
                                   player_stat[1].retn_std * stats.t._ppf(0.9, player_stat[1].retn_counts),
                                   player_stat[0].retn_std * stats.t._ppf(0.9, player_stat[0].retn_counts),
                                   player_stat[-1].retn_std * stats.t._ppf(0.9, player_stat[-1].retn_counts),
                                   player_stat[-2].retn_std * stats.t._ppf(0.9, player_stat[-2].retn_counts),
                                   player_stat[-3].retn_std * stats.t._ppf(0.9, player_stat[-3].retn_counts)]
            for x in range(player_stats.__len__()):
                if np.isnan(player_stats[x]):
                    player_stats[x] = float(0.0)
            for x in range(player_stats_ci.__len__()):
                if np.isnan(player_stats_ci[x]):
                    player_stats_ci[x] = float(0.0)
            all_players_stats[player] = {'mean': player_stats, 'ci': player_stats_ci}

        header = ['match', '3', '2', '1', '0', '-1', '-2', '-3']

    elif metrics_level == 'point':
        for player in players:

            if two_step == 'true':
                if baseline_impact == 'baseline':
                    player_stat = players[player].point_baseline_ts
                    player_match_stat = players[player].match_baseline_ts
                elif baseline_impact == 'impact':
                    player_stat = players[player].point_impact_ts
                    player_match_stat = players[player].match_impact_ts
            else:
                if baseline_impact == 'baseline':
                    player_stat = players[player].point_baseline
                    player_match_stat = players[player].match_baseline
                elif baseline_impact == 'impact':
                    player_stat = players[player].point_impact
                    player_match_stat = players[player].match_impact

            if serve_return == 'serve':
                player_stats = [player_match_stat.serv_mean,
                                player_stat['0:0'].serv_mean, player_stat['15:15'].serv_mean, player_stat['30:30'].serv_mean,
                                player_stat['40:40'].serv_mean, player_stat['15:0'].serv_mean, player_stat['30:15'].serv_mean,
                                player_stat['40:30'].serv_mean, player_stat['AD:40'].serv_mean, player_stat['30:0'].serv_mean,
                                player_stat['40:15'].serv_mean, player_stat['40:0'].serv_mean, player_stat['0:15'].serv_mean,
                                player_stat['15:30'].serv_mean, player_stat['30:40'].serv_mean, player_stat['40:AD'].serv_mean,
                                player_stat['0:30'].serv_mean, player_stat['15:40'].serv_mean, player_stat['0:40'].serv_mean]
                player_stats_ci = [player_match_stat.serv_std * stats.t._ppf(0.9, player_match_stat.serv_counts),
                                   player_stat['0:0'].serv_std * stats.t._ppf(0.9, player_stat['0:0'].serv_counts),
                                   player_stat['15:15'].serv_std * stats.t._ppf(0.9, player_stat['15:15'].serv_counts),
                                   player_stat['30:30'].serv_std * stats.t._ppf(0.9, player_stat['30:30'].serv_counts),
                                   player_stat['40:40'].serv_std * stats.t._ppf(0.9, player_stat['40:40'].serv_counts),
                                   player_stat['15:0'].serv_std * stats.t._ppf(0.9, player_stat['15:0'].serv_counts),
                                   player_stat['30:15'].serv_std * stats.t._ppf(0.9, player_stat['30:15'].serv_counts),
                                   player_stat['40:30'].serv_std * stats.t._ppf(0.9, player_stat['40:30'].serv_counts),
                                   player_stat['AD:40'].serv_std * stats.t._ppf(0.9, player_stat['AD:40'].serv_counts),
                                   player_stat['30:0'].serv_std * stats.t._ppf(0.9, player_stat['30:0'].serv_counts),
                                   player_stat['40:15'].serv_std * stats.t._ppf(0.9, player_stat['40:15'].serv_counts),
                                   player_stat['40:0'].serv_std * stats.t._ppf(0.9, player_stat['40:0'].serv_counts),
                                   player_stat['0:15'].serv_std * stats.t._ppf(0.9, player_stat['0:15'].serv_counts),
                                   player_stat['15:30'].serv_std * stats.t._ppf(0.9, player_stat['15:30'].serv_counts),
                                   player_stat['30:40'].serv_std * stats.t._ppf(0.9, player_stat['30:40'].serv_counts),
                                   player_stat['40:AD'].serv_std * stats.t._ppf(0.9, player_stat['40:AD'].serv_counts),
                                   player_stat['0:30'].serv_std * stats.t._ppf(0.9, player_stat['0:30'].serv_counts),
                                   player_stat['15:40'].serv_std * stats.t._ppf(0.9, player_stat['15:40'].serv_counts),
                                   player_stat['0:40'].serv_std * stats.t._ppf(0.9, player_stat['0:40'].serv_counts)]
            elif serve_return == 'return':
                player_stats = [player_match_stat.retn_mean,
                                player_stat['0:0'].retn_mean, player_stat['15:15'].retn_mean, player_stat['30:30'].retn_mean,
                                player_stat['40:40'].retn_mean, player_stat['15:0'].retn_mean, player_stat['30:15'].retn_mean,
                                player_stat['40:30'].retn_mean, player_stat['AD:40'].retn_mean, player_stat['30:0'].retn_mean,
                                player_stat['40:15'].retn_mean, player_stat['40:0'].retn_mean, player_stat['0:15'].retn_mean,
                                player_stat['15:30'].retn_mean, player_stat['30:40'].retn_mean, player_stat['40:AD'].retn_mean,
                                player_stat['0:30'].retn_mean, player_stat['15:40'].retn_mean, player_stat['0:40'].retn_mean]
                player_stats_ci = [player_match_stat.retn_std * stats.t._ppf(0.9, player_match_stat.retn_counts),
                                   player_stat['0:0'].retn_std * stats.t._ppf(0.9, player_stat['0:0'].retn_counts),
                                   player_stat['15:15'].retn_std * stats.t._ppf(0.9, player_stat['15:15'].retn_counts),
                                   player_stat['30:30'].retn_std * stats.t._ppf(0.9, player_stat['30:30'].retn_counts),
                                   player_stat['40:40'].retn_std * stats.t._ppf(0.9, player_stat['40:40'].retn_counts),
                                   player_stat['15:0'].retn_std * stats.t._ppf(0.9, player_stat['15:0'].retn_counts),
                                   player_stat['30:15'].retn_std * stats.t._ppf(0.9, player_stat['30:15'].retn_counts),
                                   player_stat['40:30'].retn_std * stats.t._ppf(0.9, player_stat['40:30'].retn_counts),
                                   player_stat['AD:40'].retn_std * stats.t._ppf(0.9, player_stat['AD:40'].retn_counts),
                                   player_stat['30:0'].retn_std * stats.t._ppf(0.9, player_stat['30:0'].retn_counts),
                                   player_stat['40:15'].retn_std * stats.t._ppf(0.9, player_stat['40:15'].retn_counts),
                                   player_stat['40:0'].retn_std * stats.t._ppf(0.9, player_stat['40:0'].retn_counts),
                                   player_stat['0:15'].retn_std * stats.t._ppf(0.9, player_stat['0:15'].retn_counts),
                                   player_stat['15:30'].retn_std * stats.t._ppf(0.9, player_stat['15:30'].retn_counts),
                                   player_stat['30:40'].retn_std * stats.t._ppf(0.9, player_stat['30:40'].retn_counts),
                                   player_stat['40:AD'].retn_std * stats.t._ppf(0.9, player_stat['40:AD'].retn_counts),
                                   player_stat['0:30'].retn_std * stats.t._ppf(0.9, player_stat['0:30'].retn_counts),
                                   player_stat['15:40'].retn_std * stats.t._ppf(0.9, player_stat['15:40'].retn_counts),
                                   player_stat['0:40'].retn_std * stats.t._ppf(0.9, player_stat['0:40'].retn_counts)]
            for x in range(player_stats.__len__()):
                if np.isnan(player_stats[x]):
                    player_stats[x] = float(0.0)
            for x in range(player_stats_ci.__len__()):
                if np.isnan(player_stats_ci[x]):
                    player_stats_ci[x] = float(0.0)
            all_players_stats[player] = {'mean': player_stats, 'ci': player_stats_ci}

        header = ['match', '0:0', '15:15', '30:30', '40:40', '15:0', '30:15', '40:30', 'AD:40', '30:0',
                  '40:15', '40:0', '0:15', '15:30', '30:40', '40:AD', '0:30', '15:40', '0:40']


    return flask.jsonify({'player_stats': all_players_stats, 'header': header})

# @app.route('/player_stats', methods=['GET'])
# @crossdomain(origin='*')
# def get_player_stats():
#     Player.start_year = 2013
#     Player.end_year = 2016
#     Player.surface = 'clay'
#     player_name = request.args.get('player_name')
#     stat_aspect = request.args.get('stat_aspect')
#     stat_level = request.args.get('stat_level')
#
#     player = Player(player_name)
#
#     if stat_level == 'set':
#         if stat_aspect == 'baseline':
#             stat = player.set_baseline
#             match_stat = player.match_baseline
#         elif stat_aspect == 'impact':
#             stat = player.set_impact
#             match_stat = player.match_impact
#         elif stat_aspect == 'baseline diff':
#             stat = player.set_baseline_diff
#             match_stat = player.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             stat = player.set_impact_diff
#             match_stat = player.match_impact_diff
#
#         serv = [match_stat.serv_mean,
#                 stat['0:0'].serv_mean,stat['1:0'].serv_mean,stat['0:1'].serv_mean,
#                 stat['1:1'].serv_mean,stat['2:0'].serv_mean,stat['0:2'].serv_mean,
#                 stat['1:2'].serv_mean,stat['2:1'].serv_mean,stat['2:2'].serv_mean]
#
#         retn = [match_stat.retn_mean,
#                 stat['0:0'].retn_mean, stat['1:0'].retn_mean,stat['0:1'].retn_mean,
#                 stat['1:1'].retn_mean, stat['2:0'].retn_mean,stat['0:2'].retn_mean,
#                 stat['1:2'].retn_mean, stat['2:1'].retn_mean,stat['2:2'].retn_mean]
#
#         header = ['match','0:0','1:0','0:1','1:1','2:0','0:2','1:2','2:1','2:2']
#
#     if stat_level == 'set_3':
#         if stat_aspect == 'baseline':
#             stat = player.set_baseline_3
#             match_stat = player.match_baseline
#         elif stat_aspect == 'impact':
#             stat = player.set_impact_3
#             match_stat = player.match_impact
#         elif stat_aspect == 'baseline diff':
#             stat = player.set_baseline_diff_3
#             match_stat = player.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             stat = player.set_impact_diff_3
#             match_stat = player.match_impact_diff
#
#         serv = [match_stat.serv_mean,
#                 stat['0:0'].serv_mean, stat['1:0'].serv_mean, stat['0:1'].serv_mean,
#                 stat['1:1'].serv_mean]
#
#         retn = [match_stat.retn_mean,
#                 stat['0:0'].retn_mean, stat['1:0'].retn_mean, stat['0:1'].retn_mean,
#                 stat['1:1'].retn_mean]
#
#         header = ['match', '0:0', '1:0', '0:1', '1:1']
#
#     if stat_level == 'game':
#         if stat_aspect == 'baseline':
#             stat = player.game_baseline
#             match_stat = player.match_baseline
#         elif stat_aspect == 'impact':
#             stat = player.game_impact
#             match_stat = player.match_impact
#         elif stat_aspect == 'baseline diff':
#             stat = player.game_baseline_diff
#             match_stat = player.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             stat = player.game_impact_diff
#             match_stat = player.match_impact_diff
#
#         serv = [match_stat.serv_mean,
#                 stat[3].serv_mean, stat[2].serv_mean, stat[1].serv_mean,
#                 stat[0].serv_mean, stat[-1].serv_mean, stat[-2].serv_mean,
#                 stat[-3].serv_mean]
#
#         retn = [match_stat.retn_mean,
#                 stat[3].retn_mean, stat[2].retn_mean, stat[1].retn_mean,
#                 stat[0].retn_mean, stat[-1].retn_mean, stat[-2].retn_mean,
#                 stat[-3].retn_mean]
#
#         header = ['match', '3','2','1','0','-1','-2','-3']
#
#     if stat_level == 'point':
#         if stat_aspect == 'baseline':
#             stat = player.point_baseline
#             match_stat = player.match_baseline
#         elif stat_aspect == 'impact':
#             stat = player.point_impact
#             match_stat = player.match_impact
#         elif stat_aspect == 'baseline diff':
#             stat = player.point_baseline_diff
#             match_stat = player.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             stat = player.point_impact_diff
#             match_stat = player.match_impact_diff
#
#         serv = [match_stat.serv_mean,
#                 stat['0:0'].serv_mean, stat['15:15'].serv_mean, stat['30:30'].serv_mean,
#                 stat['40:40'].serv_mean, stat['15:0'].serv_mean, stat['30:15'].serv_mean,
#                 stat['40:30'].serv_mean, stat['AD:40'].serv_mean, stat['30:0'].serv_mean,
#                 stat['40:15'].serv_mean, stat['40:0'].serv_mean, stat['0:15'].serv_mean,
#                 stat['15:30'].serv_mean, stat['30:40'].serv_mean, stat['40:AD'].serv_mean,
#                 stat['0:30'].serv_mean, stat['15:40'].serv_mean, stat['0:40'].serv_mean]
#
#         retn = [match_stat.retn_mean,
#                 stat['0:0'].retn_mean, stat['15:15'].retn_mean, stat['30:30'].retn_mean,
#                 stat['40:40'].retn_mean, stat['15:0'].retn_mean, stat['30:15'].retn_mean,
#                 stat['40:30'].retn_mean, stat['AD:40'].retn_mean, stat['30:0'].retn_mean,
#                 stat['40:15'].retn_mean, stat['40:0'].retn_mean, stat['0:15'].retn_mean,
#                 stat['15:30'].retn_mean, stat['30:40'].retn_mean, stat['40:AD'].retn_mean,
#                 stat['0:30'].retn_mean, stat['15:40'].retn_mean, stat['0:40'].retn_mean]
#
#         header = ['match', '0:0', '15:15', '30:30', '40:40', '15:0', '30:15', '40:30', 'AD:40', '30:0',
#                   '40:15', '40:0', '0:15', '15:30', '30:40', '40:AD', '0:30', '15:40', '0:40']
#
#     serv = np.array(serv)
#     serv[np.isnan(serv)] = 0
#     retn = np.array(retn)
#     retn[np.isnan(retn)] = 0
#
#     return flask.jsonify({'serv': serv.tolist(), 'retn': retn.tolist(), 'header': header})
#
#
# @app.route('/player_compare', methods=['GET'])
# @crossdomain(origin='*')
# def get_player_compare():
#     Player.start_year = 2013
#     Player.end_year = 2016
#     Player.surface = 'clay'
#     p1_name = request.args.get('p1_name')
#     p2_name = request.args.get('p2_name')
#     stat_aspect = request.args.get('stat_aspect')
#     stat_level = request.args.get('stat_level')
#     serve_return = request.args.get('serve_return')
#     p1 = Player(p1_name)
#     p2 = Player(p2_name)
#
#     if stat_level == 'set':
#         if stat_aspect == 'baseline':
#             p1_stat = p1.set_baseline
#             p1_match_stat = p1.match_baseline
#             p2_stat = p2.set_baseline
#             p2_match_stat = p2.match_baseline
#         elif stat_aspect == 'impact':
#             p1_stat = p1.set_impact
#             p1_match_stat = p1.match_impact
#             p2_stat = p2.set_impact
#             p2_match_stat = p2.match_impact
#         elif stat_aspect == 'baseline diff':
#             p1_stat = p1.set_baseline_diff
#             p1_match_stat = p1.match_baseline_diff
#             p2_stat = p2.set_baseline_diff
#             p2_match_stat = p2.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             p1_stat = p1.set_impact_diff
#             p1_match_stat = p1.match_impact_diff
#             p2_stat = p2.set_impact_diff
#             p2_match_stat = p2.match_impact_diff
#
#         if serve_return == 'serve':
#             p1_stats = [p1_match_stat.serv_mean,
#                         p1_stat['0:0'].serv_mean, p1_stat['1:0'].serv_mean, p1_stat['0:1'].serv_mean,
#                         p1_stat['1:1'].serv_mean, p1_stat['2:0'].serv_mean, p1_stat['0:2'].serv_mean,
#                         p1_stat['1:2'].serv_mean, p1_stat['2:1'].serv_mean, p1_stat['2:2'].serv_mean]
#             p2_stats = [p2_match_stat.serv_mean,
#                         p2_stat['0:0'].serv_mean, p2_stat['1:0'].serv_mean, p2_stat['0:1'].serv_mean,
#                         p2_stat['1:1'].serv_mean, p2_stat['2:0'].serv_mean, p2_stat['0:2'].serv_mean,
#                         p2_stat['1:2'].serv_mean, p2_stat['2:1'].serv_mean, p2_stat['2:2'].serv_mean]
#         elif serve_return == 'return':
#             p1_stats = [p1_match_stat.retn_mean,
#                         p1_stat['0:0'].retn_mean, p1_stat['1:0'].retn_mean, p1_stat['0:1'].retn_mean,
#                         p1_stat['1:1'].retn_mean, p1_stat['2:0'].retn_mean, p1_stat['0:2'].retn_mean,
#                         p1_stat['1:2'].retn_mean, p1_stat['2:1'].retn_mean, p1_stat['2:2'].retn_mean]
#             p2_stats = [p2_match_stat.retn_mean,
#                         p2_stat['0:0'].retn_mean, p2_stat['1:0'].retn_mean, p2_stat['0:1'].retn_mean,
#                         p2_stat['1:1'].retn_mean, p2_stat['2:0'].retn_mean, p2_stat['0:2'].retn_mean,
#                         p2_stat['1:2'].retn_mean, p2_stat['2:1'].retn_mean, p2_stat['2:2'].retn_mean]
#
#         header = ['match', '0:0', '1:0', '0:1', '1:1', '2:0', '0:2', '1:2', '2:1', '2:2']
#
#     if stat_level == 'set_3':
#         if stat_aspect == 'baseline':
#             p1_stat = p1.set_baseline_3
#             p1_match_stat = p1.match_baseline
#             p2_stat = p2.set_baseline_3
#             p2_match_stat = p2.match_baseline
#         elif stat_aspect == 'impact':
#             p1_stat = p1.set_impact_3
#             p1_match_stat = p1.match_impact
#             p2_stat = p2.set_impact_3
#             p2_match_stat = p2.match_impact
#         elif stat_aspect == 'baseline diff':
#             p1_stat = p1.set_baseline_diff_3
#             p1_match_stat = p1.match_baseline_diff
#             p2_stat = p2.set_baseline_diff_3
#             p2_match_stat = p2.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             p1_stat = p1.set_impact_diff_3
#             p1_match_stat = p1.match_impact_diff
#             p2_stat = p2.set_impact_diff_3
#             p2_match_stat = p2.match_impact_diff
#
#         if serve_return == 'serve':
#             p1_stats = [p1_match_stat.serv_mean,
#                         p1_stat['0:0'].serv_mean, p1_stat['1:0'].serv_mean, p1_stat['0:1'].serv_mean,
#                         p1_stat['1:1'].serv_mean]
#             p2_stats = [p2_match_stat.serv_mean,
#                         p2_stat['0:0'].serv_mean, p2_stat['1:0'].serv_mean, p2_stat['0:1'].serv_mean,
#                         p2_stat['1:1'].serv_mean]
#         elif serve_return == 'return':
#             p1_stats = [p1_match_stat.retn_mean,
#                         p1_stat['0:0'].retn_mean, p1_stat['1:0'].retn_mean, p1_stat['0:1'].retn_mean,
#                         p1_stat['1:1'].retn_mean]
#             p2_stats = [p2_match_stat.retn_mean,
#                         p2_stat['0:0'].retn_mean, p2_stat['1:0'].retn_mean, p2_stat['0:1'].retn_mean,
#                         p2_stat['1:1'].retn_mean]
#
#         header = ['match', '0:0', '1:0', '0:1', '1:1']
#
#     if stat_level == 'game':
#         if stat_aspect == 'baseline':
#             p1_stat = p1.game_baseline
#             p1_match_stat = p1.match_baseline
#             p2_stat = p2.game_baseline
#             p2_match_stat = p2.match_baseline
#         elif stat_aspect == 'impact':
#             p1_stat = p1.game_impact
#             p1_match_stat = p1.match_impact
#             p2_stat = p2.game_impact
#             p2_match_stat = p2.match_impact
#         elif stat_aspect == 'baseline diff':
#             p1_stat = p1.game_baseline_diff
#             p1_match_stat = p1.match_baseline_diff
#             p2_stat = p2.game_baseline_diff
#             p2_match_stat = p2.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             p1_stat = p1.game_impact_diff
#             p1_match_stat = p1.match_impact_diff
#             p2_stat = p2.game_impact_diff
#             p2_match_stat = p2.match_impact_diff
#
#         if serve_return == 'serve':
#             p1_stats = [p1_match_stat.serv_mean,
#                         p1_stat[3].serv_mean, p1_stat[2].serv_mean, p1_stat[1].serv_mean,
#                         p1_stat[0].serv_mean, p1_stat[-1].serv_mean, p1_stat[-2].serv_mean,
#                         p1_stat[-3].serv_mean]
#             p2_stats = [p2_match_stat.serv_mean,
#                         p2_stat[3].serv_mean, p2_stat[2].serv_mean, p2_stat[1].serv_mean,
#                         p2_stat[0].serv_mean, p2_stat[-1].serv_mean, p2_stat[-2].serv_mean,
#                         p2_stat[-3].serv_mean]
#         elif serve_return == 'return':
#             p1_stats = [p1_match_stat.retn_mean,
#                         p1_stat[3].retn_mean, p1_stat[2].retn_mean, p1_stat[1].retn_mean,
#                         p1_stat[0].retn_mean, p1_stat[-1].retn_mean, p1_stat[-2].retn_mean,
#                         p1_stat[-3].retn_mean]
#             p2_stats = [p2_match_stat.retn_mean,
#                         p2_stat[3].retn_mean, p2_stat[2].retn_mean, p2_stat[1].retn_mean,
#                         p2_stat[0].retn_mean, p2_stat[-1].retn_mean, p2_stat[-2].retn_mean,
#                         p2_stat[-3].retn_mean]
#
#         header = ['match', '3', '2', '1', '0', '-1', '-2', '-3']
#
#     if stat_level == 'point':
#         if stat_aspect == 'baseline':
#             p1_stat = p1.point_baseline
#             p1_match_stat = p1.match_baseline
#             p2_stat = p2.point_baseline
#             p2_match_stat = p2.match_baseline
#         elif stat_aspect == 'impact':
#             p1_stat = p1.point_impact
#             p1_match_stat = p1.match_impact
#             p2_stat = p2.point_impact
#             p2_match_stat = p2.match_impact
#         elif stat_aspect == 'baseline diff':
#             p1_stat = p1.point_baseline_diff
#             p1_match_stat = p1.match_baseline_diff
#             p2_stat = p2.point_baseline_diff
#             p2_match_stat = p2.match_baseline_diff
#         elif stat_aspect == 'impact diff':
#             p1_stat = p1.point_impact_diff
#             p1_match_stat = p1.match_impact_diff
#             p2_stat = p2.point_impact_diff
#             p2_match_stat = p2.match_impact_diff
#
#         if serve_return == 'serve':
#             p1_stats = [p1_match_stat.serv_mean,
#                         p1_stat['0:0'].serv_mean, p1_stat['15:15'].serv_mean, p1_stat['30:30'].serv_mean,
#                         p1_stat['40:40'].serv_mean, p1_stat['15:0'].serv_mean, p1_stat['30:15'].serv_mean,
#                         p1_stat['40:30'].serv_mean, p1_stat['AD:40'].serv_mean, p1_stat['30:0'].serv_mean,
#                         p1_stat['40:15'].serv_mean, p1_stat['40:0'].serv_mean, p1_stat['0:15'].serv_mean,
#                         p1_stat['15:30'].serv_mean, p1_stat['30:40'].serv_mean, p1_stat['40:AD'].serv_mean,
#                         p1_stat['0:30'].serv_mean, p1_stat['15:40'].serv_mean, p1_stat['0:40'].serv_mean]
#             p2_stats = [p2_match_stat.serv_mean,
#                         p2_stat['0:0'].serv_mean, p2_stat['15:15'].serv_mean, p2_stat['30:30'].serv_mean,
#                         p2_stat['40:40'].serv_mean, p2_stat['15:0'].serv_mean, p2_stat['30:15'].serv_mean,
#                         p2_stat['40:30'].serv_mean, p2_stat['AD:40'].serv_mean, p2_stat['30:0'].serv_mean,
#                         p2_stat['40:15'].serv_mean, p2_stat['40:0'].serv_mean, p2_stat['0:15'].serv_mean,
#                         p2_stat['15:30'].serv_mean, p2_stat['30:40'].serv_mean, p2_stat['40:AD'].serv_mean,
#                         p2_stat['0:30'].serv_mean, p2_stat['15:40'].serv_mean, p2_stat['0:40'].serv_mean]
#
#         elif serve_return == 'return':
#             p1_stats = [p1_match_stat.retn_mean,
#                         p1_stat['0:0'].retn_mean, p1_stat['15:15'].retn_mean, p1_stat['30:30'].retn_mean,
#                         p1_stat['40:40'].retn_mean, p1_stat['15:0'].retn_mean, p1_stat['30:15'].retn_mean,
#                         p1_stat['40:30'].retn_mean, p1_stat['AD:40'].retn_mean, p1_stat['30:0'].retn_mean,
#                         p1_stat['40:15'].retn_mean, p1_stat['40:0'].retn_mean, p1_stat['0:15'].retn_mean,
#                         p1_stat['15:30'].retn_mean, p1_stat['30:40'].retn_mean, p1_stat['40:AD'].retn_mean,
#                         p1_stat['0:30'].retn_mean, p1_stat['15:40'].retn_mean, p1_stat['0:40'].retn_mean]
#             p2_stats = [p2_match_stat.retn_mean,
#                         p2_stat['0:0'].retn_mean, p2_stat['15:15'].retn_mean, p2_stat['30:30'].retn_mean,
#                         p2_stat['40:40'].retn_mean, p2_stat['15:0'].retn_mean, p2_stat['30:15'].retn_mean,
#                         p2_stat['40:30'].retn_mean, p2_stat['AD:40'].retn_mean, p2_stat['30:0'].retn_mean,
#                         p2_stat['40:15'].retn_mean, p2_stat['40:0'].retn_mean, p2_stat['0:15'].retn_mean,
#                         p2_stat['15:30'].retn_mean, p2_stat['30:40'].retn_mean, p2_stat['40:AD'].retn_mean,
#                         p2_stat['0:30'].retn_mean, p2_stat['15:40'].retn_mean, p2_stat['0:40'].retn_mean]
#
#         header = ['match', '0:0', '15:15', '30:30', '40:40', '15:0', '30:15', '40:30', 'AD:40', '30:0',
#                   '40:15', '40:0', '0:15', '15:30', '30:40', '40:AD', '0:30', '15:40', '0:40']
#
#     p1_stats = np.array(p1_stats)
#     p1_stats[np.isnan(p1_stats)] = 0
#     p2_stats = np.array(p2_stats)
#     p2_stats[np.isnan(p2_stats)] = 0
#
#     return flask.jsonify({'p1_stats': p1_stats.tolist(), 'p2_stats': p2_stats.tolist(), 'header': header})

if __name__ == '__main__':
    app.run()