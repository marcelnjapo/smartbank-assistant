from transformers import pipeline


# Chargement unique du modèle au démarrage
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> str:
    result = sentiment_pipeline(text[:1000])[0]  # tronque si texte très long
    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        return f"😊 Positif ({score:.2f})"
    elif label == "NEGATIVE":
        return f"😠 Négatif ({score:.2f})"
    else:
        return f"😐 Neutre ({score:.2f})"
