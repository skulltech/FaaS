import docker
from flask import Flask, request, jsonify
from models import Function

app = Flask(__name__)
app.config["DOCKER_SERVER"] = "hal9011"


@app.route("/invoke/<id>", methods=["GET"])
def run_function(id):
    client = docker.DockerClient(base_url=f"tcp://{app.config['DOCKER_SERVER']}:2375")
    function = Function.get_or_none(id=id)
    if not function:
        return jsonify({"status": "error", "message": "function not found"}, 404)
    try:
        container = client.containers.get(id)
    except docker.errors.NotFound:
        container = client.containers.run(id, name=id, detach=True, tty=True)
    exitcode, output = container.exec_run(["python3", "run.py", function.handler])
    return jsonify(
        {
            "status": "success",
            "invocation": {"exitcode": exitcode, "output": output.decode("UTF-8")},
        }
    )
