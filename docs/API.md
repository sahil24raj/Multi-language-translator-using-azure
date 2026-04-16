# API Reference

Base URL (local):

```text
http://127.0.0.1:5000
```

## GET /

Serves the frontend page.

### GET Root Response

- Status: 200
- Content-Type: text/html
- Body: index.html content

## GET /index.html

Serves the same frontend page.

### GET index.html Response

- Status: 200
- Content-Type: text/html

## GET /translate

Not allowed by design for translation.

### OPTIONS Response

- Status: 405
- Body:

```json
{
  "error": "Use POST /translate with a JSON body."
}
```

## POST /translate

Translate one input text into multiple target languages.

### Headers

- Content-Type: application/json

### Request Body

```json
{
  "endpoint": "https://api.cognitive.microsofttranslator.com",
  "key": "<azure-subscription-key>",
  "region": "eastus",
  "text": "Hello, how are you?",
  "targets": ["es", "fr", "de", "hi", "ar"]
}
```

### Required Fields

- endpoint
- key
- text
- targets (non-empty array)

### Success Response

- Status: 200

```json
{
  "translations": {
    "es": "Hola, ¿como estas?",
    "fr": "Bonjour, comment allez-vous?",
    "de": "Hallo, wie geht es dir?",
    "hi": "नमस्ते, आप कैसे हैं?",
    "ar": "مرحبًا، كيف حالك؟"
  }
}
```

### Validation Error

- Status: 400

```json
{
  "error": "endpoint, key, text, and targets are required."
}
```

### Invalid JSON Error

- Status: 400

```json
{
  "error": "Invalid JSON body."
}
```

### Upstream Azure HTTP Error

- Status: Azure status code (for example 401/403/404/429)
- Body: raw details returned by Azure (as string in error field)

### Connectivity Error to Azure

- Status: 502

```json
{
  "error": "Unable to reach Azure endpoint: <reason>"
}
```

### Unexpected Internal Error

- Status: 500

```json
{
  "error": "<internal error message>"
}
```

## CORS

Backend sends permissive CORS headers:

- Access-Control-Allow-Origin: *
- Access-Control-Allow-Headers: Content-Type
- Access-Control-Allow-Methods: POST, OPTIONS

## OPTIONS /translate

Preflight support.

### Response

- Status: 204
