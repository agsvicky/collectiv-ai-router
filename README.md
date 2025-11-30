<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="380" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Human-Centered AI Routing Layer for the CollectiVAI App</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-Prototype-ffcc00?style=flat" alt="CollectiVAI App" />
  </a>
  <img src="https://img.shields.io/badge/Layer-Router-003399?style=flat" alt="Router Layer" />
  <img src="https://img.shields.io/badge/Status-Early%20Design-999999?style=flat" alt="Status" />
</p>

---

> 🇬🇧 This repository documents the **routing layer** used by the  
> **CollectiVAI App** (iOS / iPadOS / macOS).  
>
> 🇩🇪 Dieses Repository beschreibt die **Routing-Schicht**,  
> die von der **CollectiVAI-App** genutzt wird.

---

## 1. What is the CollectiVAI Router?

The **CollectiVAI Router** is the backend layer behind the CollectiVAI app’s chat experience.

Instead of talking directly to one model, the app sends every request to **one router endpoint**.  
The router then decides:

- **which provider** to use  
  (`OpenAI`, `Gemini`, `Mistral`, `Meta`, `DeepSeek`, or **Auto**)
- **which model** to call for that provider  
- **how to apply safety & ethics filters** based on:
  - **Mode** (ethical / research / technical)
  - **Topic** (democracy, climate, economy, security, research, health)
  - **Service profile** (city services, universities, NGOs, citizen advisor, startups)

The router is designed as a **human-centered control layer**:
you can swap providers or keys on the backend without changing the app.

---

## 2. Relationship to the CollectiVAI App

The SwiftUI app talks to a single HTTP endpoint using this struct:

```swift
struct CollectivAIBackend {
    static let endpoint =
      URL(string: "https://collectivai-server.collectivai.workers.dev/api/chat")!

    struct ChatRequest: Encodable {
        let prompt: String
        let mode: String
        let provider: String
        let topic: String
        let modelId: String?
        let serviceProfile: String?
    }

    struct RoutingInfo: Decodable {
        let reason: String?
        let filters: [String]?
        let latencyMs: Int?
    }

    struct ChatResponse: Decodable {
        let reply: String
        let providerUsed: String
        let model: String
        let routingInfo: RoutingInfo?
    }

    // ...
}
