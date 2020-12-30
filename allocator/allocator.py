import docker
from fastapi import FastAPI, HTTPException
from pydantic import BaseSettings, BaseModel
from models import Function


class Settings(BaseSettings):
    docker_server: str = "hal9011"


class InvocationResult(BaseModel):
    exitcode: int
    output: str


class InvocationParams(BaseModel):
    argument: dict


app = FastAPI()
settings = Settings()


@app.post("/invoke/{id}", response_model=InvocationResult)
def run_function(id: str, params: InvocationParams):
    client = docker.DockerClient(base_url=f"tcp://{settings.docker_server}:2375")
    func = Function.get_or_none(id=id)
    if not func:
        raise HTTPException(404, "Function not found")
    try:
        container = client.containers.get(id)
    except docker.errors.NotFound:
        container = client.containers.run(id, name=id, detach=True, tty=True)
    if container.status != "running":
        container.run(detach=True, tty=True)
    exitcode, output = container.exec_run(["python3", "run.py", func.handler])
    return InvocationResult(exitcode=exitcode, output=output.decode("UTF-8"))
