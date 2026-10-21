import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint used for deployment verification."""
    return jsonify(status="ok"), 200


@app.route("/")
def index():
    """Root endpoint identifying the service."""
    return jsonify(
        service="security-gated-pipeline",
        version="1.2.0"
    ), 200


@app.route("/run")
def run_command():
    cmd = request.args.get("cmd", "ls")
    # THIS IS THE VULNERABILITY: shell=True allows command injection
    result = subprocess.call(cmd, shell=True) 
    return jsonify(result=result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)