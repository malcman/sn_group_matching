"""
data.student
------------
Loads the survey data from the signed up students and prepares it for the
optimization program.

TODO: Move to Google Sheets integration in favor of Qualtrics / CSV uploads.

"""

import logging
import re

import numpy as np
import pandas as pd


LOG = logging.getLogger(__name__)

COLUMN_MAP = {
    "Q1": "first",
    "Q2": "last",
    "Q3": "email",
    "Q9": "gender",
    "Q7": "grad_standing",
    "Q16": "campus",
    "Q15_1": "t_mon",
    "Q15_2": "t_tue",
    "Q15_3": "t_wed",
    "Q15_4": "t_thu",
}

VALUE_MAP = {"gender": {"Man": "M", "Woman": "F",}}

TIME_COLUMNS = ["t_mon", "t_tue", "t_wed", "t_thu"]
TIMESLOTS = [
    "4-5 pm",
    "5-6 pm",
    "6-7 pm",
    "7-8 pm",
    "8-9 pm",
]


def _split_times(row):
    """
    Row-wise helper function to One-Hot encode the timeslots, from comma-separated
    lists per day.

    """
    ix = 0
    for t_col in TIME_COLUMNS:
        if row[t_col] is np.nan:
            for t in TIMESLOTS:
                row[f"t_{ix}"] = 0
                ix += 1
        else:
            given_slots = set(map(str.strip, row[t_col].split(",")))
            for t in TIMESLOTS:
                row[f"t_{ix}"] = 1 if t in given_slots else 0
                ix += 1
    return row


def student_data_from_csv(csv_file):
    """
    Loads, validates, cleans, and transforms the room data to prepare it for the
    optimization program.

    Also logs informational summary messages about the characteristics of the
    participant pool.

    """
    raw_df = pd.read_csv(csv_file)
    if not set(COLUMN_MAP.keys()).issubset(set(raw_df.columns)):
        raise ValueError("Provided column mapping for survey data csv did not match")

    # Drop qualtrics columns, NOTE: temporary
    df = raw_df.drop([0, 1], axis=0)

    # Rename cols
    df = df[COLUMN_MAP.keys()].rename(columns=COLUMN_MAP)
    df = df.replace(VALUE_MAP)

    # Drop nulls
    num_nulls = df.isna().all(axis=1).sum()
    if num_nulls > 0:
        LOG.debug(f"Ignoring {num_nulls} null rows")
    df = df.dropna(axis=0, how="all")

    # Drop duplicates, use email as unique identifier
    df["email"] = df["email"].str.lower()
    num_duplicates = df["email"].duplicated().sum()
    if num_duplicates > 0:
        LOG.debug(f"Found {num_duplicates} duplicates, using last occurrences")

    df = df[~df["email"].duplicated(keep="last")]

    # Create student IDs from the cleaned dataframe.
    df = df.reset_index().drop("index", axis=1)
    df = df.reset_index().rename(columns={"index": "s_id"})

    # Bucket gender
    df["gender"] = df["gender"].apply(lambda x: x if x in {"M", "F"} else "O")

    # Use central as default campus, NOTE: temporary
    df["campus"] = df["campus"].fillna(value="Central Campus")

    # Encode time slots
    df = df.apply(_split_times, axis=1)
    # hack in the half-hour slots, NOTE: temporary
    df["t_20"] = ((df["t_0"] == 1) & (df["t_1"] == 1)).astype(int)  # M 4:30
    df["t_21"] = ((df["t_3"] == 1) & (df["t_4"] == 1)).astype(int)  # M 7:30

    # Summarize dataframe
    LOG.debug(f"\n\nGender breakdown:\n{str(df.gender.value_counts())}\n")
    LOG.debug(f"\n\nGraduation standings:\n{str(df.grad_standing.value_counts())}\n")
    LOG.debug(f"\n\nCampus breakdown:\n{str(df.campus.value_counts())}\n")

    # Extract data to return along with dataframe
    At = df[[f"t_{ix}" for ix in range(22)]].to_numpy()

    campus_ohe_df = pd.get_dummies(df.campus)
    campus_ohe_df.loc[df[df.campus.str.contains(",")].index, :2] = 1
    campus_ohe_df = campus_ohe_df[campus_ohe_df.columns[:2]]
    Al = campus_ohe_df.to_numpy()

    Ag = pd.get_dummies(df.grad_standing).to_numpy()

    Xg = pd.get_dummies(df.gender, dummy_na=True).to_numpy()

    return df, (At, Al, Ag), (Xg)
