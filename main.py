"""
main
----
The entry-point to the group matching API.

TODO:
- Generalize to multiple possible data sources
- Actual authentication

"""

import os

from flask import jsonify

from data.group import output_dict_from_results
from data.student import student_data_from_csv
from data.room import room_data_from_csv
from optimization.match import place_students


def create_groups(request):
    """
    Creates a set of weekly meeting groups, given student sign-up data.

    Loads CSV data into numpy arrays, runs a Pyomo mixed-integer program, and
    formats the output into a JSON-like response.

    """
    # Import data
    responses_csv_file = request.files.get("responses_csv_file")
    rooms_csv_file = request.files.get("rooms_csv_file")

    if responses_csv_file is None:
        raise ValueError("Missing responses csv file!")
    if rooms_csv_file is None:
        raise ValueError("Missing rooms csv file!")
    # temporary gate for development purposes only
    if request.form.get("user") != "michigan_spring_2019_dev":
        return jsonify()

    sdf, A, X = student_data_from_csv(responses_csv_file)
    rdf, R = room_data_from_csv(rooms_csv_file)

    # Optimize
    group_dict = place_students(A, X, R)

    # Format output
    output_dict = output_dict_from_results(group_dict, sdf, rdf)

    return jsonify(output_dict)


def health_check(request):
    return jsonify({"success": True})
