import numpy as np
import matplotlib.pyplot as plt
from least_squares_modules import events, x0, fun, gen_data, all_jumps


################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/" + "LSQfigs/"
dest = results_location + "SelectedData/"


################################################

## VISUALIZATION
def plot_ls_results(
    stn,
    xval,
    yval1,
    res_lsq,
    yvalN,
    res_lsqN,
    yvalE,
    res_lsqE,
    trendU,
    trendN,
    trendE,
    seasonalityU,
    seasonalityN,
    seasonalityE,
    jumpsU,
    jumpsN,
    jumpsE,
):
    fontsize = 16
    fontsizeTitle = 16

    fig, ax = plt.subplots(4, 1, figsize=(15, 8), sharex=True)
    ax[0].plot(xval, yval1, "bo", label="data", markersize=1)
    ax[0].plot(xval, gen_data(xval, *res_lsq.x), "k", lw=1, label="Least squares fit")
    ax[0].set_title(stn + "-U", fontsize=fontsizeTitle)
    # ax[0].set_ylim([-150, 140])
    ax[0].legend(fontsize=fontsize)
    plt.setp(ax[0].get_yticklabels(), fontsize=16)

    # Vertical Trend
    ax[1].plot(
        xval, trendU, "k", label=" Linear Trend: {:.1f}".format(res_lsq.x[1]), lw=1
    )
    ax[1].legend(fontsize=fontsize)
    # ax[1].set_ylim([-50, 140])
    plt.setp(ax[1].get_yticklabels(), fontsize=16)

    ## Seasonality Vertical
    ax[2].plot(xval, seasonalityU, "k", label="Seasonal and tidal part", lw=1)
    # ax[2].set_ylim([-3, 3])
    # ax[2].set_ylabel("Amp (in mm)", color="k", fontsize=22)

    ax[2].legend(fontsize=fontsize)
    plt.setp(ax[2].get_yticklabels(), fontsize=16)

    ## Jumps Vertical
    ax[3].plot(xval, jumpsU, "k", label="Co Seismic Jumps", lw=1)
    ax[3].legend(fontsize=fontsize)
    plt.setp(ax[3].get_yticklabels(), fontsize=16)
    # plt.xticks(np.arange(min(xval), max(xval) + 1, 1.0), fontsize=16)
    # for event, cc in zip(
    #     [
    #         2016.098,
    #     ],
    #     ["green", "red"],
    # ):
    # ax[0].axvline(x=event, color=cc, ls="--", lw=1)
    # ax[3].axvline(x=event, color=cc, ls="--", lw=1)

    plt.subplots_adjust(hspace=0.05, wspace=0)
    plt.savefig(
        results_location + "model_fitting_U_{}.png".format(stn),
        bbox_inches="tight",
        dpi=300,
    )
    plt.close("all")

    ### N
    fig, ax = plt.subplots(4, 1, figsize=(15, 8), sharex=True)

    # N
    ax[0].plot(xval, yvalN, "bo", label="data", markersize=1)
    ax[0].plot(xval, gen_data(xval, *res_lsqN.x), "k", lw=1, label="Least squares fit")
    ax[0].set_title(stn + "-N", fontsize=fontsizeTitle)
    # ax[0].set_ylim([-150, 140])
    ax[0].legend(fontsize=fontsize)
    plt.setp(ax[0].get_yticklabels(), fontsize=16)

    # North
    ax[1].plot(
        xval, trendN, "k", label=" Linear Trend: {:.1f}".format(res_lsqN.x[1]), lw=1
    )
    ax[1].legend(fontsize=fontsize)
    # ax[1].set_ylim([-50, 140])
    plt.setp(ax[1].get_yticklabels(), fontsize=16)

    # North
    ax[2].plot(xval, seasonalityN, "k", label="Seasonal and tidal part", lw=1)
    # ax[2].set_ylim([-3, 3])
    ax[2].legend(fontsize=fontsize)
    plt.setp(ax[2].get_yticklabels(), fontsize=16)
    # ax[2].set_ylabel("Amp (in mm)", color="k", fontsize=22)

    ## Jumps North
    ax[3].plot(xval, jumpsN, "k", label="Co Seismic Jumps", lw=1)
    ax[3].legend(fontsize=fontsize)
    # plt.xticks(np.arange(min(xval), max(xval) + 1, 1.0), fontsize=16)
    plt.setp(ax[3].get_yticklabels(), fontsize=16)
    # for event, cc in zip(
    #     [
    #         2016.098,
    #     ],
    #     ["green", "red"],
    # ):
    # ax[0].axvline(x=event, color=cc, ls="--", lw=1)
    # ax[3].axvline(x=event, color=cc, ls="--", lw=1)

    plt.subplots_adjust(hspace=0.05, wspace=0)
    plt.savefig(
        results_location + "model_fitting_N_{}.png".format(stn),
        bbox_inches="tight",
        dpi=300,
    )
    plt.close("all")

    ### E
    fig, ax = plt.subplots(4, 1, figsize=(15, 8), sharex=True)

    # E
    ax[0].plot(xval, yvalE, "bo", label="data", markersize=1)
    ax[0].plot(xval, gen_data(xval, *res_lsqE.x), "k", lw=1, label="Least squares fit")
    ax[0].set_title(stn + "-E", fontsize=fontsizeTitle)
    # ax[0].set_ylim([-150, 140])
    ax[0].legend(fontsize=fontsize)
    plt.setp(ax[0].get_yticklabels(), fontsize=16)

    # East
    ax[1].plot(
        xval, trendE, "k", label=" Linear Trend: {:.1f}".format(res_lsqE.x[1]), lw=1
    )
    ax[1].legend(fontsize=fontsize)
    # ax[1].set_ylim([-50, 140])
    plt.setp(ax[1].get_yticklabels(), fontsize=16)

    # East
    ax[2].plot(xval, seasonalityE, "k", label="Seasonal and tidal part", lw=1)
    # ax[2].set_ylim([-3, 3])

    # ax[2].set_ylabel("Amp (in mm)", color="k", fontsize=22)

    ax[2].legend(fontsize=fontsize)
    plt.setp(ax[2].get_yticklabels(), fontsize=16)

    ## Jumps East
    ax[3].plot(xval, jumpsE, "k", label="Co Seismic Jumps", lw=1)
    ax[3].legend(fontsize=fontsize)
    plt.setp(ax[3].get_yticklabels(), fontsize=16)
    # for event in [
    #     2016.098,
    #     2010.31507,
    #     2010.16986,
    #     2010.10137,
    # ]:
    #     ax[3].axvline(x=event)
    # for event, cc in zip(
    #     [
    #         2016.098,
    #     ],
    #     ["green", "red"],
    # ):
    #     ax[0].axvline(x=event, color=cc, ls="--", lw=1)
    #     ax[3].axvline(x=event, color=cc, ls="--", lw=1)

    plt.subplots_adjust(hspace=0.05, wspace=0)
    plt.savefig(
        results_location + "model_fitting_E_{}.png".format(stn),
        bbox_inches="tight",
        dpi=300,
    )
    plt.close("all")