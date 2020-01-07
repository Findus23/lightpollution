import math

import numpy as np
from matplotlib import pyplot as plt

width = 100

grid = np.zeros((width, width), dtype=np.uint64)

all_data: dict = np.load("out.npy", allow_pickle=True).item()
print(all_data)
for y in range(width):
    print(y)
    for x in range(width):
        for start, bins in all_data.items():
            pixpos = np.array([x, y])
            myradians = math.atan2(start[0] - x, start[1] - y)
            angle = np.degrees(myradians)
            if not np.isnan(angle):
                bin = int(round(angle) % 360)
                grid[x, y] += bins[bin]
        # exit()
grid = grid.T
# grid[grid > 200] = 200
plt.imshow(grid)
plt.colorbar()
plt.show()
