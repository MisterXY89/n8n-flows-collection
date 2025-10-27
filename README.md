# n8n Flows Collection

Reusable workflows for [n8n](https://n8n.io) — practical automations for text extraction, OCR, and app integrations.

## Contents
- OCR and categorize grocery receipts from Telegram using Gemini, store structured data in NocoDB.
- Generate blog-ready content with optional web research and formatting automation.
- more to come ..


## Use
1. Clone repo → `git clone https://github.com/yourname/n8n-flows-collection.git`
2. In n8n → *Workflows → Import from File* → select a `.json`.
3. Adjust credentials (Telegram, Notion, OpenRouter).

## Structure
- `workflows/` → n8n exports
- `docs/` → short guides & diagrams
- `assets/` → previews & screenshots

## Hosting
Use Coolify to run the stack (n8n, NocoDB, DB) on a single VPS with TLS and Git-based deploys.

## Contribute
Add flow under `/workflows` and a one-line entry in `/docs/overview.md`.

## License
MIT [LICENSE](LICENSE) 2025 Tilman Kerl.
