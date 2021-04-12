import pandas as pd
import numpy as np
from scipy.optimize import least_squares as ls
from numpy import linalg as LA
import matplotlib.pyplot as plt
from analysis_support import dec2dt, dec2dt2, write_summary, toYearFraction as tyf
import matplotlib
import scipy.io as sio

################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/"
eof_results_location = root_location + "Results/EOFresults/"
dest = results_location + "SelectedData/"


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


# Read the mat file
matfiles = [
    "pc1_U.mat",
    "pc1_N.mat",
    "pc1_E.mat",
]
pcdata_dict = {}
for mat in matfiles:
    pcdata = sio.loadmat(eof_results_location + mat)
    pc = np.array(pcdata["pcdata"])
    comp = mat.split("_")[1].split(".")[0]
    pcdata_dict[f"pc_{comp}"] = pc

data_Ndict = {}
data_Edict = {}
data_Udict = {}
for i, stn in enumerate(dUU.columns.values):

    data_Ndict[stn] = dNN.iloc[:, i].values.reshape(-1, 1) - pcdata_dict["pc_N"]
    data_Ndict[stn] = [val[0] for val in data_Ndict[stn]]
    data_Edict[stn] = dEE.iloc[:, i].values.reshape(-1, 1) - pcdata_dict["pc_E"]
    data_Edict[stn] = [val[0] for val in data_Edict[stn]]
    data_Udict[stn] = dUU.iloc[:, i].values.reshape(-1, 1) - pcdata_dict["pc_U"]
    data_Udict[stn] = [val[0] for val in data_Udict[stn]]


dfN_final = pd.DataFrame.from_dict(data_Ndict)
dfE_final = pd.DataFrame.from_dict(data_Edict)
dfU_final = pd.DataFrame.from_dict(data_Udict)


dfN_final.to_csv(eof_results_location + "final_N.txt", index=False)
dfE_final.to_csv(eof_results_location + "final_E.txt", index=False)
dfU_final.to_csv(eof_results_location + "final_U.txt", index=False)
