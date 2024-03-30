import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt


def solarcalc(num, wp, lat_deg, lon_deg):
    # Constants
    ITERATIONS: int = 8760
    SUN_LAT: float = 23.5
    NL_LAT: float = 52.1

    lat = np.deg2rad(lat_deg)
    lon = np.deg2rad(lon_deg)

    mt2014 = np.array(read_csv("./static/mt2014.txt",
                               header=None, usecols=[0, 2]))
    idif = np.float32(mt2014[:, 0])  # zonneschijnduur per 0,1 uur
    idir = np.float32(mt2014[:, 1])  # globale straling

    lat_sun = np.empty(ITERATIONS)
    lon_sun = np.empty(ITERATIONS)
    lat_sun_deg = np.empty(ITERATIONS)
    lon_sun_deg = np.empty(ITERATIONS)
    isp = np.empty(ITERATIONS)
    theta = np.empty(ITERATIONS)
    power = np.empty(ITERATIONS)

    for i in range(ITERATIONS):

        lat_sun_deg[i] = (90 - NL_LAT) * np.sin((i - 6) * 2 * np.pi / 24) - SUN_LAT * np.sin(
            (101.25 * 24 + i) * np.pi * 2 / (24 * 365))

        if i == 0:
            lon_sun_deg[i] = -180
        else:
            lon_sun_deg[i] = lon_sun_deg[i - 1] + 15
            if i % 24 == 0:
                lon_sun_deg[i] = lon_sun_deg[i - 1] + 15 - 360

        # a[i] = np.sin(lat_sun[i] - lat / 2) ** 2 + np.cos(lat_sun[i]) * np.cos(lat) * np.sin(
        #     lon_sun[i] - lon / 2) ** 2
        #
        # theta[i] = 2 * np.arctan(np.sqrt(a[i] / np.sqrt(1 - a[i])))

        lat_sun[i] = np.deg2rad(lat_sun_deg[i])
        lon_sun[i] = np.deg2rad(lon_sun_deg[i])


        # Calculate angular distance in rads
        theta[i] = np.arccos(
            np.sin(lat_sun[i]) * np.sin(lat) + np.cos(lat_sun[i]) * np.cos(lat) * np.cos(lon_sun[i] - lon))

        # theta[i] = theta[i] * 180 / np.pi

        if theta[i] < (0.5 * np.pi):  # less than 90 degrees = direct sunlight
            isp[i] = np.cos(theta[i]) * idir[i] + idif[i] * (0.5 + np.cos(lat / 2))

        else:
            isp[i] = idif[i] * (0.5 + np.cos(lat / 2))

        # numpy vectorization possible below
        power[i] = 0.8 * isp[i] * wp * num / 1_000_000  # kWh

    esum = int(sum(power))

    res = {0: esum, 1: range(ITERATIONS), 2: power}

    return res
