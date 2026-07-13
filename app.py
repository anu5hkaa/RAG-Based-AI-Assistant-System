import os
import shutil

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from proccesing_incoming import process_question
from processing_upload import process_uploaded_file

app = FastAPI()

# Streamlit runs on a different port (8501) than FastAPI (8000),
# so CORS needs to be open for local dev between the two.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):

    answer = process_question(query.question)

    return {"answer": answer}


@app.post("/upload")
def upload(
    file: UploadFile = File(...),
    number: str = Form(...),
    title: str = Form(...),
):
    os.makedirs("audios", exist_ok=True)
    save_path = os.path.join("audios", file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks_added = process_uploaded_file(save_path, number, title)

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_added": chunks_added,
    }