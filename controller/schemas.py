from pydantic import BaseSettings, BaseModel
from typing import Optional, List


class Settings(BaseSettings):
    docker_registry: str = "hal9011"


class FunctionBase(BaseModel):
    payload: str
    handler: str


class FunctionIn(FunctionBase):
    pass


class FunctionOut(FunctionBase):
    id: str


class FunctionOutList(BaseModel):
    functions: List[FunctionOut]