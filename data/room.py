"""
data.room
---------
Loads the data on the available rooms and prepares it for the optimization
program.

Because the group leaders need to be approved, matched, and scheduled prior to
participant placement, these groups are set.

"""

import logging

import pandas as pd


LOG = logging.getLogger(__name__)

COLUMN_MAP = {
    "Group ID": "group_id",
    "Meeting Time": "time_id",
    "Campus": "campus",
    "Grad Standing": "grad_standing",
}

VALUE_MAP = {
    "time_id": {
        "Monday 4:00-5:00": 0,
        "Monday 5:00-6:00": 1,
        "Monday 6:00-7:00": 2,
        "Monday 7:00-8:00": 3,
        "Monday 8:00-9:00": 4,
        "Tuesday 4:00-5:00": 5,
        "Tuesday 5:00-6:00": 6,
        "Tuesday 6:00-7:00": 7,
        "Tuesday 7:00-8:00": 8,
        "Tuesday 8:00-9:00": 9,
        "Wednesday 4:00-5:00": 10,
        "Wednesday 5:00-6:00": 11,
        "Wednesday 6:00-7:00": 12,
        "Wednesday 7:00-8:00": 13,
        "Wednesday 8:00-9:00": 14,
        "Thursday 4:00-5:00": 15,
        "Thursday 5:00-6:00": 16,
        "Thursday 6:00-7:00": 17,
        "Thursday 7:00-8:00": 18,
        "Thursday 8:00-9:00": 19,
        # hack in the half-hour slots, NOTE: temporary
        "Monday 4:30-5:30": 20,
        "Monday 7:30-8:30": 21,
    },
}


def room_data_from_csv(csv_file):
    """
    Loads, validates, cleans, and transforms the room data to prepare it for the
    optimization program.

    """
    raw_df = pd.read_csv(csv_file)
    if not set(COLUMN_MAP.keys()).issubset(set(raw_df.columns)):
        raise ValueError("Provided column mapping for rooms csv did not match")

    LOG.debug(f"Found {raw_df.shape[0]} rooms from the room csv")

    df = raw_df[COLUMN_MAP.keys()].rename(columns=COLUMN_MAP)
    df = df.replace(VALUE_MAP)

    # For each filtering variable, encode categorical values as indices.
    indexed_value_map = {
        "campus": {x: ix for ix, x in enumerate(sorted(df.campus.unique()))},
        "grad_standing": {
            x: ix for ix, x in enumerate(sorted(df.grad_standing.unique()))
        },
    }
    df = df.replace(indexed_value_map)

    R_id, Rt, Rl, Rg = df.to_numpy().T
    return df, (Rt, Rl, Rg)
