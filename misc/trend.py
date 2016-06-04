import sys
import matplotlib.pyplot as plt
from classes.player import Player
import numpy as np



sys.setrecursionlimit(10000)

Player.start_year = '2012-01-01'
Player.end_year = '2012-12-31'
Player.surface = 'hard'


for y in ['2012','2013']
serv_bs = []
serv_bs_std = []
retn_bs = []
retn_bs_std = []

for p in top:
    player = Player(p)
    print p
    serv_bs.append(player.set_baseline_3['0:0'].serv_mean)
    serv_bs_std.append(player.set_baseline_3['0:0'].serv_std)
    retn_bs.append(player.set_baseline_3['0:0'].retn_mean)
    retn_bs_std.append(player.set_baseline_3['0:0'].retn_std)

print top
print serv_bs
print serv_bs_std
print retn_bs
print retn_bs_std


n = top_abbr
z = serv_bs
y = retn_bs

plt.scatter(y,z)
for label, x, y in zip(n, y, z):
    plt.annotate(
        label,
        xy = (x, y), xytext = (-1, 1),
        textcoords = 'offset points', ha = 'right', va = 'bottom')

plt.show()



