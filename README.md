<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="400" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Human-centred AI routing backend for the CollectiVAI App</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Project-CollectiVAI-003399?style=flat" alt="CollectiVAI" />
  <img src="https://img.shields.io/badge/Status-Prototype-ffcc00?style=flat" alt="Prototype" />
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

---

## 🧠 What is this?

The **CollectiVAI Router** is the backend for the **CollectiVAI App** (iOS / iPadOS / macOS).

It receives structured requests from the app – including:

- selected **provider** (OpenAI, Gemini, Mistral, Meta, DeepSeek, Auto)  
- **mode** (Ethical / Research / Technical)  
- **topic** (Democracy, Climate, Economy, Security, Research, Health)  
- **service profile** (Cities, Universities, NGOs, Citizens, Startups)  
- optional **model ID**

and returns:

- the **final answer text**  
- which **provider/model** was actually used  
- **routing meta data** for the live monitoring sidebar (latency, filters, reason)

The idea:  
> You keep **full control** of your API keys and routing logic on the server side,  
> while the CollectiVAI App stays clean, minimal and privacy-friendly.

---

## 🧩 Relation to the CollectiVAI App

The SwiftUI app (CollectiVAI) talks to a single HTTP endpoint:

```swift
struct CollectivAIBackend {
    static let endpoint = URL(string: "https://collectivai-server.collectivai.workers.dev/api/chat")!
    // ...
}
