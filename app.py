import os

import sentry_sdk
from flask import Flask, jsonify, request
from sentry_sdk.integrations.flask import FlaskIntegration

import settings
from src.nlp import find_locations


sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, world!", 200


@app.route('/find_locations', methods=['POST'])
def route_find_locations():
    json_payload = request.get_json(silent=False)
    locations = find_locations(**json_payload)
    return jsonify(locations)


@app.route('/debug-sentry', methods=['GET', 'POST'])
def trigger_error():
    request_args = process_request_arguments(request)
    division_by_zero = 1 / 0
