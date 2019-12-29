import os

from flask import jsonify

from data.group import output_from_results
from data.student import student_data_from_csv
from data.room import room_data_from_csv
from optimization.match import place_students


def create_groups(request):
    # Import the data
    responses_csv_file = request.files.get("responses_csv_file")
    rooms_csv_file = request.files.get("rooms_csv_file")

    if responses_csv_file is None:
        raise ValueError("Missing responses csv file!")
    if rooms_csv_file is None:
        raise ValueError("Missing rooms csv file!")
    # temporary gate for development purposes only
    if request.form.get("user") != "michigan_spring_2019_dev":
        return jsonify()

    student_data = student_data_from_csv(responses_csv_file)
    room_data = room_data_from_csv(rooms_csv_file)

    # Optimize
    results = place_students(student_data, room_data)

    # Format output
    output = output_from_results(results)

    return jsonify({"results": output})


def health_check(request):
    return jsonify({"success": True})
