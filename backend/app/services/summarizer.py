from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_transcript(transcript: str, profil: str = "Banquier") -> str:
    # Prompts personnalisés selon le métier
    prompts = {
        "Banquier": (
            "Tu es un assistant bancaire. Résume l’échange entre le client et le conseiller. "
            "dans un format structuré avec les sections suivantes :\n\n"
            "1. Objectif de l’échange\n"
            "2. Résumé de la discussion\n"
            "3. Points clés / besoins exprimés\n"
            "4. Solutions ou recommandations\n"
            "5. Prochaines étapes"
        ),
        "Juriste": (
            "Tu es un assistant juridique. Résume cet échange vocal en mettant en évidence les enjeux juridiques, "
            "dans un format structuré avec les sections suivantes :\n\n"
            "1. Objectif de l’échange\n"
            "2. Résumé de la discussion\n"
            "3. Points clés / besoins exprimés\n"
            "4. Solutions ou recommandations\n"
            "5. Prochaines étapes"
        ),
        "Avocat": (
            "Tu es un assistant pour un avocat. Résume l’échange en extrayant les faits clés de l’affaire, "
            "les parties concernées, les dates importantes et les objectifs du client."
            "dans un format structuré avec les sections suivantes :\n\n"
            "1. Objectif de l’échange\n"
            "2. Résumé de la discussion\n"
            "3. Points clés / besoins exprimés\n"
            "4. Solutions ou recommandations\n"
            "5. Prochaines étapes"
        ),
        "Agent immobilier": (
            "Tu es un assistant immobilier. Résume cet échange pour identifier le type de bien recherché, "
            "le budget, la localisation, les critères, et les prochaines actions à mener."
            "dans un format structuré avec les sections suivantes :\n\n"
            "1. Objectif de l’échange\n"
            "2. Résumé de la discussion\n"
            "3. Points clés / besoins exprimés\n"
            "4. Solutions ou recommandations\n"
            "5. Prochaines étapes"
        ),
          "SAV": (
            "Tu es un assistant du service après-vente. Résume la demande du client concernant un produit défectueux. "
            "Identifie le produit concerné, les problèmes rencontrés, les vérifications effectuées, "
            "et la solution apportée par le conseiller SAV."
            "dans un format structuré avec les sections suivantes :\n\n"
            "1. Objectif de l’échange\n"
            "2. Résumé de la discussion\n"
            "3. Points clés / besoins exprimés\n"
            "4. Solutions ou recommandations\n"
            "5. Prochaines étapes"
        )
    }

    # Fallback générique
    base_prompt = prompts.get(profil, prompts["Banquier"])

    # Construction du prompt final
    full_prompt = f"{base_prompt}\n\nVoici la transcription à résumer :\n{transcript}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ou gpt-4 si tu veux
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
