
# 🧠 Smart Pro Assistant

> **Prototype IA de transcription, résumé et analyse des échanges vocaux entre professionnels et clients.**

[🎥 Démo (optionnel)](https://apps.njapsconsulting.com/smartpro)

---

## 🚀 Objectifs

Smart Pro Assistant est une application déployée sur AWS qui permet :

- 🗣️ D'uploader des enregistrements vocaux clients (banquier, juriste, etc.)
- ✍️ De transcrire automatiquement le contenu audio
- 🧠 De générer un résumé structuré de la conversation
- 😊 D’analyser le sentiment global de l’échange
- 📄 De produire une fiche PDF automatiquement téléchargeable

---

## 🧱 Architecture du projet

```
smart-pro-assistant/
├── backend/ (FastAPI)
│   ├── main.py
│   ├── routes/inference.py
│   └── utils/ (transcription, résumé, PDF, etc.)
│
├── frontend/ (Streamlit)
│   ├── app.py
│   ├── Dockerfile.frontend
│   └── assets/
│
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml
│       └── deploy-frontend.yml
│
└── README.md
```

---

## ☁️ Déploiement AWS

L’ensemble est **déployé automatiquement sur AWS** grâce à **GitHub Actions**, via :

- 📦 **ECR** pour les images Docker
- 🐳 **ECS Fargate** pour héberger les conteneurs (backend & frontend)
- 🌐 **ALB** avec routage basé sur les chemins (`/api/smartpro`, `/smartpro`)
- 🔐 **HTTPS** via certificat SSL (ACM)
- ⚙️ **CI/CD** déclenché automatiquement à chaque `git push` sur `main`

### ✅ URL en production

- Frontend : [https://apps.njapsconsulting.com/smartpro](https://apps.njapsconsulting.com/smartpro)
- Backend : [https://apps.njapsconsulting.com/api/smartpro/api/transcribe](https://apps.njapsconsulting.com/api/smartpro/api/transcribe)

---

## 📦 Variables d’environnement GitHub

| Nom | Description |
|-----|-------------|
| `API_URL` | URL du backend (ex: `https://apps.njapsconsulting.com/api/smartpro`) |
| `ECR_REPOSITORY_BACKEND` / `FRONTEND` | Repos ECR pour les images Docker |
| `SERVICE_NAME_BACKEND` / `FRONTEND` | Nom des services ECS |
| `CLUSTER_NAME` | Nom du cluster ECS |
| `TG_ARN_BACKEND` / `FRONTEND` | ARN des Target Groups ALB |
| `SUBNET_1`, `SUBNET_2` | Subnets privés/publics |
| `SECURITY_GROUP_ID` | Groupe de sécurité pour ECS |
| `ACCOUNT_ID`, `AWS_REGION` | Infos du compte AWS |

---

## 🛠️ Technologies utilisées

- **Python / FastAPI** (backend API)
- **Streamlit** (frontend interactif)
- **Docker** + **Amazon ECR / ECS Fargate**
- **GitHub Actions** (CI/CD complet)
- **HTTPS + ACM** via Application Load Balancer (ALB)
- **LLM / Whisper (optionnel)** pour transcription

---

## 🔮 Améliorations possibles

- 🧾 Ajouter l'historique des conversations
- 🧠 Intégrer un LLM pour une FAQ ou résumé plus riche
- 📊 Dashboard analytique par utilisateur
- 🔐 Authentification et gestion de comptes

---

## 📸 Capture d’écran

![Demo Screenshot](assets/demo.png)

---

## 🙌 Auteur

Projet personnel réalisé par Marcel Njapo 
👉 N'hésitez pas à [me contacter](mailto:marcel.njapo@gmail.com) pour toute question ou collaboration.
