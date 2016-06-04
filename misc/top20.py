import sys
import matplotlib.pyplot as plt
from classes.player import Player
import numpy as np


top = ['Novak Djokovic', 'Andy Murray', 'Roger Federer', 'Stan Wawrinka', 'Rafael Nadal', 'Kei Nishikori', 'Jo-Wilfried Tsonga', 'Tomas Berdych', 'Milos Raonic', 'Richard Gasquet', 'Marin Cilic', 'David Ferrer', 'David Goffin', 'Gael Monfils', 'Dominic Thiem', 'Roberto Bautista-Agut', 'John Isner', 'Gilles Simon', 'Nick Kyrgios', 'Kevin Anderson']
top_abbr = ['NoDj', 'AnMu', 'RoFe', 'StWa', 'RaNa', 'KeNi', 'JoTs', 'ToBe', 'MiRa', 'RiGa', 'MaCi', 'DaFe', 'DaGo', 'GaMo', 'DoTh', 'RoBa', 'JoIs', 'GiSi', 'NiKy', 'KeAn']

sys.setrecursionlimit(10000)

Player.start_year = '2012-01-01'
Player.end_year = '2015-12-31'
Player.surface = 'hard'

serv_bs = []
serv_bs_std = []
retn_bs = []
retn_bs_std = []

for p in top:
    player = Player(p)

Player.calculate_all_ts()

for p in top:
    player = Player.cached_players[p]
    print p
    serv_bs.append(player.set_baseline_3_ts['0:0'].serv_mean-player.match_baseline.serv_mean)
    retn_bs.append(player.set_baseline_3_ts['0:0'].retn_mean-player.match_baseline.retn_mean)

print top
print serv_bs
print serv_bs_std
print retn_bs
print retn_bs_std


n = top_abbr
x = serv_bs
y = retn_bs
fig = plt.figure()
plt.scatter(x,y)
for label, x, y in zip(n, x, y):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-1, 1),
        textcoords = 'offset points', ha = 'right', va = 'bottom')
plt.xlabel('Serve Baseline Difference')
plt.ylabel('Return Baseline Difference')
plt.show()
#
# fig.savefig('01i.png')



