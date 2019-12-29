import os

from flask import Flask, request
import yaml

from main import health_check, create_groups


PATH_TO_ENV_FILE = ".env.yaml"


def load_env_variables(env_file_path):
    env = None
    with open(env_file_path) as f:
        env = yaml.safe_load(f)
    if env is None:
        raise EnvironmentError(
            f"Unable to find environment variable file at {env_file_path}"
        )

    os.environ["FLASK_ENV"] = env["FLASK_ENV"]
    os.environ["HOST"] = env["HOST"]
    os.environ["PORT"] = env["PORT"]
    os.environ["APP_SECRET_KEY"] = env["APP_SECRET_KEY"]

    return


# Define application and routes

app = Flask(__name__)


@app.route("/health-check")
def health_check_route():
    return health_check(request)


@app.route("/create-groups", methods=["POST"])
def create_groups_route():
    return create_groups(request)


if __name__ == "__main__":
    load_env_variables(PATH_TO_ENV_FILE)
    app.run(
        host=os.environ["HOST"],
        port=os.environ["PORT"],
        # options forwarded to Werkzeug server
        threaded=True,
    )
