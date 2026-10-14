from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint used by deployment verification."""
    return jsonify(status="ok"), 200


@app.route("/")
def index():
    """Root endpoint identifying the service."""
    return jsonify(
        service="security-gated-pipeline",
        version="1.1.0"     # ← changed from 1.0.0
    ), 200