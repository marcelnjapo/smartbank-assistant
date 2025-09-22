from gtts import gTTS
import io

def generate_tts_audio(text: str) -> io.BytesIO:
    """Génère un fichier audio MP3 à partir d’un texte (synthèse vocale)."""
    tts = gTTS(text, lang='fr')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp