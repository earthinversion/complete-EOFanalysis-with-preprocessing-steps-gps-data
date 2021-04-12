import pandas as pd
import numpy as np
from scipy.optimize import least_squares as ls
from numpy import linalg as LA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from analysis_support import dec2dt, dec2dt2, write_summary, toYearFraction as tyf
import matplotlib
import scipy.io as sio

################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/"
dest = results_location + "SelectedData/"

summaryfile = write_summary(
    scriptname=__file__, filename=results_location + "summary.txt", mode="a"
)
################################################
dU_1 = pd.read_pickle(results_location + "dU_data.pickle")


# convert time to decimal year
year = []
for dd in dU_1.index:
    year.append(round(tyf(dd), 5))

dUU = pd.read_pickle(results_location + "resd_dU.pickle")
dNN = pd.read_pickle(results_location + "resd_dN.pickle")
dEE = pd.read_pickle(results_location + "resd_dE.pickle")
row, col = dUU.shape

dataNN = np.empty((row, col))
dataEE = np.empty((row, col))
dataUU = np.empty((row, col))
for i in range(col):
    dataNN[:, i] = dNN.iloc[:, i]
    dataEE[:, i] = dEE.iloc[:, i]
    dataUU[:, i] = dUU.iloc[:, i]


df_sel_stns = pd.read_csv(
    results_location + "stn_loc.txt", sep="\s+", names=["stn", "lon", "lat"]
)
lat_vals = []
lon_vals = []

for stn in dUU.columns.values:
    if stn in df_sel_stns["stn"].values:
        lon_vals.append(df_sel_stns[df_sel_stns["stn"] == stn]["lon"].values[0])
        lat_vals.append(df_sel_stns[df_sel_stns["stn"] == stn]["lat"].values[0])

## save in mat format
sio.savemat(
    results_location + "all_data.mat",
    {
        "dN": dataNN,
        "dE": dataEE,
        "dU": dataUU,
        "slat": lat_vals,
        "slon": lon_vals,
        "tdata": np.array(year),
    },
)