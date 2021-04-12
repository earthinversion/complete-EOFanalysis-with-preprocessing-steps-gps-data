# import libraries
import pandas as pd
import numpy as np
from scipy.optimize import least_squares as ls
from numpy import linalg as LA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from analysis_support import dec2dt, dec2dt2, write_summary, toYearFraction as tyf
import matplotlib


matplotlib.rcParams["figure.figsize"] = (10.0, 6.0)
from matplotlib import style

style.use("seaborn")
import scipy.io as sio

## Python import
from least_squares_modules import events, x0, fun, gen_data, all_jumps
from least_squares_plot import plot_ls_results
import time

"""
- Utpal Kumar, 
  Institute of Earth Sciences,
  Academia Sinica
  @2020
  
This script aims to:
- Least squares model to remove the tidal and seasonal signals as well as co-seismic jumps
- Earthquakes selected are obtained from wilber 3 web interface
- Co-seismic jumps from all earthquakes (>5.1 Mw) except 2016-02-05 removed
- residual results are saved in Results/resd_dU.pickle
- lsq plot are saved at Results/LSQfigs
"""

start_time = time.perf_counter()

################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/"
dest = results_location + "SelectedData/"

summaryfile = write_summary(
    scriptname=__file__, filename=results_location + "summary.txt", mode="a"
)
################################################
# Periods in days for removal of tidal and seasonal signals
yr = 365.26
P1 = 13.6608 / yr
P2 = 14.7653 / yr
P3 = 27.5546 / yr
P4 = 182.62 / yr
P5 = yr / yr
P6 = 18.6


# read station information
stnloc = pd.read_csv(
    results_location + "stn_loc.txt",
    header=None,
    sep="\s+",
    names=["stn", "lon", "lat"],
)
stnloc.set_index("stn", inplace=True)

# load pickle data
dUU = pd.read_pickle(results_location + "dU_data.pickle")
dNN = pd.read_pickle(results_location + "dN_data.pickle")
dEE = pd.read_pickle(results_location + "dE_data.pickle")

# convert time to decimal year
year = []
for dd in dUU.index:
    year.append(round(tyf(dd), 5))

df_sel_stns = pd.read_csv(
    results_location + "stn_loc.txt", sep="\s+", names=["stn", "lon", "lat"]
)
selected_stations = df_sel_stns["stn"].values

