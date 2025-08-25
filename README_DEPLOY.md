# 🎙️ SmartPro Assistant – FastAPI + Streamlit, déployé en CI/CD sur AWS 🚀

[![Deploy Backend](https://github.com/marcelnjapo/smartbank-assistant/actions/workflows/deploy-backend.yml/badge.svg)](https://github.com/marcelnjapo/smartpro-assistant/actions/workflows/deploy-backend.yml)
[![Deploy Frontend](https://github.com/marcelnjapo/smartbank-assistant/actions/workflows/deploy-frontend.yml/badge.svg)](https://github.com/marcelnjapo/smartpro-assistant/actions/workflows/deploy-frontend.yml)

Ce projet est un assistant intelligent vocal pour les professionnels (banquier, juriste, etc.). Il transcrit, résume et analyse vos échanges audio avec vos clients et génère automatiquement une **fiche PDF**. Il est intégralement déployé sur **AWS** avec une infrastructure **Fargate + ALB** et une stratégie **CI/CD GitHub Actions**.

## 🌐 Accès à l'application

- 🔗 **Frontend (Streamlit)** : [https://apps.njapsconsulting.com/smartpro/](https://apps.njapsconsulting.com/smartpro/)
- 🔗 **API Backend (FastAPI)** : [https://apps.njapsconsulting.com/api/smartpro/docs](https://apps.njapsconsulting.com/api/smartpro/docs)

---

## 🧠 Fonctionnalités

- 🎙️ Transcription vocale (OpenAI Whisper)
- 🧠 Résumé automatique des conversations
- 📄 Génération de fiches PDF professionnelles
- 😊 Analyse de sentiment
- 🔐 Déploiement sécurisé HTTPS via certificat SSL
- 🧬 Architecture scalable sur AWS ECS Fargate
- 🔁 CI/CD complet avec GitHub Actions

---

## 🏗️ Architecture AWS

```
Client → ALB (HTTPS + Path-based routing)
        ├── /smartpro/       → Frontend (Streamlit)
        └── /api/smartpro/   → Backend (FastAPI)
```

---

## 🔁 Déploiement CI/CD (GitHub Actions)

Deux pipelines séparés :
- `deploy-backend.yml` pour l'API FastAPI
- `deploy-frontend.yml` pour l'app Streamlit

**Étapes CI/CD :**
1. `git push` déclenche le workflow.
2. Le code est buildé avec Docker.
3. L’image est poussée vers ECR.
4. Une Task Definition ECS est rendue puis enregistrée.
5. Le service ECS est créé ou mis à jour (avec ALB et target group).
6. Le Load Balancer route vers le bon chemin.

---

## 📁 Arborescence principale

```
📦 smartpro-assistant
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   └── Dockerfile.backend
├── frontend/
│   ├── app.py
│   └── Dockerfile.frontend
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml
│       └── deploy-frontend.yml
│   └── task-definitions/
│       ├── backend.json
│       └── frontend.json
└── README.md
```

---

## 🛠️ Technologies

- 🐍 **FastAPI** – Backend API
- 📦 **Streamlit** – Interface utilisateur
- 🧠 **OpenAI Whisper + GPT-3.5** – IA
- 🐳 **Docker** – Conteneurisation
- ☁️ **AWS ECS Fargate** – Déploiement serverless
- 🐙 **GitHub Actions** – CI/CD
- 🔒 **ACM + HTTPS** – Sécurisation SSL

---

## 📌 Variables GitHub requises

### 🔐 Secrets
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `OPENAI_API_KEY`

### ⚙️ Variables
- `ECR_REPOSITORY`
- `ECR_REPOSITORY_FRONTEND`
- `ACCOUNT_ID`
- `AWS_REGION`
- `CLUSTER_NAME`
- `SERVICE_NAME_BACKEND`
- `SERVICE_NAME_FRONTEND`
- `SUBNET_1`
- `SUBNET_2`
- `SECURITY_GROUP_ID`
- `TG_ARN_BACKEND`
- `TG_ARN_FRONTEND`
- `API_URL` → `https://apps.njapsconsulting.com/api/smartpro/`

---

## ✨ Résultat final

![demo](assets/demo_smartpro.png)

---

## 🤝 Contribuer

Si tu veux proposer des idées d’amélioration (rôle utilisateur, historique des sessions, email du PDF…), n’hésite pas à ouvrir une issue ou une pull request !

---

## © Auteurs

- 🧑‍💻 Projet personnel réalisé par **[Ton Nom / Njaps Consulting](https://www.njapsconsulting.com)** pour démontrer une mise en production complète avec **FastAPI + Streamlit + AWS ECS Fargate + CI/CD**.