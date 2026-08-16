from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import time
from services.transcription import transcribe_audio
from services.chunking import chunk_transcript
from services.summarization import summarize_chunk, combine_summaries

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage/uploads"

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Meeting Summarizer backend is running"}

@app.post("/upload")
async def upload_meeting(file: UploadFile = File(...)):
    # 1. Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Transcribe
    transcript = transcribe_audio(file_path)

    # 3. Chunk the transcript
    chunks = chunk_transcript(transcript, max_chunk_words=800)

    # 4. Summarize each chunk (the "map" step), with pacing to respect rate limits
    chunk_summaries = []
    for chunk in chunks:
        result = summarize_chunk(chunk)
        chunk_summaries.append(result)
        time.sleep(2)  # stay safely under 5 requests/minute on the free tier

    # 5. Combine into one final summary (the "reduce" step)
    final_summary = combine_summaries(chunk_summaries)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "summary": final_summary
    }