output_result_N = {}
output_result_E = {}
output_result_U = {}
# output_result_N = {"tdata": np.array(year)}
# output_result_E = {"tdata": np.array(year)}
# output_result_U = {"tdata": np.array(year)}
calcLSQ = 1
plot_test_station = 1
if calcLSQ:
    ## Least square fitting

    for test_stn in selected_stations:
        print(f"Least square fitting the data for the station: {test_stn}")
        yval = np.array(dUU[test_stn + "_U"])
        yvalN = np.array(dNN[test_stn + "_N"])
        yvalE = np.array(dEE[test_stn + "_E"])
        xval = np.array(year)
        # print(xval)
        res_lsq = ls(fun, x0, args=(xval, yval))
        y_lsq = gen_data(xval, *res_lsq.x)
        output_result_U[test_stn] = yval - y_lsq

        res_lsqN = ls(fun, x0, args=(xval, yvalN))
        y_lsqN = gen_data(xval, *res_lsqN.x)
        output_result_N[test_stn] = yvalN - y_lsqN

        res_lsqE = ls(fun, x0, args=(xval, yvalE))
        y_lsqE = gen_data(xval, *res_lsqE.x)
        output_result_E[test_stn] = yvalE - y_lsqE

        trend = res_lsq.x[0] + xval * res_lsq.x[1]
        trendN = res_lsqN.x[0] + xval * res_lsqN.x[1]
        trendE = res_lsqE.x[0] + xval * res_lsqE.x[1]

        seasonality = (
            res_lsq.x[2] * np.cos(2 * np.pi * xval / P1)
            + res_lsq.x[3] * np.sin(2 * np.pi * xval / P1)
            + res_lsq.x[4] * np.cos(2 * np.pi * xval / P2)
            + res_lsq.x[5] * np.sin(2 * np.pi * xval / P2)
            + res_lsq.x[6] * np.cos(2 * np.pi * xval / P3)
            + res_lsq.x[7] * np.sin(2 * np.pi * xval / P3)
            + res_lsq.x[8] * np.cos(2 * np.pi * xval / P4)
            + res_lsq.x[9] * np.sin(2 * np.pi * xval / P4)
            + res_lsq.x[10] * np.cos(2 * np.pi * xval / P5)
            + res_lsq.x[11] * np.sin(2 * np.pi * xval / P5)
        )

        seasonalityN = (
            res_lsqN.x[2] * np.cos(2 * np.pi * xval / P1)
            + res_lsqN.x[3] * np.sin(2 * np.pi * xval / P1)
            + res_lsqN.x[4] * np.cos(2 * np.pi * xval / P2)
            + res_lsqN.x[5] * np.sin(2 * np.pi * xval / P2)
            + res_lsqN.x[6] * np.cos(2 * np.pi * xval / P3)
            + res_lsqN.x[7] * np.sin(2 * np.pi * xval / P3)
            + res_lsqN.x[8] * np.cos(2 * np.pi * xval / P4)
            + res_lsqN.x[9] * np.sin(2 * np.pi * xval / P4)
            + res_lsqN.x[10] * np.cos(2 * np.pi * xval / P5)
            + res_lsqN.x[11] * np.sin(2 * np.pi * xval / P5)
        )

        seasonalityE = (
            res_lsqE.x[2] * np.cos(2 * np.pi * xval / P1)
            + res_lsqE.x[3] * np.sin(2 * np.pi * xval / P1)
            + res_lsqE.x[4] * np.cos(2 * np.pi * xval / P2)
            + res_lsqE.x[5] * np.sin(2 * np.pi * xval / P2)
            + res_lsqE.x[6] * np.cos(2 * np.pi * xval / P3)
            + res_lsqE.x[7] * np.sin(2 * np.pi * xval / P3)
            + res_lsqE.x[8] * np.cos(2 * np.pi * xval / P4)
            + res_lsqE.x[9] * np.sin(2 * np.pi * xval / P4)
            + res_lsqE.x[10] * np.cos(2 * np.pi * xval / P5)
            + res_lsqE.x[11] * np.sin(2 * np.pi * xval / P5)
        )

        jumps = all_jumps(xval, *res_lsq.x[12 : len(events) + 12])
        jumpsN = all_jumps(xval, *res_lsqN.x[12 : len(events) + 12])
        jumpsE = all_jumps(xval, *res_lsqE.x[12 : len(events) + 12])
        summaryfile.write(
            f"LSQ for station: {test_stn}, see the plot at Results/LSQfigs/model_fitting_[N,E,U]_{test_stn}.png"
        )
        if plot_test_station:
            plot_ls_results(
                test_stn,
                xval,
                yval,
                res_lsq,
                yvalN,
                res_lsqN,
                yvalE,
                res_lsqE,
                trend,
                trendN,
                trendE,
                seasonality,
                seasonalityN,
                seasonalityE,
                jumps,
                jumpsN,
                jumpsE,
            )
dfE = pd.DataFrame.from_dict(output_result_E)
dfN = pd.DataFrame.from_dict(output_result_N)
dfU = pd.DataFrame.from_dict(output_result_U)

dfE.to_pickle(results_location + "resd_dE.pickle")
dfN.to_pickle(results_location + "resd_dN.pickle")
dfU.to_pickle(results_location + "resd_dU.pickle")

## save in mat format
sio.savemat(
    results_location + "all_data.mat",
    {
        "dN": dfN,
        "dE": dfE,
        "dU": dfU,
        "slat": df_sel_stns["lat"].values,
        "slon": df_sel_stns["lon"].values,
        "tdata": np.array(year),
    },
)

print("--- Finished in %s seconds ---" % (time.perf_counter() - start_time))