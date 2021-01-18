from pydantic import BaseModel


class InvocationResult(BaseModel):
    exitcode: int
    output: str


class InvocationParams(BaseModel):
    argument: dict
