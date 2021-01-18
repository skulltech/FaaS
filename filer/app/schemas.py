from pydantic import BaseModel
from typing import List


class FileOut(BaseModel):
    filename: str
    url: str


class FileOutList(BaseModel):
    files: List[FileOut]
