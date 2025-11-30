<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="400" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Mini backend for democratic AI routing</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-iOS%20%7C%20iPadOS%20%7C%20macOS-ffcc00?style=flat" alt="App" />
  </a>
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

---

<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="420" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Multi‑provider AI routing backend for the CollectiVAI app</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-iOS%20·%20iPadOS%20·%20macOS-ffcc00?style=flat" alt="CollectiVAI App" />
  </a>
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

> **Status:** Prototype backend for the CollectiVAI app  
> **Stack:** Python · FastAPI · httpx · Cloudflare (reverse proxy / Workers)  
> **Security:** No API keys stored in the app – all secrets live in the router / platform.

---

## 🇬🇧 Overview

The **CollectiVAI Router** is the backend that the **CollectiVAI iOS / iPadOS / macOS app**
uses to send chat requests.

It receives a request like:

```jsonc
POST /api/chat
{
  "prompt": "How can citizens participate in climate decisions in the EU?",
  "mode": "ethical",
  "provider": "auto",
  "topic": "climate",
  "modelId": null,
  "serviceProfile": "citizen_advisor"
}
```

…and then decides which model / provider to call:

- **OpenAI** (e.g. GPT‑4.1, GPT‑4o mini)  
- **Gemini** (e.g. 2.0 Flash / Pro)  
- **Mistral** (e.g. Mistral Small / Large)  
- **Meta** (LLaMA models via a compatible endpoint)  
- **DeepSeek** (chat / reasoner)  
- (optional) **Custom** – your own backend (disabled by default)

The router returns a **single, unified response** back to the app, including some
routing metadata for the developer view:

```jsonc
{
  "reply": "…",
  "providerUsed": "openai",
  "model": "gpt-4.1",
  "routingInfo": {
    "reason": "Ethical mode + democracy topic → high‑reliability model.",
    "filters": ["safety", "democracy"],
    "latencyMs": 850
  }
}
```

In production, this backend can be:

- exposed via a **Cloudflare Worker / Tunnel** (e.g.  
  `https://collectivai-server.collectivai.workers.dev/api/chat`), and  
- connected to the providers using **server‑side API keys**.

The **CollectiVAI App never stores API keys on device.**

---

## 🇩🇪 Überblick

Der **CollectiVAI Router** ist das Backend, mit dem die  
**CollectiVAI App (iOS / iPadOS / macOS)** spricht.

- Die App sendet Anfragen an `/api/chat` mit:
  - `mode` (Ethical, Research, Technical),
  - `topic` (Demokratie, Klima, Sicherheit, …),
  - `provider` (Auto, OpenAI, Gemini, Mistral, Meta, DeepSeek),
  - optional `modelId` und `serviceProfile`.
- Der Router entscheidet, welcher Provider / welches Modell genutzt wird,
  ruft die jeweilige API auf und gibt eine einheitliche Antwort zurück.
- In der **Developer‑Ansicht** der App sieht man zusätzlich Routing‑Infos
  (genutztes Modell, Provider, Latenz, Begründung).

Die API‑Schlüssel liegen **nur im Router / in der Infrastruktur**  
(z. B. Cloudflare‑Variablen), **nicht** in der App.

Weitere Hinweise zur Sicherheit:  
👉 [`SECURITY_NOTES.md`](SECURITY_NOTES.md)

---

## 🧱 Folder structure

Reference structure for this repository:

```text
collectiv-ai-router/
├─ README.md
├─ SECURITY_NOTES.md
├─ .gitignore
├─ .env.example          # template for local dev – never commit real .env
├─ requirements.txt
└─ router/
   ├─ __init__.py
   ├─ config.py          # loads env variables / settings
   ├─ models.py          # pydantic request/response models
   ├─ routing.py         # simple routing logic (auto / profiles)
   ├─ main.py            # FastAPI app with /health and /api/chat
   └─ providers/
      ├─ __init__.py
      ├─ openai_provider.py
      ├─ gemini_provider.py
      ├─ mistral_provider.py
      ├─ meta_provider.py
      ├─ deepseek_provider.py
      └─ custom_provider.py   # placeholder / optional
```

Your current GitHub repo already contains some of these files; the rest can be
added step‑by‑step.

---

## 🚀 Local development

### 1. Clone & create virtualenv

```bash
git clone https://github.com/collectiv-ai/collectiv-ai-router.git
cd collectiv-ai-router

python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
# On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment

Create a local `.env` file based on the template:

```bash
cp .env.example .env
```

Edit `.env` and insert **test keys** (never production keys) for:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `MISTRAL_API_KEY`
- `META_API_KEY`
- `DEEPSEEK_API_KEY`

### 4. Run the dev server

```bash
uvicorn router.main:app --reload --port 8000
```

The router is now available at:

- `http://localhost:8000/health` → health‑check  
- `http://localhost:8000/api/chat` → chat endpoint

For local testing of the iOS/macOS app you can temporarily point the app’s
base URL to `http://localhost:8000/api/chat`.

---

## 🌐 Production / Cloudflare

In production you will typically:

1. Run the router on a small VM / container or serverless environment.  
2. Put **Cloudflare** in front as:
   - reverse proxy / Tunnel (custom domain), or  
   - Worker that forwards to your backend.
3. Store all **API keys as secrets** in Cloudflare or your hosting platform.

The concrete deployment setup is **not included** here, because it depends on
your infrastructure (VM, Docker, Cloudflare, etc.).  
This repo focuses on the **router logic and security model**.

---

## 🔐 Security model (short)

- No API keys in the CollectiVAI app.  
- No real secrets in this repository.  
- `.env` is **ignored** by git (see `.gitignore`).  
- `.env.example` is only a documentation template.  
- Provider API keys are stored **only in your backend / platform**.  
- Logging should be minimal and privacy‑friendly (see `SECURITY_NOTES.md`).

---

## 🧩 Relation to the CollectiVAI app

The current CollectiVAI SwiftUI app expects the backend to:

- accept `POST /api/chat` with the fields:
  - `prompt`, `mode`, `provider`, `topic`, `modelId`, `serviceProfile`
- return:
  - `reply` (string)
  - `providerUsed` (string)
  - `model` (string)
  - optional `routingInfo`:
    - `reason` (string)
    - `filters` (string[])
    - `latencyMs` (int)

The structures in `router/models.py` and the logic in `router/main.py`
are aligned with this contract.

---

## 🤝 Contributing

This is a **public, non‑confidential reference implementation**.

If you want to:

- propose improvements to the routing logic,
- add new providers,
- improve the security hardening,

you can open issues or pull requests in this repository.

Please avoid submitting any code that contains **real secrets, keys or tokens**.

---

## ⚖️ License / Branding

The router code and documentation in this repository may later be released
under a permissive open‑source license. Until then, treat it as:

> **“Public, non‑confidential reference code – All rights reserved.”**

The **CollectiVAI** name, logo and visual identity are protected.  
See the central branding repository for details.

© 2025 David Compasso / CollectiVAI.
