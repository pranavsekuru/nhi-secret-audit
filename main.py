from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class NHI(BaseModel):
    name: str
    type: str
    status: str


@app.get("/")
def home():
    return {
        "message": "NHI Secret Audit Service is running"
    }


@app.post("/nhi")
def create_nhi(nhi: NHI):
    return {
        "success": True,
        "message": "NHI registered successfully",
        "data": {
            "name": nhi.name,
            "type": nhi.type,
            "status": nhi.status
        }
    }