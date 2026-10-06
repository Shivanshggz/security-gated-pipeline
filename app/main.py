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
        version="1.0.0"
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)