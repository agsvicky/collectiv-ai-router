<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="320" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Multi-Provider AI Routing · Backend für die CollectiVAI App</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-iOS·iPadOS·macOS-ffcc00?style=flat" alt="CollectiVAI App" />
  </a>
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

---

> ⚠️ **Status:** Frühes Experiment / Prototyp (v0.1)  
> Backend-Router für die CollectiVAI App – **nicht produktiv einsetzen**.

---

## 🧠 Was ist der CollectiVAI Router?

Der **CollectiVAI Router** ist ein kleines Backend, das als „Gehirn“ hinter der  
**CollectiVAI App** läuft:

- nimmt Chat-Anfragen von der App entgegen  
- routet sie an unterschiedliche AI-Provider (OpenAI, Gemini, Mistral, Meta, DeepSeek, lokale Modelle …)  
- berücksichtigt **Mode, Topic, Service-Profil und Modellwahl**  
- gibt eine **einheitliche Antwort** inkl. Routing-Meta-Infos zurück

Die iOS / iPadOS / macOS-App spricht den Router über eine einfache HTTP-API an.  
In der App ist das als `CollectivAIBackend.send(…)` implementiert.

---

## 🧩 Aktuelle Rolle im CollectiVAI Ökosystem

- **Frontend:**  
  CollectiVAI SwiftUI-App mit:
  - Provider-Auswahl (Auto, OpenAI, Gemini, Mistral, Meta, DeepSeek)  
  - Modes (`Ethical`, `Research`, `Technical`)  
  - Topics (Democracy, Climate, Security, …)  
  - Civic Service Profiles (City, Universities, NGOs, Citizens, Startups)  
  - Civics-Tabs: **Chat · Contracts · Chain · Settings**

- **Backend:**  
  Dieser Router:

  - nimmt strukturierte Requests der App entgegen  
  - entscheidet, **welches Modell** tatsächlich verwendet wird  
  - kann ein **Ethik- / Privacy-Overlay** implementieren  
  - liefert Routing-Infos zurück (Provider, Modell, Latenz, Filter, Reason)

- **Provider-Ebene (später):**
  - OpenAI, Google Gemini, Mistral, Meta, DeepSeek, lokale Modelle (Ollama, etc.)  
  - zusätzliche Layer für Governance, Logging, Safety, EU-Compliance

---

## 🔌 API-Vertrag (wie die App mit dem Router spricht)

### Endpoint

Der Router stellt (lokal oder im Netz) z. B. einen Endpoint bereit:

```text
POST /api/chat
Content-Type: application/json
