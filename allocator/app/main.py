import docker
from fastapi import FastAPI, HTTPException
from models import Function, Container
from config import Settings
from schemas import InvocationParams, InvocationResult
import datetime


app = FastAPI()
settings = Settings()


@app.post("/invoke/{id}", response_model=InvocationResult)
def run_function(id: str, params: InvocationParams) -> InvocationResult:
    client = docker.DockerClient(base_url=f"tcp://{settings.docker_host}:2375")
    func = Function.get_or_none(id=id)
    if not func:
        raise HTTPException(404, "Function not found")
    image_tag = f"{settings.docker_registry}/{id}"
    container = None
    for cont in func.containers:
        if not cont.is_active:
            container = client.containers.get(cont.id)
    if not container:
        container = client.containers.run(image_tag, detach=True, tty=True)
        cont = Container.create(id=container.id, function=func)
    exitcode, output = container.exec_run(["python3", "run.py", func.handler])
    cont.stopped_at = datetime.datetime.now()
    cont.is_active = False
    cont.save()
    return InvocationResult(exitcode=exitcode, output=output.decode("UTF-8"))
