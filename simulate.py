import math

import imageio
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import zoom, gaussian_filter

img = imageio.imread('input_slight_blur.png')
print(img)
# img = zoom(img, 3)
width = 100
numstarts = 6
i = np.linspace(0, 360, numstarts, endpoint=False)
i += np.random.randint(-20, 20, numstarts)
r = width / 2.3
ang = np.radians(i)
xstart = np.cos(ang) * r * np.random.randint(80, 110, numstarts) / 100 + width / 2
ystart = np.sin(ang) * r * np.random.randint(80, 110, numstarts) / 100 + width / 2
print(xstart, ystart)
plt.scatter(xstart, ystart, c="red")
plt.imshow(img)
plt.show()

all_data = {}
show = True
for i in range(numstarts):
    pos = (xstart[i], ystart[i])
    start = np.array(pos)

    bins = np.zeros(360)
    for y, row in enumerate(img):
        for x, value in enumerate(row):
            pixpos = np.array([x, y])
            myradians = math.atan2(start[0] - x, start[1] - y)
            angle = np.degrees(myradians)
            # print(angle)
            # exit()
            if not np.isnan(angle):
                bin = int(round(angle) % 360)
                bins[bin] += value
            else:
                print(pixpos)
    bins = gaussian_filter(bins, sigma=1)
    all_data[pos] = bins
    print(pos)
    if show:
        plt.plot(np.arange(0, 360), bins)
        plt.xlabel("angle")
        plt.savefig("fig.png")
        plt.show()
        show = False
np.save("out", all_data)
