# CollectiVAI Router – Security Notes

This document explains security assumptions and recommendations for the
`collectiv-ai-router` project.

## 1. Secrets & API keys

- **Never** commit a real `.env` file to GitHub.
- Store **all provider API keys** (OpenAI, Gemini, Mistral, Meta, DeepSeek, …)
  in your deployment platform's secret storage (e.g. Cloudflare environment
  variables, GitHub Actions secrets, etc.).
- The file `.env.example` is only a template and MUST NOT contain real secrets.

If you accidentally pushed a real `.env` file to a public repo:

1. **Immediately rotate** all affected API keys (OpenAI, Gemini, Mistral, …).
2. Remove the file from the repo and commit history if possible.
3. Add `.env` to `.gitignore` (already present in this template).

## 2. Logging & data protection

- Be careful not to log full prompts, answers or personal data.
- Prefer structured, **minimal** logging:
  - timestamp
  - provider / model
  - latency and status
- If logs contain user data, treat them as confidential and store them securely.
- If you operate this router in the EU or process EU citizen data, you must
  ensure compliance with GDPR (data minimisation, retention limits, right to
  erasure, etc.).

## 3. CORS & origins

- Restrict `ROUTER_ALLOWED_ORIGINS` to your real frontends  
  (e.g. the CollectiVAI iOS/macOS app, website, or staging domains).
- Do **not** use `*` in production.

## 4. Rate limiting & abuse protection

In production you should add:

- basic rate limiting (per IP / per API key),
- request size limits,
- simple anomaly detection (too many errors, too many tokens, etc.).

These are not included in this minimal reference implementation.

## 5. Custom providers

The `custom` provider is a **placeholder**.  
Only enable/implement it if you:

- control the target backend, and
- understand the security, logging and privacy implications.

By default, the example implementation returns a clear error  
(e.g. `"Custom provider is not configured in this public demo."`)  
if it is selected.

## 6. Transport security & authentication

- Always deploy the router **behind HTTPS** (e.g. via Cloudflare, Nginx, Traefik).
- The reference implementation does **not** include authentication or API keys.
  In production you should:
  - protect the router with authentication (e.g. JWT, API key, OAuth, mTLS), or
  - **restrict access** to trusted networks / IP ranges only.
- Never expose a development or demo deployment directly to the public internet
  without proper access control.

---

© 2025 CollectiVAI – This file is non-confidential documentation.
