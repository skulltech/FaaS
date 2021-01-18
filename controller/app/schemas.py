from pydantic import BaseModel
from typing import List


class FunctionBase(BaseModel):
    payload: str
    handler: str


class FunctionIn(FunctionBase):
    pass


class FunctionOut(FunctionBase):
    id: str


class FunctionOutList(BaseModel):
    functions: List[FunctionOut]
