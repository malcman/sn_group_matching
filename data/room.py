import pandas as pd


COLUMN_MAP = {
    "Group ID": "g_id",
    "Meeting Time": "t_id",
    "Campus": "campus",
    "Grad Standing": "grad_standing",
}

VALUE_MAP = {
    "grad_standing": {"Undergrad": "undergrad", "Grad": "grad"},
    "campus": {
        "Central Campus": "central",
        "North Campus": "north",
        "North Campus, Central Campus": "both",
    },
    "t_id": {
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
    },
}


def room_data_from_csv(csv_file):
    raw_df = pd.read_csv(csv_file)
    if not set(COLUMN_MAP.keys()).issubset(set(raw_df.columns)):
        raise ValueError("Provided column mapping for rooms csv did not match")

    df = raw_df[COLUMN_MAP.keys()].rename(columns=COLUMN_MAP)
    df = df.replace(VALUE_MAP)

    return df
