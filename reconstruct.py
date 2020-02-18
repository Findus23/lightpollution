import json
import math

import numpy as np
from matplotlib import pyplot as plt

from data import points, bounds

simple = True


def distance(origin, destination):
    """
    https://gist.github.com/rochacbruno/2883505
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


cloud_height = 0.9


def distance_to_angle(distance: float):
    # if randint(0,1000)==0:
    #     print(distance,int(round(np.degrees(np.arctan(2 * cloud_height / distance)))))
    return np.degrees(np.arctan(2 * cloud_height / distance))


def calculate(filename: str, simple: bool, spline: bool = False, checkhorizon: bool = False):
    output = np.zeros((gridsize, gridsize), dtype=np.float64)

    # all_data: dict = np.load("out.npy", allow_pickle=True).item()
    all_data = points
    xspace = np.linspace(bounds["lon"]["lower"], bounds["lon"]["upper"], gridsize)
    yspace = np.linspace(bounds["lat"]["lower"], bounds["lat"]["upper"], gridsize)
    xgrid, ygrid = np.meshgrid(xspace, yspace)
    print(bounds)
    for yindex in range(gridsize):
        # realy = y / gridsize * bounds["y"]["width"] + bounds["y"]["lower"]
        print(yindex)
        for xindex in range(gridsize):
            y = ygrid[xindex, yindex]
            x = xgrid[xindex, yindex]
            # realx = x / gridsize * bounds["x"]["width"] + bounds["x"]["lower"]
            for point in all_data:
                if simple:
                    bins = point.brightnesses
                else:
                    bins = point.brightnesses2d
                    dist = distance((x, y), point.coord)
                    # print(dist)
                    ang = distance_to_angle(dist)
                    # print(ang)
                myradians = math.atan2(point.coord[1] - y, point.coord[0] - x)
                directionangle = np.degrees(myradians)
                if not np.isnan(directionangle):
                    if not spline:
                        bin = int(round(directionangle)) % 360
                    if simple:
                        value = bins[bin]
                    else:
                        if spline:
                            if checkhorizon:
                                horizon = point.horizon_spline(directionangle % 360)
                                if ang < horizon:
                                    value = 0
                                else:
                                    value = point.spline(ang, directionangle % 360)
                            else:
                                value = point.spline(ang, directionangle % 360)
                        else:
                            angle = int(round(ang))
                            value = bins[angle, bin]
                    output[xindex, yindex] += value
            # exit()
    output = output.T
    # output[output < 30] = np.nan
    plt.imshow(output, origin="lower", interpolation="bilinear")
    plt.colorbar()
    plt.imsave(filename, output, origin="lower")
    data = {
        "filename": filename,
        "bounds": [
            [bounds["lon"]["lower"], bounds["lat"]["lower"]],
            [bounds["lon"]["upper"], bounds["lat"]["upper"]]
        ]
    }
    # plt.show()
    return data


if __name__ == '__main__':
    gridsize = 1000
    images = [
        calculate("simple.png", simple=True),
        calculate("clouds.png", simple=False, spline=False),
        calculate("spline.png", simple=False, spline=True),
        calculate("horizon.png", simple=False, spline=True,checkhorizon=True),
    ]
    with open("settings.json", "w") as f:
        json.dump(images, f)
