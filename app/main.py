import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/")
def index():
    return jsonify(
        service="security-gated-pipeline",
        version="1.0.0"
    ), 200


@app.route("/run")
def run_command():
    cmd = request.args.get("cmd", "ls")
    result = subprocess.call(cmd, shell=True)  # intentional vulnerability
    return jsonify(result=result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)