# import libraries
import pandas as pd
import numpy as np
from scipy.optimize import least_squares as ls
from numpy import linalg as LA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from analysis_support import dec2dt, write_summary, toYearFraction as tyf
import matplotlib

################################################
## Set parameters

root_location = "../../"
results_location = root_location + "Results/"
dest = results_location + "SelectedData/"

summaryfile = write_summary(
    scriptname=__file__, filename=results_location + "summary.txt", mode="a"
)
################################################


def lsq_int(
    data_pickle=results_location + "dU_data.pickle",
    event_file=root_location + "eventsMg5frCloseMeinong.txt",
    selected_events_file=results_location + "SigEarthquakes.txt",
):
    # load pickle data
    dUU = pd.read_pickle(data_pickle)

    # convert time to decimal year
    year = []
    for dd in dUU.index:
        year.append(round(tyf(dd), 5))

    all_events_selectedRange = pd.read_csv(
        event_file,
        delimiter="|",
        header=None,
        skiprows=1,
        names=[
            "#EventID",
            "Time",
            "Latitude",
            "Longitude",
            "Depth/km",
            "Author",
            "Catalog",
            "Contributor",
            "ContributorID",
            "MagType",
            "Magnitude",
            "MagAuthor",
            "EventLocationName",
        ],
    )
    all_events_selectedRange = all_events_selectedRange[
        all_events_selectedRange["Magnitude"] >= 5.2
    ]
    tmp = [event.split("T")[0] for event in all_events_selectedRange["Time"]]
    all_events_selectedRange.to_csv(selected_events_file, index=False)
    evs = pd.DatetimeIndex(tmp)  # string to pandas datetimeIndex
    ## converting the events to year fraction
    events_old = []
    for ee in evs:
        events_old.append(round(tyf(ee), 5))

    events = []
    # print(events)
    for yr in events_old:
        if (yr >= np.min(year)) and (yr <= np.max(year)):
            events.append(yr)

    # # defining the intial values
    initVals = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    initValsEnd = [0 for jj in range(len(events))]
    x0 = np.array(initVals + initValsEnd)
    return events, x0


if __name__ == "__main__":
    lsq_int()