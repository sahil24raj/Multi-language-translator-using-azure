# Setup Guide

This guide explains how to run the application locally on Windows and how to provide Azure Translator credentials.

## Prerequisites

- Python 3.9+
- Internet connectivity
- Azure Translator resource with:
  - Endpoint URL
  - Subscription key
  - Region value (for many Azure resources)

## Local Run Steps (Windows)

1. Open terminal in project root.
1. Start backend server:

```powershell
py backend.py
```

1. Open browser and visit:

```text
http://127.0.0.1:5000
```

1. In the form, provide:
   - Azure Endpoint
   - Azure Translator Key
   - Region
1. Enter source text and click Translate to 5 Languages.

## How to Stop Server

- In terminal where backend is running, press Ctrl + C.

## Notes

- Do not open /translate directly in browser; it is an API endpoint.
- Open only root URL / for UI.
- The backend serves index.html directly, so no extra web server is needed.

## Common Endpoint Example

```text
https://api.cognitive.microsofttranslator.com
```

## If py command does not work

Try:

```powershell
python backend.py
```

or

```powershell
python3 backend.py
```
