# n8n Flows Collection

Reusable workflows for [n8n](https://n8n.io) — practical automations for text extraction, OCR, and app integrations.

## Contents
- OCR and categorize grocery receipts from Telegram using Gemini, store structured data in NocoDB.
- Generate blog-ready content with optional web research and formatting automation.
- more to come ..

## Sanitize Workflows

Before publishing, anonymize all `.json` files in `/workflows` (removes credentials, Notion IDs, model IDs, instance IDs).

Using Make:
- Overwrite in place: `make anon`
- Optional to another folder: `make anon-out OUT=out_workflows`
- Verify no credentials remain: `make check-anon`

Direct Python:
`python3 scripts/anonymize_n8n.py workflows workflows --recursive`

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
