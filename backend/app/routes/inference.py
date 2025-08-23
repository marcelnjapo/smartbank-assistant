from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.summarizer import summarize_transcript
from services.pdf_generator import generate_pdf_base64
from services.transcription import transcribe_with_openai
import base64
from services.sentiment import analyze_sentiment
router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...),profil: str = Form("Banquier")):
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/m4a", "audio/mp4", "audio/x-m4a", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Format audio non supporté")

    file_bytes = await file.read()

    try:
        transcript = transcribe_with_openai(file_bytes, file.filename)
        summary = summarize_transcript(transcript,profil)
        sentiment = analyze_sentiment(transcript)
        # Générer le PDF directement en base64
        pdf_base64 = generate_pdf_base64(profil, summary, transcript,sentiment)
       
        return JSONResponse(content={
                "transcription": transcript,
                "summary": summary,
                "sentiment": sentiment,
                "pdf_base64": pdf_base64})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la transcription : {str(e)}")

