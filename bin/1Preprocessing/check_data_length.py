import pandas as pd
import numpy as np
import glob, os
import matplotlib.pyplot as plt
import seaborn as sns
from shutil import copy2

# from dec2dt import dec2dt, dec2dt2
from functools import reduce

# from toYearFraction import toYearFraction as tyf
from analysis_support import (
    create_dir,
    rem_dir,
    dec2dt,
    dec2dt2,
    write_summary,
    toYearFraction as tyf,
)

"""
- Utpal Kumar, 
  Institute of Earth Sciences,
  Academia Sinica
  @2020
  
This script aims to:
- store the start, end time and number of points in the time series for each stations in dataInspection.txt file
- visualizing the data length by histogram (set vizhist = 1 in the script below) and output s_e_timeHistogram.png
- select the data based on the start and end time and copy it into new directory, SelectedData
- cut the time series using the start and end time and removing the 2 sigma outliers
- resampling the data for each day and interpolating for unavailable entries
- removing the stations with NaNs (comes from large gaps in interpolation scheme)
- select stations within 50 km from the EQ
- write the selected stations information in stn_loc.txt
- store data in pickle format and mat format separately for dN, dE, and dU for easy read in other scripts: dU_data.[pickle,mat]
"""

## Set parameters
### Set time
evtime = 2016.098  # Meinong earthquake time
starttime = evtime - 0.5
endtime = evtime + 1

mlat, mlon = 22.9387, 120.5928
distEQ = 80  # within 50 km from the EQ
### Other params
vizhist = 0  # data availablity histogram
sigma_val = 2  # sigma for outliers

## forcely reject the list of stations
rejectstn = [] #["ERLN"]

root_location = os.path.join("..","..") #"../../"
results_location = os.path.join(root_location , "Results/")
datasource = os.path.join(root_location, "TimeSeriesReleased1993.01.01_2018.04.30/")
dest = os.path.join(results_location , "SelectedData/")
datainspection = os.path.join(results_location , "dataInspection.txt")

# minimum number of data points in a time series to be selected
req_num_points = 300 * (endtime - starttime)  ## 300 points in a year on avg

summaryfile = write_summary(
    scriptname=__file__, filename=results_location + "summary.txt", mode="w"
)

summaryfile.write(
    f"EOF analysis for the time series between {dec2dt2(starttime)} & {dec2dt2(endtime)}"
)
summaryfile.write(f"Meinong EQ: {dec2dt2(evtime)}")
############################################################


# Writing dataInspection.txt file
all_data_files = glob.glob(datasource + "*.COR")
summaryfile.write(f"Total number of stations to begin with: {len(all_data_files)}")

## extract the start time, end time and number of points in the time series for each stations
with open(datainspection, "w") as ff:
    for dfile in all_data_files:
        df = pd.read_csv(dfile, header=None, sep="\s+")
        dfile_base = os.path.basename(dfile)
        stn = dfile_base.split(".")[0]
        stime = df.iloc[:, 0].min()
        etime = df.iloc[:, 0].max()
        tdataPoints = df.shape[0]
        df_cut = df[(df.iloc[:, 0] > starttime) & (df.iloc[:, 0] < endtime)]
        npts_in_range = df_cut.shape[0]
        ff.write(
            "{} {:.4f} {:.4f} {} {}\n".format(
                stn, stime, etime, tdataPoints, npts_in_range
            )
        )
datalength = pd.read_csv(
    datainspection,
    header=None,
    sep="\s+",
    names=["stn", "stime", "etime", "tdataPoints", "npts_in_range"],
)

## Visualizing the data length by histogram
if vizhist:
    fig, ax = plt.subplots(2, 1, sharex=True)
    sns.distplot(
        datalength["stime"].values,
        hist=True,
        kde=False,
        bins="auto",
        color="darkblue",
        hist_kws={"edgecolor": "black", "label": "Start Time"},
        ax=ax[0],
    )
    ax[0].set_title("Starting Time")
    ax[0].legend()
    sns.distplot(
        datalength["etime"].values,
        hist=True,
        kde=False,
        bins=10,
        color="darkblue",
        hist_kws={"edgecolor": "black", "label": "End Time"},
        ax=ax[1],
    )
    ax[1].set_title("End Time")
    ax[1].legend()
    plt.xlim(datalength["stime"].min(), datalength["etime"].max())
    plt.savefig(results_location + "s_e_timeHistogram.png", bbox_inches="tight")

## Select the data files based on start time, end time and npts
selData = datalength[
    (datalength["stime"] < starttime)
    & (datalength["etime"] > endtime)
    & (datalength["npts_in_range"] > req_num_points)
]

## Copy selected files

rem_dir(dest)
create_dir(dest)

## list of stations to be rejected
for selstn in selData["stn"].values:
    if selstn not in rejectstn:
        copy2(datasource + selstn + ".COR", dest)


## New Selected Data
selstns_all = glob.glob(dest + "*.COR")
summaryfile.write(f"Number of stations selected: {len(selstns_all)} ")
selstns = [os.path.basename(stn).split(".")[0] for stn in selstns_all]

