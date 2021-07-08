from fastapi import FastAPI, File, UploadFile, Response, Header
from fastapi.responses import FileResponse
from typing import Optional
from deta import Deta
from pydantic import BaseModel
import hashlib
import jwt
import uuid
import json
from datetime import datetime, timedelta
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# pydantic to declare body of put or post
app = FastAPI()
a = "c0ih1z2i_gjQeDzhBwsJSU"
deta = Deta(a+"btdTrNurU2bg69GSfLv")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "It's Hackathon Time!!"}


@app.post("/api/fileupload")
def updateImage(file: UploadFile = File(...)):
    
    hackDrive = deta.Drive("HackathonFiles")
    
    fileName = str(uuid.uuid4())
    fileExtension = file.filename.split(".")[1]
    fileName += "."+fileExtension
    
    hackDrive.put(name=fileName, data=file.file)

    return {
        "status": 200,
        "link": "https://acm-hackathon.deta.dev/api/getfile/"+fileName
    }
    
@app.get("/api/getfile/{fileLocation}")
def getImage(fileLocation: str):
    
    hackDrive = deta.Drive("HackathonFiles")
    try:
        theFile = hackDrive.get(fileLocation)
        return StreamingResponse(theFile.iter_chunks(1024))
    except:
        return({
            "status": 404,
            "message": "File Does not Exist"
        })

# "endpoint": "https://vd65r8.deta.dev",
