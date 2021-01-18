import docker
from fastapi import FastAPI, HTTPException
from models import Function
from config import Settings
from schemas import InvocationParams, InvocationResult


app = FastAPI()
settings = Settings()


@app.post("/invoke/{id}", response_model=InvocationResult)
def run_function(id: str, params: InvocationParams) -> InvocationResult:
    client = docker.DockerClient(base_url=f"tcp://{settings.docker_host}:2375")
    func = Function.get_or_none(id=id)
    if not func:
        raise HTTPException(404, "Function not found")
    image_tag = f"{settings.docker_registry}/{id}"
    try:
        container = client.containers.get(image_tag)
    except docker.errors.NotFound:
        container = client.containers.run(image_tag, name=id, detach=True, tty=True)
    exitcode, output = container.exec_run(["python3", "run.py", func.handler])
    return InvocationResult(exitcode=exitcode, output=output.decode("UTF-8"))
