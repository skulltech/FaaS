from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from urllib.parse import urljoin
import os
import shortuuid
from config import Settings
from schemas import FileOut, FileOutList
from starlette.responses import Response
from starlette.status import HTTP_200_OK


app = FastAPI()
settings = Settings()


@app.get("/files/{filename}")
async def get_file(filename: str) -> FileResponse:
    return FileResponse(
        os.path.join(settings.storage_directory, filename),
        media_type="application/octet-stream",
        filename=filename,
    )


def file_url(filename: str) -> str:
    return urljoin(settings.base_url, app.url_path_for("get_file", filename=filename))


@app.get("/files", response_model=FileOutList)
async def list_files() -> FileOutList:
    files = [
        f
        for f in os.listdir(settings.storage_directory)
        if os.path.isfile(os.path.join(settings.storage_directory, f))
    ]
    return FileOutList(
        files=[
            FileOut(
                filename=filename,
                url=file_url(filename),
            )
            for filename in files
        ]
    )


@app.post("/files", response_model=FileOut)
async def create_file(file: UploadFile = File(...)) -> FileOut:
    filename = shortuuid.uuid() + "-" + file.filename
    with open(os.path.join(settings.storage_directory, filename), "wb") as f:
        f.write(await file.read())
    return FileOut(filename=filename, url=file_url(filename))


@app.delete("/files/{filename}")
async def delete_file(filename: str) -> FileResponse:
    os.remove(os.path.join(settings.storage_directory, filename))
    return Response(status_code=HTTP_200_OK)