## Writing all selected data into a data frame
main_dU = []
main_dN = []
main_dE = []
for s1 in selstns:
    duu = "{}_U".format(s1)
    dnn = "{}_N".format(s1)
    dee = "{}_E".format(s1)
    selGroundMotion = pd.read_csv(
        dest + s1 + ".COR",
        header=None,
        delimiter=r"\s+",
        names=["year", "lat", "lon", "hgt", "dN", "dE", "dU", "FLAG(reserved)"],
    )
    timeVal = dec2dt(selGroundMotion.values[:, 0])
    selGroundMotion["Time"] = timeVal
    selGroundMotion.set_index("Time", inplace=True)

    # Extracting data between start and end time and renaming the columns
    df2 = selGroundMotion.loc[
        (selGroundMotion.year > starttime) & (selGroundMotion.year < endtime),
        ["dN", "dE", "dU"],
    ].rename(columns={"dN": dnn, "dE": dee, "dU": duu})
    # Removing the 2-sigma outliers
    df2 = df2[
        (np.abs(df2[dnn] - df2[dnn].mean()) <= sigma_val * df2[dnn].std())
        | (np.abs(df2[dee] - df2[dee].mean()) <= sigma_val * df2[dee].std())
        | (np.abs(df2[duu] - df2[duu].mean()) <= sigma_val * df2[duu].std())
    ]

    # # # Resampling the data for each day and interpolating for unavailable entries
    df3 = df2.resample("D").last().interpolate(method="nearest")
    # df3=df2 #no interpolation
    # Storing each station data in a single list separately for dN, dE and dU
    main_dN.append(df3[dnn])
    main_dE.append(df3[dee])
    main_dU.append(df3[duu])

# Concatenating all the data frames in the list to make a single data frame
dNN = reduce(lambda x, y: pd.concat([x, y], axis=1), main_dN)
dEE = reduce(lambda x, y: pd.concat([x, y], axis=1), main_dE)
dUU = reduce(lambda x, y: pd.concat([x, y], axis=1), main_dU)


## Removing the stations with NaNs (comes from large gaps in interpolation scheme)
allcols = dUU.columns.values
cols_rem = []
for i in range(len(allcols)):
    if np.isnan(dUU.iloc[0, i]) or np.isnan(dUU.iloc[-1, i]):
        cols_rem.append(allcols[i])

allcolsE = dEE.columns.values
cols_remE = []
for i in range(len(allcolsE)):
    if np.isnan(dEE.iloc[0, i]) or np.isnan(dEE.iloc[-1, i]):
        cols_remE.append(allcolsE[i])

allcolsN = dNN.columns.values
cols_remN = []
for i in range(len(allcolsN)):
    if np.isnan(dNN.iloc[0, i]) or np.isnan(dNN.iloc[-1, i]):
        cols_remN.append(allcolsN[i])

dUU = dUU.drop(cols_rem, axis=1)
dNN = dNN.drop(cols_remN, axis=1)
dEE = dEE.drop(cols_remE, axis=1)

# ## Writing the selected stations locations in a textfile stn_loc.txt

# Read the available station info from the catalog
stncat = pd.read_csv(
    "new_station_info.txt",
    header=None,
    delimiter=r"\s+",
    names=["stns", "lat", "lon", "elev"],
)
avail_stn_raw = stncat["stns"].values
avail_stn_lat = stncat["lat"].values
avail_stn_lon = stncat["lon"].values
avail_stn = []

# find and obtain the selected stations info from the catalog
for stn in avail_stn_raw:
    avail_stn.append(stn[0:4])
avail_stn = np.array(avail_stn)

no_rec_stn = []
selstns_new = [stn.split("_")[0] for stn in dUU.columns.values]
with open(results_location + "stn_loc.txt", "w") as stnloc:
    for i, stn in enumerate(selstns_new):
        if stn in avail_stn:
            stn_lon = avail_stn_lon[np.where(avail_stn == stn)[0][0]]
            stn_lat = avail_stn_lat[np.where(avail_stn == stn)[0][0]]

            ## Select stations within 50 km from the EQ
            ## CAUTION: Earth considered FLAT
            distance_frm_eq = (
                np.sqrt((mlon - stn_lon) ** 2 + (mlat - stn_lat) ** 2) * 111.1
            )
            if distance_frm_eq < distEQ:
                stnloc.write(
                    "{} {:.5f} {:.5f}\n".format(
                        stn,
                        stn_lon,
                        stn_lat,
                    )
                )

        else:
            no_rec_stn.append(stn)


noRecU = [stn + "_U" for stn in no_rec_stn]
noRecN = [stn + "_N" for stn in no_rec_stn]
noRecE = [stn + "_E" for stn in no_rec_stn]

## Remove the stations with no location information
dUU = dUU.drop(noRecU, axis=1)
dNN = dNN.drop(noRecN, axis=1)
dEE = dEE.drop(noRecE, axis=1)

# Save the data in pickle format for easy read
dUU.to_pickle(results_location + "dU_data.pickle")
dNN.to_pickle(results_location + "dN_data.pickle")
dEE.to_pickle(results_location + "dE_data.pickle")
summaryfile.write(f"pickle files, {results_location}d[U,N,E]_data.pickle saved")


year = []
for dd in dUU.index:
    year.append(round(tyf(dd), 5))
dUU["year"] = year
dNN["year"] = year
dEE["year"] = year


## Save into mat file
import scipy.io as sio

sio.savemat(
    results_location + "dU_data.mat", {name: col.values for name, col in dUU.items()}
)
sio.savemat(
    results_location + "dN_data.mat", {name: col.values for name, col in dNN.items()}
)
sio.savemat(
    results_location + "dE_data.mat", {name: col.values for name, col in dEE.items()}
)
summaryfile.write(f"mat files, {results_location}d[U,N,E]_data.mat saved")
