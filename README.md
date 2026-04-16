# Multi-language-translator-using-azure

A lightweight multi-language translator app built with:

- Frontend: single HTML file with embedded CSS and JavaScript
- Backend: Python/Node.js based backend for Vercel deployment
- Cloud service: Azure AI Translator Text API

The application lets you paste text once and get translations in selected languages at the same time.

## Features

- Single-page UI with dynamic frontend
- Translate one input into your chosen custom selection of languages in one request
- User enters Azure endpoint, key, and region directly in UI
- No external frontend or backend dependencies required
- Basic error handling for invalid JSON, API failures, and connectivity issues

Supported languages out of the box:

- Spanish (es), French (fr), German (de), Hindi (hi), Arabic (ar), 
- Italian (it), Japanese (ja), Portuguese (pt), Russian (ru), Chinese (zh-Hans),
- Bengali (bn), Korean (ko).

## Project Structure

```text
.
├── backend.py
├── index.html
└── docs
    ├── API.md
    ├── ARCHITECTURE.md
    ├── SETUP.md
    └── TROUBLESHOOTING.md
```

## Quick Start

1. Install Python 3.9 or higher.
1. Open terminal in this project folder.
1. Start backend:

```powershell
py backend.py
```

1. Open browser:

```text
http://127.0.0.1:5000
```

1. In UI, enter:
   - Azure endpoint
   - Azure translator key
   - Region (recommended/usually required)
6. Select 1 or more languages to translate into.
7. Enter source text and click Translate Text.

## Azure Input Format

- Endpoint example: <https://api.cognitive.microsofttranslator.com>
- Key: Azure Translator subscription key
- Region example: eastus

Note: Region is optional in code but many Azure resources require it.

## Runtime Flow

1. Browser loads index page from backend root route.
2. User enters credentials and source text.
3. Frontend sends POST /translate to local backend.
4. Backend forwards request to Azure Translator endpoint.
5. Backend maps Azure response and returns compact JSON to frontend.
6. Frontend renders language cards with translated text.

## Security Note

- This app accepts key and endpoint from frontend input and forwards them to Azure.
- For local/demo usage this is fine.
- For production, use server-side secret management and never expose sensitive credentials in browser forms.

## API Summary

- Local endpoint: POST /translate
- Request JSON fields: endpoint, key, region, text, targets
- Response JSON field: translations

See detailed API reference in docs/API.md.

## Documentation Index

- Setup and run guide: docs/SETUP.md
- API reference: docs/API.md
- System architecture: docs/ARCHITECTURE.md
- Troubleshooting guide: docs/TROUBLESHOOTING.md

## Future Improvements

- Source language selector with auto-detect fallback
- Persist endpoint and region in local storage
- Copy-to-clipboard per translation card
- Better structured error parsing for Azure error bodies
