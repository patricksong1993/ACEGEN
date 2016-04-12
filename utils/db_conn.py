import MySQLdb

db = MySQLdb.connect("localhost", "root", "349968", "slam_point")
cursor = db.cursor()

# unused currently
# def all_matches_period(player, start_year, end_year, slam="'ausopen', 'usopen'"):
#     matches = {}
#     # as player 1
#     sql = "SELECT * FROM matches " \
#           "WHERE player1 = '" + player + "' " \
#           "AND slam IN (" + slam + ") " \
#           "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     matches[1] = data
#     sql = "SELECT * FROM matches " \
#           "WHERE player2 = '" + player + "' " \
#           "AND slam IN (" + slam + ") " \
#           "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     matches[2] = data
#     return matches


def all_match_ids_period(player, start_year, end_year, surface='hard'):
    matches = {}
    sql = "SELECT match_id FROM matches " \
          "WHERE player1 = '" + player + "' " \
          "AND surface ='" + surface + "'" \
          "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
    cursor.execute(sql)
    data = cursor.fetchall()
    matches[1] = [row[0] for row in data]
    sql = "SELECT match_id FROM matches " \
          "WHERE player2 = '" + player + "' " \
          "AND surface ='" + surface + "'" \
          "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
    cursor.execute(sql)
    data = cursor.fetchall()
    matches[2] = [row[0] for row in data]

    # db for non-grand slam
    sql = "SELECT match_id FROM pbp " \
          "WHERE player1 = '" + player + "' " \
          "AND surface ='" + surface + "'" \
          "AND tournament_level != 'grand' " \
          "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
    cursor.execute(sql)
    data = cursor.fetchall()
    matches[3] = [row[0] for row in data]
    sql = "SELECT match_id FROM pbp " \
          "WHERE player2 = '" + player + "' " \
          "AND surface ='" + surface + "'" \
          "AND tournament_level != 'grand' " \
          "AND year BETWEEN " + str(start_year) + " AND " + str(end_year)
    cursor.execute(sql)
    data = cursor.fetchall()
    matches[4] = [row[0] for row in data]
    return matches

def match_attributes(match_id):
    sql = "SELECT * FROM matches WHERE match_id = '%s'" %match_id
    cursor.execute(sql)
    data = cursor.fetchall()
    return data[0]

def match_attributes_pbp(match_id):
    sql = "SELECT * FROM pbp WHERE match_id = '%s'" %match_id
    cursor.execute(sql)
    data = cursor.fetchall()
    return data[0]

def match_points(match_id):
    sql = "SELECT * from points " \
          "WHERE match_id = '%s' ORDER BY PointNumber" \
          % match_id
    cursor.execute(sql)
    data = cursor.fetchall()
    return data



