import streamlit as st
import requests
from io import BytesIO
import base64
import os

st.set_page_config(page_title="Smart Pro Assistant", page_icon="🤖")

st.title("🎙️ Smart Pro Assistant")
st.write("Ce prototype transcrit et résume vos échanges vocaux avec les clients professionnels.")

profil = st.selectbox("Quel est votre métier ?", ["Banquier", "Juriste", "Avocat", "Agent immobilier", "SAV"])
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ✅ Section : Fichiers audio de démonstration
# ✅ Section : Fichiers audio de démonstration (avec expander)
with st.expander("📥 Fichiers audio de test (cliquer pour afficher / masquer)"):
    demo_files = {
        "Banquier.wav": "https://smartproassistant.s3.eu-central-1.amazonaws.com/banquier.wav",
        "Avocat.wav": "https://smartproassistant.s3.eu-central-1.amazonaws.com/avocat.wav",
        "SAV.wav": "https://smartproassistant.s3.eu-central-1.amazonaws.com/sav.wav",
        "Juriste.wav": "https://smartproassistant.s3.eu-central-1.amazonaws.com/juriste.wav",
        "Agent immobilier.wav": "https://smartproassistant.s3.eu-central-1.amazonaws.com/agent_immobilier.wav"
    }

    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None

    for label, url in demo_files.items():
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

    if st.button("Envoyer pour transcription"):
        with st.spinner("⏳ Transcription en cours..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type or "audio/m4a")}
                data = {"profil": profil}
                response = requests.post(f"{API_URL}/transcribe", files=files, data=data)

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Transcription réussie")
                    st.text_area("📝 Transcription", data["transcription"], height=200)

                    st.markdown("### 🧠 Résumé automatique")
                    st.write(data["summary"])

                    st.markdown("### 😃 Analyse de sentiment")
                    st.info(data["sentiment"])

                    st.markdown("### 📄 Télécharger la fiche PDF")
                    st.download_button(
                        label="📥 Télécharger la fiche",
                        data=base64.b64decode(data["pdf_base64"]),
                        file_name=f"fiche_{profil.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error(f"❌ Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
