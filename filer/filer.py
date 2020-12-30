from pydantic import BaseSettings, BaseModel
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from urllib.parse import urljoin
import os
import shortuuid


class Settings(BaseSettings):
    storage_directory: str = "storage"
    base_url: str = "http://127.0.0.1:6060/"


class FileOut(BaseModel):
    filename: str
    url: str


class FileOutList(BaseModel):
    files: List[FileOut]


app = FastAPI()
settings = Settings()


@app.get("/files/{filename}")
def get_file(filename: str):
    return FileResponse(
        os.path.join(settings.storage_directory, filename),
        media_type="application/octet-stream",
        filename=filename,
    )


@app.get("/files", response_model=FileOutList)
def list_files():
    files = [
        f
        for f in os.listdir(settings.storage_directory)
        if os.path.isfile(os.path.join(settings.storage_directory, f))
    ]
    return FileOutList(
        files=[
            FileOut(
                filename=filename,
                url=urljoin(
                    settings.base_url, app.url_path_for("get_file", filename=filename)
                ),
            )
            for filename in files
        ]
    )


@app.post("/files", response_model=FileOut)
async def create_file(file: UploadFile = File(...)):
    filename = shortuuid.uuid() + "-" + file.filename
    with open(os.path.join(settings.storage_directory, filename), "wb") as f:
        f.write(await file.read())
    return FileOut(
        filename=filename,
        url=urljoin(settings.base_url, app.url_path_for("get_file", filename=filename)),
    )
