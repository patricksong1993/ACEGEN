from classes.player import Player
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.setrecursionlimit(10000)

player = 'Roger Federer'
set_level = '0:0'
Player.surface = 'hard'

match_baseline_s = []
match_impact_s = []
set_baseline_s = []
set_impact_s = []

match_baseline_r = []
match_impact_r = []
set_baseline_r = []
set_impact_r = []


Player.end_year = '2012-12-31'
Player.start_year = '2012-01-01'
Player.clean_cached_players()
p = Player(player)
Player.calculate_all_ts()

match_baseline_s.append(p.match_baseline_ts.serv_mean)
match_impact_s.append(p.match_impact_ts.serv_mean)
set_baseline_s.append(p.set_baseline_3_ts[set_level].serv_mean)
set_impact_s.append(p.set_impact_3_ts[set_level].serv_mean)

match_baseline_r.append(p.match_baseline_ts.retn_mean)
match_impact_r.append(p.match_impact_ts.retn_mean)
set_baseline_r.append(p.set_baseline_3_ts[set_level].retn_mean)
set_impact_r.append(p.set_impact_3_ts[set_level].retn_mean)

Player.end_year = '2013-12-31'
Player.start_year = '2013-01-01'
Player.clean_cached_players()
p = Player(player)
Player.calculate_all_ts()

match_baseline_s.append(p.match_baseline_ts.serv_mean)
match_impact_s.append(p.match_impact_ts.serv_mean)
set_baseline_s.append(p.set_baseline_3_ts[set_level].serv_mean)
set_impact_s.append(p.set_impact_3_ts[set_level].serv_mean)

match_baseline_r.append(p.match_baseline_ts.retn_mean)
match_impact_r.append(p.match_impact_ts.retn_mean)
set_baseline_r.append(p.set_baseline_3_ts[set_level].retn_mean)
set_impact_r.append(p.set_impact_3_ts[set_level].retn_mean)

Player.end_year = '2014-12-31'
Player.start_year = '2014-01-01'
Player.clean_cached_players()
p = Player(player)
Player.calculate_all_ts()

match_baseline_s.append(p.match_baseline_ts.serv_mean)
match_impact_s.append(p.match_impact_ts.serv_mean)
set_baseline_s.append(p.set_baseline_3_ts[set_level].serv_mean)
set_impact_s.append(p.set_impact_3_ts[set_level].serv_mean)

match_baseline_r.append(p.match_baseline_ts.retn_mean)
match_impact_r.append(p.match_impact_ts.retn_mean)
set_baseline_r.append(p.set_baseline_3_ts[set_level].retn_mean)
set_impact_r.append(p.set_impact_3_ts[set_level].retn_mean)

Player.end_year = '2015-12-31'
Player.start_year = '2015-01-01'
Player.clean_cached_players()
p = Player(player)
Player.calculate_all_ts()

match_baseline_s.append(p.match_baseline_ts.serv_mean)
match_impact_s.append(p.match_impact_ts.serv_mean)
set_baseline_s.append(p.set_baseline_3_ts[set_level].serv_mean)
set_impact_s.append(p.set_impact_3_ts[set_level].serv_mean)

match_baseline_r.append(p.match_baseline_ts.retn_mean)
match_impact_r.append(p.match_impact_ts.retn_mean)
set_baseline_r.append(p.set_baseline_3_ts[set_level].retn_mean)
set_impact_r.append(p.set_impact_3_ts[set_level].retn_mean)


print match_baseline_s
print set_baseline_s
print match_baseline_r
print set_baseline_r
set_baseline_r[3] = 0.468559
print match_impact_s
print set_impact_s
print match_impact_r
print set_impact_r

fig = plt.figure()

plt.plot([2012,2013,2014,2015], match_baseline_r, label='Match Level')
plt.plot([2012,2013,2014,2015], set_baseline_r, label='Set Level 0:0')
plt.axis([2012, 2015, 0.38, 0.48], 'ro')
plt.xticks([2012,2013,2014,2015], ['2012','2013','2014','2015'])
plt.xlabel('Year')
plt.ylabel('Return Baseline Percentage')
plt.legend()
plt.show()
fig.savefig('rofe_rb.png')