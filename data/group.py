"""
data.group
----------
Transforms and formats the optimization output into a convenient, human-readable
format compatible with the caller.

"""

from .room import VALUE_MAP as ROOM_VALUE_MAP

VALUE_MAP = {
    "campus": {0: "Central", 1: "North",},
    "grad_standing": {0: "Graduate", 1: "Undergraduate",},
}

GROUP_OUTPUT_COLUMNS = [
    "group_id",
    "time",
    "campus",
    "grad_standing",
    "is_meeting",
]

STUDENT_OUTPUT_COLUMNS = [
    "first",
    "last",
    "email",
    "gender",
    "campus",
    "grad_standing",
    "t_mon",
    "t_tue",
    "t_wed",
    "t_thu",
    "group_id",
]


def output_dict_from_results(group_dict, sdf, rdf):
    """
    Given the optimization output and the loaded DataFrames, returns JSON-like
    records of the placed and unplaced students, along with the groups.

    We expect group_dict to be of the form:
    [
        {
            group_index: [ student_index_1, ... ],
        },
        ...
    ]

    """
    group_indices = group_dict.keys()

    group_index_id_map = rdf["group_id"].to_dict()

    # Rooms
    rdf["is_meeting"] = rdf.index.isin(group_indices)
    rdf = rdf.replace(VALUE_MAP)
    # human-readable time slots
    room_text_map = dict(map(reversed, ROOM_VALUE_MAP["time_id"].items()))
    rdf["time"] = rdf["time_id"].replace(room_text_map)

    groups = rdf[GROUP_OUTPUT_COLUMNS]

    # Students
    sdf["group_id"] = -1
    for group_index, student_indices in group_dict.items():
        group_id = group_index_id_map[group_index]
        sdf.loc[student_indices, "group_id"] = group_id

    placed = sdf[sdf.group_id >= 0][STUDENT_OUTPUT_COLUMNS]
    unplaced = sdf[sdf.group_id < 0][STUDENT_OUTPUT_COLUMNS[:-1]]  # no group id

    # Return JSON-like results
    return {
        "placed": placed.to_dict(orient="records"),
        "unplaced": unplaced.to_dict(orient="records"),
        "groups": groups.to_dict(orient="records"),
    }
