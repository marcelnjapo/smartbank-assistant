from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.models import TranscriptionHistory



from app.services.summarizer import summarize_transcript
from app.services.pdf_generator import generate_pdf_base64
from app.services.transcription import transcribe_with_openai
from app.services.translation_utils import translate_to_english
import base64
from app.services.sentiment import analyze_sentiment

from fastapi import Depends, Header, HTTPException
from app.services.auth_cognito import verify_jwt
from app.dependencies.db import get_db 
router = APIRouter()



@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...),profil: str = Form("Banquier"), user: dict = Depends(verify_jwt),db: Session = Depends(get_db)):
    
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/m4a", "audio/mp4", "audio/x-m4a", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Format audio non supporté")

    file_bytes = await file.read()

    try:
        transcript = transcribe_with_openai(file_bytes, file.filename)
        summary = summarize_transcript(transcript,profil)
        summary_en=translate_to_english(summary)
        sentiment = analyze_sentiment(transcript)
        # Générer le PDF directement en base64
        pdf_base64 = generate_pdf_base64(profil, summary, transcript,sentiment)
       
       #🔴 Enregistrement en base
        print(user)
        history = TranscriptionHistory(
            username = f"{user.get('given_name')} {user.get('family_name')}",
            email=user.get("email"),
            transcript=transcript,
            summary=summary,
            role=profil,
            sentiment=sentiment

        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return JSONResponse(content={
                "transcription": transcript,
                "summary": summary,
                "summary_en":summary_en,
                "sentiment": sentiment,
                "pdf_base64": pdf_base64})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la transcription : {str(e)}")
    


@router.get("/history")
def get_transcription_history(
    user: dict = Depends(verify_jwt),
    db: Session = Depends(get_db)
):
    username = f"{user.get('given_name')} {user.get('family_name')}"

    if not username:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")

    history = (
        db.query(TranscriptionHistory)
        .filter(TranscriptionHistory.username == username)
        .order_by(TranscriptionHistory.created_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "username":item.username,
            "profil": item.role,
            "transcript": item.transcript[:300],  # Optionnel : tronquer
            "summary": item.summary[:300],        # Optionnel : tronquer
            "sentiment": item.sentiment,
            "timestamp": item.created_at.isoformat(),
        }
        for item in history
    ]
