from flask import Flask, request, jsonify
from src.nlp import find_locations

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

your_sentry_dsn = 'https://0faaadd6ed104e2cbc28a4e05bd2f4ea@o304275.ingest.sentry.io/5380111'  # TODO fill this

sentry_sdk.init(
    dsn=your_sentry_dsn,
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

