from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inference
from app.services.auth_cognito import verify_jwt
from app.db import models


# Création des tables (code first)

app = FastAPI(
    title="Smart Pro Assistant API",
    root_path="/api/smartpro"  # C’est ici qu’on aligne avec l’ALB
)

# CORS (utile pour les appels depuis Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API SmartPro Assistant 🚀"}

@app.get("/")
def public_route():
    return {"message": "Accessible sans authentification"}

@app.get("/secure")
def secure_route(user=Depends(verify_jwt)):
     return {
        "username": user.get("cognito:username"),
        "email": user.get("email"),
        "given_name": user.get("given_name"),
        "family_name": user.get("family_name")
    }

# Inclusions des routes
app.include_router(inference.router)
