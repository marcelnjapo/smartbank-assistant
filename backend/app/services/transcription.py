from openai import OpenAI
from app.config import OPENAI_API_KEY
import io

client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_with_openai(file_bytes: bytes, filename: str):
    # Forcer l'extension correcte
    if not filename.endswith(".m4a"):
        filename += ".m4a"

    file = io.BytesIO(file_bytes)
    file.name = filename  # Obligatoire pour OpenAI API

    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="json"
        )
        return transcript.text
    except Exception as e:
        raise RuntimeError(f"Erreur OpenAI : {e}")
