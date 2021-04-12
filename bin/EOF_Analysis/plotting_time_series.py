import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import matplotlib
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
from analysis_support import dec2dt, dec2dt2, write_summary, toYearFraction as tyf

font = {"weight": "bold", "size": 22}

matplotlib.rc("font", **font)

plt.style.use("ggplot")


################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/EOFresults/"
dest = results_location + "SelectedData/"

################################################


df_ve = pd.read_csv(
    results_location + "EOF_modes_VE.txt",
    sep="\s+",
    header=None,
    names=["mode", "comp", "VE"],
)

# Read the mat file
matfiles = [
    "pc1_U.mat",
    "pc1_N.mat",
    "pc1_E.mat",
    "pc2_U.mat",
    "pc2_N.mat",
    "pc2_E.mat",
]
for mat in matfiles:
    pcdata = sio.loadmat(results_location + mat)

    pc_tdata = np.transpose(np.array(pcdata["tdata"]))

    pc = np.array(pcdata["pcdata"])
    pctime = []
    for i in range(len(pc_tdata)):
        pctime.append(dec2dt(pc_tdata[i]))

    pctime = np.array(pctime)
    comp = mat.split(".")[0].split("_")[1]
    mode = mat[2]
    if int(mode) == 1:
        plt.figure(figsize=(10, 6))
        ve = df_ve[(df_ve["mode"] == int(mode)) & (df_ve["comp"] == comp)]["VE"].values[
            0
        ]
        plt.plot(pctime, pc, "k", lw=1, label=f"Variance Explained: {ve}%")
        # plt.plot(np.NaN,np.NaN,'*',label=f'Variance Explained: {ve}%')
        leg = plt.legend(
            fontsize=18, loc=1, handlelength=0, handletextpad=0, fancybox=True
        )
        for item in leg.legendHandles:
            item.set_visible(False)
        # plt.legend(fontsize=18,loc=1)
        plt.ylabel("{}, in mm".format(comp), fontsize=30)
        # plt.ylim([-3, 3])
        plt.savefig(
            results_location + "eof{}_CGPS_comp_temp{}.png".format(mode, comp),
            dpi=150,
            bbox_inches="tight",
        )
    elif int(mode) == 2:
        plt.figure(figsize=(10, 6))
        ve = df_ve[(df_ve["mode"] == int(mode)) & (df_ve["comp"] == comp)]["VE"].values[
            0
        ]
        plt.plot(pctime, pc, "k", lw=1, label=f"Variance Explained: {ve}%")
        leg = plt.legend(
            fontsize=18, loc=1, handlelength=0, handletextpad=0, fancybox=True
        )
        for item in leg.legendHandles:
            item.set_visible(False)
        plt.ylabel("{}, in mm".format(comp), fontsize=30)
        # plt.ylim([-1, 1])
        plt.savefig(
            results_location + "eof{}_CGPS_comp_temp{}.png".format(mode, comp),
            dpi=150,
            bbox_inches="tight",
        )
