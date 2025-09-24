import streamlit as st
import requests
from io import BytesIO
import base64
import os
from tts_utils import generate_tts_audio
import urllib.parse
from dotenv import load_dotenv
from urllib.parse import quote,urlencode
import requests
from jose import jwt



load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/api/smartpro")
COGNITO_CLIENT_ID=os.getenv("COGNITO_CLIENT_ID")
COGNITO_DOMAIN=os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_SECRET=os.getenv("COGNITO_CLIENT_SECRET")
COGNITO_REDIRECT_URI = os.getenv("COGNITO_REDIRECT_URI", "http://localhost:8501") 
# Scope demandé par Cognito
SCOPES = ["openid", "email", "profile"]


st.set_page_config(page_title="Smart Pro Assistant",
                    page_icon="🤖",
                    layout="wide",  
                    initial_sidebar_state="auto"
                    )
# Load CSS styles
with open("frontend/style_buttons.css") as f:
     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                  
# OAuth2 - Connexion Cognito
query_params = st.query_params
auth_headers={}
if "code" in query_params:
    code = query_params["code"]

    # Échange du code contre un id_token
    token_url = f"https://{COGNITO_DOMAIN}/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": COGNITO_CLIENT_ID,
        "code": code,
        "redirect_uri": COGNITO_REDIRECT_URI
    }
   
     # 🔐 Construction du header Basic Auth
    basic_auth = f"{COGNITO_CLIENT_ID}:{COGNITO_CLIENT_SECRET}"
    b64_auth = base64.b64encode(basic_auth.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_auth}"
    }

    try:
        response = requests.post(token_url, data=urlencode(payload), headers=headers)
        response.raise_for_status()
        tokens = response.json()
        st.session_state["id_token"] = tokens["id_token"]
        # Nettoyer l'URL (enlève ?code=...)
       
        query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Erreur lors de l'échange du token : {str(e)}")
        st.stop()

user_info = {}
if "id_token" in st.session_state:
    try:
        auth_headers = {"Authorization": f"Bearer {st.session_state['id_token']}"}
        user_info = jwt.get_unverified_claims(st.session_state["id_token"])
        user_email = user_info.get("email")
        user_name = user_info.get("given_name", "") + " " + user_info.get("family_name", "")
        st.success(f"✅ Connecté en tant que : {user_name or user_email}")
    except Exception as e:
        st.warning("⚠️ Token invalide ou expiré.")
        st.session_state.clear()
    
# 🔘 Boutons connexion / déconnexion
login_url = (
f"https://{COGNITO_DOMAIN}/login?"
f"client_id={COGNITO_CLIENT_ID}"
f"&response_type=code"
f"&scope={'+'.join(SCOPES)}"
f"&redirect_uri={quote(COGNITO_REDIRECT_URI,safe='')}"
    )
logout_url = (
        f"https://{COGNITO_DOMAIN}/logout?"
        f"client_id={COGNITO_CLIENT_ID}&"
        f"logout_uri={quote(COGNITO_REDIRECT_URI, safe='')}"
    )
    
# 🧭 Haut de page : à droite (icone 👤 + bouton)
with st.container():
    col_spacer, col_user = st.columns([8, 1.5])
    with col_user:
        if "id_token" in st.session_state:
            if st.button("🔒 Se déconnecter", key="bouton-deconnexion"):
                st.session_state.clear()
                st.markdown(f"<meta http-equiv='refresh' content='0;url={logout_url}'>", unsafe_allow_html=True)
                st.stop()
        else:
            st.markdown(
            f"<div style='text-align:right;'><a href='{login_url}'><button class='bouton-connexion'>🖐️ Se connecter</button></a></div>",
            unsafe_allow_html=True
    )

       
# ✅ CONTENU DE LA PAGE (affiché à tous)
st.title("🎙️ Smart Pro Assistant")
st.write("Ce prototype transcrit et résume vos échanges vocaux avec les clients professionnels.")
if "id_token" not in st.session_state:
     st.markdown(
                """
                <div style='
                    background-color: #fdecea;
                    color: #a94442;
                    padding: 15px;
                    border-left: 6px solid #f44336;
                    border-radius: 4px;
                    font-weight: 500;
                '>
                    🔐 Connectez-vous pour utiliser toutes les fonctionnalités, comme la transcription, le résumé vocal ou le téléchargement du PDF.".
                </div>
                """,
                unsafe_allow_html=True
            )
col_formulaire, col_historique = st.columns([2, 1])  # 2/3 pour le formulaire, 1/3 pour l’historique

