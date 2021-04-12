import pandas as pd
import numpy as np
from scipy.optimize import least_squares as ls
from numpy import linalg as LA
from datetime import datetime, timedelta
from analysis_support import dec2dt, dec2dt2, write_summary, toYearFraction as tyf
import scipy.io as sio
from least_squares_init import lsq_int

# print(events)
# defining the jump function
events, x0 = lsq_int()


def jump(t, t0):
    "heaviside step function"
    o = np.zeros(len(t))
    ind = np.where(t == t0)[0][0]
    o[ind:] = 1.0
    return o


# print(jump(t,events[0]))


def all_jumps(t, *c):
    out = c[0] * jump(t, events[0])
    for ev_ind in range(len(events)):
        out += c[ev_ind] * jump(t, events[ev_ind])
    return out


# defining the function for the removal of trend, seasonal, tidal and co-seismic signals
# Periods in days for removal of tidal and seasonal signals
yr = 365.26
P1 = 13.6608 / yr
P2 = 14.7653 / yr
P3 = 27.5546 / yr
P4 = 182.62 / yr
P5 = yr / yr
P6 = 18.6


def fun(x, t, y):
    all_jump_args = x[12 : len(events) + 12]
    return (
        x[0]
        + x[1] * t
        + x[2] * np.cos(2 * np.pi * t / P1)
        + x[3] * np.sin(2 * np.pi * t / P1)
        + x[4] * np.cos(2 * np.pi * t / P2)
        + x[5] * np.sin(2 * np.pi * t / P2)
        + x[6] * np.cos(2 * np.pi * t / P3)
        + x[7] * np.sin(2 * np.pi * t / P3)
        + x[8] * np.cos(2 * np.pi * t / P4)
        + x[9] * np.sin(2 * np.pi * t / P4)
        + x[10] * np.cos(2 * np.pi * t / P5)
        + x[11] * np.sin(2 * np.pi * t / P5)
        + all_jumps(t, *all_jump_args)
        - y
    )


# function for regenerating the data after removal of signals
def gen_data(t, a, b, a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, *c):
    y = (
        a
        + b * t
        + a1 * np.cos(2 * np.pi * t / P1)
        + b1 * np.sin(2 * np.pi * t / P1)
        + a2 * np.cos(2 * np.pi * t / P2)
        + b2 * np.sin(2 * np.pi * t / P2)
        + a3 * np.cos(2 * np.pi * t / P3)
        + b3 * np.sin(2 * np.pi * t / P3)
        + a4 * np.cos(2 * np.pi * t / P4)
        + b4 * np.sin(2 * np.pi * t / P4)
        + a5 * np.cos(2 * np.pi * t / P5)
        + b5 * np.sin(2 * np.pi * t / P5)
        + all_jumps(t, *c)
    )
    return y


if __name__ == "__main__":
    print("Running least_squares_modules.py")