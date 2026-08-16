from groq import Groq

client = Groq()

def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo"
        )
    return transcription.text