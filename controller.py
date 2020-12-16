from models import Function
from flask import Flask, request, jsonify, url_for, send_from_directory
import os
import uuid
from peewee import DoesNotExist
import docker
import subprocess

app = Flask(__name__)
app.config["PAYLOAD_FOLDER"] = "payloads"
app.config["DOCKER_REGISTRY"] = "hal9011"


def deploy(server, payload):
    client = docker.DockerClient(base_url=f"tcp://{server}:2375")
    image_tag = os.path.splitext(os.path.basename(payload))[0]
    print("deploying ", payload)
    image = client.images.build(
        path=".", buildargs={"payload": payload}, tag=image_tag, quiet=False
    )
    return image


@app.route("/payloads/<id>", methods=["GET"])
def get_payload(id):
    return send_from_directory(app.config["PAYLOAD_FOLDER"], id + ".zip")


@app.route("/functions", methods=["POST"])
def add_function():
    f = request.files.get("file")
    if not f:
        return jsonify({"status": "error", "message": "payload missing"}, 400)
    handler = request.form.get("handler")
    if not handler:
        return jsonify({"status": "error", "message": "handler unspecified"}, 400)
    id = str(uuid.uuid4())
    filename = id + ".zip"
    filepath = os.path.join(app.config["PAYLOAD_FOLDER"], filename)
    f.save(filepath)
    try:
        deploy(app.config["DOCKER_REGISTRY"], filepath)
    except (docker.errors.BuildError, docker.errors.APIError):
        os.remove(filepath)
        return jsonify({"status": "error", "message": "image build unsuccessful"}, 400)
    function = Function.create(id=id, handler=handler)
    return jsonify(
        {
            "status": "success",
            "function": {
                "id": function.id,
                "handler": function.handler,
                "payload": url_for("get_payload", id=id, _external=True),
            },
        },
        201,
    )


@app.route("/functions", methods=["GET"])
def list_functions():
    functions = Function.select()
    return jsonify(
        {
            "status": "success",
            "functions": [
                {
                    "id": function.id,
                    "handler": function.handler,
                    "payload": url_for("get_payload", id=id, _external=True),
                }
                for function in functions
            ],
        },
        200,
    )


@app.route("/functions/<id>", methods=["GET"])
def get_function(id):
    if id:
        function = Function.get_or_none(id=id)
        if not function:
            return jsonify(
                {"status": "error", "message": "function does not exist"}, 404
            )
    return jsonify(
        {
            "status": "success",
            "function": {
                "id": function.id,
                "handler": function.handler,
                "payload": url_for("get_payload", id=id, _external=True),
            },
        },
        200,
    )


@app.route("/functions/<id>", methods=["PUT"])
def update_function(id):
    if id:
        function = Function.get_or_none(id=id)
        if not function:
            return jsonify(
                {"status": "error", "message": "function does not exist"}, 404
            )
    handler = request.form.get("handler")
    if handler:
        function.handler = handler
    f = request.files.get("file")
    if f:
        f.save(os.path.join(app.config["PAYLOAD_FOLDER"], id, ".zip"))
    return jsonify(
        {
            "status": "success",
            "function": {
                "id": function.id,
                "handler": function.handler,
                "payload": url_for("get_payload", id=id, _external=True),
            },
        },
        201,
    )
