import pygmt
import numpy as np
import glob, os
import pandas as pd
import matplotlib
import warnings, matplotlib.cbook
import matplotlib.pyplot as plt
import logging

warnings.filterwarnings("ignore", category=FutureWarning)
DEG2KM = 111.2
from analysis_support import write_summary


################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/"
dest = results_location + "SelectedData/"

summaryfile = write_summary(
    scriptname=__file__, filename=results_location + "summary.txt", mode="a"
)
################################################
mlat, mlon = 22.9387, 120.5928
all_stations_df = pd.read_csv(
    results_location + "stn_loc.txt",
    sep="\s+",
    names=["stn", "Longitude", "Latitude"],
)

minlon = all_stations_df["Longitude"].min() - 1
minlat = all_stations_df["Latitude"].min() - 1
maxlon = all_stations_df["Longitude"].max() + 1
maxlat = all_stations_df["Latitude"].max() + 1


colormap = "geo"
markersize = 20
frame1 = "a0.5f0.25"
markertype = "triangle"

if markertype == "triangle":
    mrktype = "i"
elif markertype == "circle":
    mrktype = "c"

topo_data = "@earth_relief_15s"
res = "f"
frame = [frame1, "WSen"]


fig = pygmt.Figure()
fig.basemap(region=[minlon, maxlon, minlat, maxlat], projection="M8i", frame=frame)

# plot high res topography
try:
    fig.grdimage(
        grid=topo_data,
        shading=True,
        cmap=colormap,
    )
except:
    fig.grdimage(
        grid="@earth_relief_10m",
        shading=True,
        cmap=colormap,
    )

fig.coast(
    frame=frame,
    resolution=res,
    shorelines=["1/0.2p,black", "2/0.05p,gray"],
    borders=1,
)


fig.plot(
    x=all_stations_df["Longitude"].values,
    y=all_stations_df["Latitude"].values,
    style=f"{mrktype}{markersize}p",
    color="blue",
    pen="black",
)
fig.plot(
    x=mlon,
    y=mlat,
    style=f"a30p",
    color="red",
    pen="black",
)


# fig.legend(position="JBR+jBR+o0.1c+l1.5c", box="+gwhite+p1p")
fig.savefig("topo_plot.png", crop=True, dpi=300)
