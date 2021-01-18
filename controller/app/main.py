from models import Function
from fastapi import FastAPI, HTTPException
import uuid
from playhouse.shortcuts import model_to_dict
import docker
from schemas import FunctionIn, FunctionOut, FunctionOutList
from config import Settings

app = FastAPI()
settings = Settings()


def deploy(id, payload, docker_host, docker_registry):
    client = docker.DockerClient(base_url=f"tcp://{docker_host}:2375")
    image_tag = f"{docker_registry}/{id}"
    image = client.images.build(
        path=".",
        buildargs={"payload": payload},
        tag=image_tag,
        quiet=False,
    )
    client.images.push(image_tag)
    return image


@app.post("/functions", response_model=FunctionOut)
def create_function(function: FunctionIn):
    id = str(uuid.uuid4())
    try:
        deploy(id, function.payload, settings.docker_host, settings.docker_registry)
    except (docker.errors.BuildError, docker.errors.APIError):
        raise HTTPException(status_code=400, detail="Image build unsuccessful")
    func = Function.create(**function.dict(), id=id)
    return FunctionOut(**model_to_dict(func))


@app.get("/functions", response_model=FunctionOutList)
def list_functions():
    functions = Function.select()
    return FunctionOutList(
        functions=[FunctionOut(**model_to_dict(func)) for func in functions]
    )


@app.get("/functions/{id}", response_model=FunctionOut)
def get_function(id: str):
    func = Function.get_or_none(id=id)
    if not func:
        raise HTTPException(404, "Function not found")
    return FunctionOut(**model_to_dict(func))


@app.put("/functions/{id}", response_model=FunctionOut)
def update_function(id: str, function: FunctionIn):
    func = Function.get_or_none(id=id)
    if not func:
        raise HTTPException(404, "Function not found")
    func.update(**function.dict())
    return FunctionOut(**model_to_dict(func))
