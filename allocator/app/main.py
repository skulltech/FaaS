import docker
from fastapi import FastAPI, HTTPException
from models import Function, Container
from config import Settings
from schemas import InvocationParams, InvocationResult
import datetime
import logging
from fastapi_utils.tasks import repeat_every


app = FastAPI()
settings = Settings()
logger = logging.getLogger(__name__)


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
            cont.is_active = True
            cont.save()
    if not container:
        container = client.containers.run(image_tag, detach=True, tty=True)
        cont = Container.create(id=container.id, function=func)
    exitcode, output = container.exec_run(["python3", "run.py", func.handler])
    cont.stopped_at = datetime.datetime.now()
    cont.is_active = False
    cont.save()
    return InvocationResult(exitcode=exitcode, output=output.decode("UTF-8"))


@app.on_event("startup")
@repeat_every(seconds=settings.purge_every, logger=logger, wait_first=True)
def purge_containers():
    client = docker.DockerClient(base_url=f"tcp://{settings.docker_host}:2375")
    for cont in Container.select():
        stopped_at = cont.stopped_at or datetime.datetime.max
        if (
            stopped_at + datetime.timedelta(seconds=settings.warm_duration)
            < datetime.datetime.now()
        ):
            container = client.containers.get(cont.id)
            container.remove(v=True, force=True)
            cont.delete_instance()
