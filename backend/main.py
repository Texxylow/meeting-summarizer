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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Meeting Summarizer backend is running"}


@app.post("/upload")
async def upload_meeting(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(file_path)

    chunks = chunk_transcript(transcript, max_chunk_words=800)

    chunk_summaries = []
    for chunk in chunks:
        result = summarize_chunk(chunk)
        chunk_summaries.append(result)
        time.sleep(2)

    final_summary = combine_summaries(chunk_summaries)

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "summary": final_summary
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)