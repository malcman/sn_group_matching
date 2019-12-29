import os

from flask import jsonify


def health_check(request):
    return jsonify({"success": True})


def create_groups(request):
    return jsonify({"response": "hello world"})
