import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="Smart Pro Assistant", page_icon="🤖")

st.title("🎙️ Smart Pro Assistant")
st.write("Ce prototype transcrit et résume vos échanges vocaux avec les clients professionnels.")

# API URL depuis variables d’environnement
API_URL = os.getenv("API_URL", "http://localhost:8000")



# Sélection du profil métier
profil = st.selectbox("Quel est votre métier ?", ["Banquier", "Juriste", "Avocat", "Agent immobilier", "SAV"])

# Upload fichier audio
audio_file = st.file_uploader("Téléversez un enregistrement audio", type=["wav", "m4a", "mp3"])
# ✅ Section de téléchargement des fichiers audio de test
st.markdown("### 📥 Fichiers audio de test")
st.markdown(
    """
    Vous pouvez télécharger des exemples de fichiers audio pour tester l'application :

    - [🎧 Banquier.wav](https://github.com/marcelnjapo/smartpro-audio-samples/blob/main/banquier.wav)
    - [🎧 Avocat.wav](https://github.com/marcelnjapo/smartpro-audio-samples/blob/main/avocat.wav)
    - [🎧 SAV.wav](https://github.com/marcelnjapo/smartpro-audio-samples/blob/main/sav.wav)
    - [🎧 Juriste.wav](https://github.com/marcelnjapo/smartpro-audio-samples/blob/main/juriste.wav)
    - [🎧 Agent immobilier.wav](https://github.com/marcelnjapo/smartpro-audio-samples/blob/main/agent_immobilier.wav)

    👉 Téléchargez un fichier, puis importez-le ci-dessous pour lancer l’analyse.
    """
)
if audio_file:
    st.audio(audio_file, format="audio/wav")

    if st.button("Envoyer pour transcription"):
        with st.spinner("⏳ Transcription en cours..."):
            try:
                files = {"file": (audio_file.name, audio_file, audio_file.type or "audio/m4a")}
                data = {"profil": profil}
                response = requests.post(f"{API_URL}/transcribe", files=files, data=data)

                if response.status_code == 200:
                    data = response.json()
                    transcription = data["transcription"]
                    summary = data["summary"]
                    sentiment = data["sentiment"]
                    pdf_base64 = data["pdf_base64"]

                    st.success("✅ Transcription réussie")
                    st.text_area("📝 Transcription", transcription, height=200)

                    st.markdown("### 🧠 Résumé automatique")
                    st.write(summary)

                    st.markdown("### 😃 Analyse de sentiment")
                    st.info(sentiment)

                    st.markdown("### 📄 Télécharger la fiche PDF")
                    st.download_button(
                        label="📥 Télécharger",
                        data=base64.b64decode(pdf_base64),
                        file_name=f"fiche_{profil.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error(f"❌ Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Erreur réseau ou API : {str(e)}")
