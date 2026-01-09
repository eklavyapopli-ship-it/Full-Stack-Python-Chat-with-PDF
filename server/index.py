from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from worker import process

origins = ["http://localhost:3000"]  # Next.js frontend



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def uploadfile(file: UploadFile):
    try:
        file_path = f"server/uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            z=process(x=file.filename)
            return {"message": "File saved successfully", "path": f"/uploads/{file.filename}","workSuccess":z}
        
    except Exception as e:
        return {"message": e.args}