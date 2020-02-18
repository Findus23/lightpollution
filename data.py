from dataclasses import dataclass
from typing import Tuple, List

import numpy as np
from scipy.interpolate import RectBivariateSpline, CubicSpline


@dataclass
class Measurepoint():
    def __init__(self, coord: Tuple[float, float], filename: str, name: str):
        self.coord = coord
        self.filename = filename
        self.name = name
        self.brightnesses = self.load_horizontal_sky_brightness()
        self.brightnesses2d = self.load_2d_sky_brightness()
        self.spline = self.load_spline(self.brightnesses2d)
        self.horizon_spline = self.load_horizon_spline()

    def load_horizontal_sky_brightness(self) -> List[float]:
        brightnesses = []
        mags = []
        with open(f"../rohdaten/{self.filename} - Horizontal Sky Brightness Graph.csv") as f:
            for _ in range(29):
                next(f)
            for line in f:
                if line == "\n":
                    continue
                azimuth, sky_brightness, luminance, cct = map(float, line.split(","))
                brightnesses.append(luminance)
                mags.append(10 ** (-0.4 * sky_brightness) * 108e6)

        # plt.plot(range(len(brightnesses)), brightnesses)
        # plt.show()
        assert len(brightnesses) == 360
        brightnesses = np.array(brightnesses)
        # mags = np.array(mags)
        # print(brightnesses, mags)
        # print(brightnesses / mags)
        # plt.plot(brightnesses, mags)
        # plt.show()
        brightnesses = np.roll(brightnesses, 180)
        return brightnesses

    @property
    def filename2d(self):
        return f"../rohdaten/{self.filename}-2D-matrix.csv"

    def load_2d_sky_brightness(self):
        data = np.loadtxt(
            self.filename2d,
            skiprows=241,
            delimiter=",",
            max_rows=92,
            usecols=range(1, 361)
        )
        data = np.roll(data, 180, axis=1)
        data = np.flipud(data)
        return 10 ** (-0.4 * data) * 108e6

    def load_horizon_spline(self) -> CubicSpline:
        horizon = np.loadtxt(
            self.filename2d,
            skiprows=57,
            delimiter=",",
            max_rows=237 - 58,
            usecols=(0, 1)
        )
        horizon[:, 1] = 90 - horizon[:, 1]  # degrees are upside down
        cs = CubicSpline(horizon[:, 0], horizon[:, 1])
        # x = np.linspace(0, 360, 1000)
        # plt.plot(horizon[:, 0], horizon[:, 1])
        # plt.plot(x, cs(x))
        # plt.show()
        return cs

    def load_spline(self, data2d: np.ndarray) -> RectBivariateSpline:
        x, y = np.arange(data2d.shape[0]), np.arange(data2d.shape[1])
        return RectBivariateSpline(x, y, data2d)


points = [
    Measurepoint(filename="IMG_0172", name="Mistelbach-Süd", coord=(48.5232506, 16.5654793)),
    Measurepoint(filename="IMG_0176", name="Mistelbach-West", coord=(48.5747355, 16.498188)),
    Measurepoint(filename="IMG_0182", name="Mistelbach-Nordwest", coord=(48.5945091, 16.5278206)),
    Measurepoint(filename="IMG_0186", name="Mistelbach-Nord", coord=(48.6069419, 16.5606171)),
    Measurepoint(filename="IMG_0190", name="Mistelbach-Nordost", coord=(48.5913925, 16.6311699)),
    Measurepoint(filename="IMG_0194", name="Mistelbach-Südost", coord=(48.5471377, 16.6404243)),
]

# interpolator = points[0].load_interpolation(points[0].brightnesses2d)
# zoom = 5
# z = np.zeros((93 * zoom, 360 * zoom))
# for x in range(93 * zoom):
#     print(x)
#     for y in range(360 * zoom):
#         z[x, y] = interpolator(x / zoom, y / zoom)
# plt.imshow(z, origin="lower")
# plt.colorbar()
# plt.show()
#
# plt.imshow(points[0].brightnesses2d, origin="lower")
# plt.colorbar()
# plt.show()

bounds = {
    "lon": {
        "upper": max(p.coord[0] for p in points) + 0.2,
        "lower": min(p.coord[0] for p in points) - 0.2
    },
    "lat": {
        "upper": max(p.coord[1] for p in points) + 0.2,
        "lower": min(p.coord[1] for p in points) - 0.2
    }
}
# bounds["x"]["width"] = bounds["x"]["upper"] - bounds["x"]["lower"]
# bounds["y"]["width"] = bounds["y"]["upper"] - bounds["y"]["lower"]
