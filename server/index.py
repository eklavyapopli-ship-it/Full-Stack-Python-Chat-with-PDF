from fastapi import FastAPI, File, UploadFile, Query
from typing import Annotated
from pathlib import Path
from dotenv import load_dotenv
from retrieval.ret import reply
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from worker import process
from rqClient.rq_client import queue

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
            if(f.name):
                job = queue.enqueue(process,file.filename)
                return {"message": "File saved successfully", "path": f"/uploads/{file.filename}","job":job.id}
        
    except Exception as e:
        return {"message": e.args}
@app.get("/job-status")
def getResult( job_id: str = Query(...,description="Job ID")
):
    
    job = queue.fetch_job(job_id=job_id)
    resut = job.result
    return{"result": resut}

@app.get("/chat")
def getReply(mess:str = Query(...,description="user message")):
    k = reply(mess)
    return {"ans":k}