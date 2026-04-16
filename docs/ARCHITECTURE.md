# Architecture

## Overview

The project is intentionally minimal and uses only two runtime files:

- index.html: complete frontend (HTML + CSS + JavaScript)
- backend.py: complete backend server and Azure API proxy

## Component Diagram

```text
Browser (index.html UI)
    |
    | POST /translate (JSON)
    v
Local Python Server (backend.py)
    |
    | POST {endpoint}/translate?api-version=3.0&to=...
    v
Azure AI Translator
```

## Frontend Responsibilities

- Collect endpoint, key, region, and source text from user
- Trigger translation request
- Display success/error status
- Render translation cards for five languages

## Backend Responsibilities

- Serve frontend HTML at root route
- Validate translation payload
- Build Azure Translator request with required headers
- Forward request to Azure endpoint
- Normalize response into simple key-value translation map
- Return proper HTTP error status and message

## Design Choices

- No framework dependencies: easier setup, good for demos/interviews
- Standard library HTTP server: no external package installation
- Relative API call (/translate): avoids host mismatch issues
- Single request for all target languages: lower latency than one call per language

## Security Considerations

Current model:

- Credentials are typed in browser and sent to local backend.

For production recommendation:

- Keep subscription keys server-side only.
- Use secure secret stores and environment variables.
- Add auth/rate limiting and strict CORS policy.
- Add request logging and monitoring with secret masking.

## Scalability Notes

Current backend uses Python HTTPServer (single-process default) which is enough for local usage.

For higher load:

- Move to production WSGI/ASGI stack (for example FastAPI/Flask with gunicorn/uvicorn).
- Add structured retries for transient Azure errors (429/5xx).
- Cache common translations when appropriate.