with col_formulaire:
    profil = st.selectbox("Quel est votre métier ?", ["Banquier", "Juriste", "Avocat", "Agent immobilier", "SAV"])



    # ✅ Section : Fichiers audio de démonstration
    # ✅ Section : Fichiers audio de démonstration (avec expander)
    with st.expander("📥 Fichiers audio de test (cliquer pour afficher / masquer)"):
        demo_files = {
            "Banquier": "https://smartproassistant.s3.eu-central-1.amazonaws.com/banquier.wav",
            "Avocat": "https://smartproassistant.s3.eu-central-1.amazonaws.com/avocat.wav",
            "SAV": "https://smartproassistant.s3.eu-central-1.amazonaws.com/sav.wav",
            "Juriste": "https://smartproassistant.s3.eu-central-1.amazonaws.com/juriste.wav",
            "Agent immobilier": "https://smartproassistant.s3.eu-central-1.amazonaws.com/agent_immobilier.wav"
        }

        if "uploaded_file" not in st.session_state:
            st.session_state["uploaded_file"] = None

        if profil in demo_files:
            url=demo_files[profil]
            label=f"{profil}.wav"
            st.markdown(f"**🎧 {label}**")
            st.audio(url, format="audio/wav")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label=f"📥 Télécharger {label}",
                    data=requests.get(url).content,
                    file_name=label,
                    mime="audio/wav"
                )
            with col2:
                if st.button(f"📤 Importer automatiquement {label}", key=f"import_{label}"):
                    response = requests.get(url)
                    if response.status_code == 200:
                        st.session_state["uploaded_file"] = {
                            "name": label,
                            "content": BytesIO(response.content),
                            "type": "audio/wav"
                        }
                        st.success(f"{label} a été importé dans le formulaire ci-dessous !")
                    else:
                        st.error(f"❌ Échec de l'import automatique de {label}.")
            st.markdown("---")


    # ✅ Upload manuel du fichier personnel
    uploaded_file = st.file_uploader("Ou téléversez votre propre fichier audio :", type=["wav", "m4a", "mp3"])

    # ✅ Priorité à l’import automatique si présent
    if st.session_state.get("uploaded_file") and uploaded_file is None:
        st.info(f"📤 Fichier auto-importé : {st.session_state['uploaded_file']['name']}")
        uploaded_file = st.session_state["uploaded_file"]["content"]
        uploaded_file.name = st.session_state["uploaded_file"]["name"]
        uploaded_file.type = st.session_state["uploaded_file"]["type"]

    # ✅ Affichage de l’audio + envoi à l’API
    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")
        st.markdown("---")
    # ✅ Encadré explicatif
        st.markdown("""
            <div style='
                background-color: #f0f9ff;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #2196f3;
                margin-bottom: 20px;
            '>
                <p style="font-size:20px; font-weight:bold; color:#0d47a1;">
                    🎯 Cliquez ci-dessous pour lancer l’analyse vocale complète
                </p>
                <p style="font-size:16px; color:#0d47a1;">
                    Transcription, résumé, sentiment & fiche PDF générée automatiquement
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ✅ Bouton bien visible et centré
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎧 Envoyer pour transcription", key="transcribe_btn"):
                if "id_token" not in st.session_state:
                    st.markdown(
                        """
                        <div style='
                            background-color: #fdecea;
                            color: #a94442;
                            padding: 15px;
                            border-left: 6px solid #f44336;
                            border-radius: 4px;
                            font-weight: 500;
                            margin-top: 20px;
                        '>
                            ❌ Vous devez être connecté pour utiliser cette fonctionnalité (transcription, résumé, PDF, etc.).
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    with st.spinner("⏳ Transcription en cours..."):
                        try:
                            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type or "audio/m4a")}
                            data = {"profil": profil}
                            
                            response = requests.post(f"{API_URL}/transcribe", files=files, data=data, headers=auth_headers)

                            if response.status_code == 200:
                                data = response.json()
                                st.success("✅ Transcription réussie")
                                st.text_area("📝 Transcription", data["transcription"], height=200)

                                st.markdown("### 🧠 Résumé automatique")
                                st.write(data["summary"])
                                # ✅ Option pour afficher la traduction anglaise
                                with st.expander("### 🌍 Traduction anglaise du résumé"):
                                    st.write(data["summary_en"])
                                st.markdown("### 😃 Analyse de sentiment")
                                st.info(data["sentiment"])

                                st.markdown("### 📄 Télécharger la fiche PDF")
                                st.download_button(
                                    label="📥 Télécharger la fiche",
                                    data=base64.b64decode(data["pdf_base64"]),
                                    file_name=f"fiche_{profil.lower().replace(' ', '_')}.pdf",
                                    mime="application/pdf"
                                )
                                audio_data = generate_tts_audio(data["summary"])
                                st.markdown("### 🔈 Écouter le résumé vocal")
                                #lecture audio Streamlit
                                st.audio(audio_data, format="audio/mp3")
                                # 📥 Bouton de téléchargement
                                st.download_button(
                                    label="📥 Télécharger le résumé vocal",
                                    data=audio_data,
                                    file_name="resume_audio.mp3",
                                    mime="audio/mpeg"
                                )
                            else:
                                st.error(f"❌ Erreur API : {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"❌ Erreur : {str(e)}")
with col_historique:
    if st.checkbox("📜 Afficher mon historique de transcription"):
        if "id_token" not in st.session_state:
            st.error("Vous devez être connecté pour voir votre historique.")
        else:
            
            try:
                with st.spinner("Chargement de l'historique..."):
                
                    response = requests.get(f"{API_URL}/history", headers=auth_headers)

                    if response.status_code == 200:
                        history_data = response.json()
                        if not history_data:
                            st.info("Aucun historique trouvé.")
                        else:
                            for item in history_data:
                                st.markdown("---")
                                st.markdown(f"🧑‍💼 **Nom** : `{item['username']}`")
                                st.markdown(f"🧑‍💼 **Profil** : `{item['profil']}`")
                                st.markdown(f"🕒 **Date** : `{item['timestamp']}`")
                                st.markdown(f"📝 **Résumé** :\n\n{item['summary']}")
                                st.markdown(f"📈 **Sentiment** : `{item['sentiment']}`")
                    else:
                        st.error(f"Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erreur lors du chargement de l'historique : {e}")
