from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import inference

app = FastAPI(title="Smart Pro Assistant API")

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

# Inclusions des routes
app.include_router(inference.router, prefix="/api")
