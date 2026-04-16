# Troubleshooting

## 1) This site cannot be reached (127.0.0.1 refused to connect)

Cause:

- backend.py is not running.

Fix:

1. Run server:

```powershell
py backend.py
```

1. Open:

```text
http://127.0.0.1:5000
```

1. Do not open /translate directly in browser.

## 2) Getting 401 or 403 from Azure

Cause:

- Invalid key, wrong endpoint, or wrong region.

Fix:

- Re-check subscription key.
- Ensure endpoint belongs to your translator resource.
- Provide correct region value.

## 3) Getting 404 from Azure

Cause:

- Endpoint path/domain mismatch.

Fix:

- Use base endpoint, for example:

```text
https://api.cognitive.microsofttranslator.com
```

The backend itself appends /translate and query parameters.

## 4) Translation failed with networking error

Cause:

- DNS/proxy/firewall/internet issue.

Fix:

- Check internet connection.
- Verify endpoint can be reached from machine.
- If corporate proxy is required, configure system/proxy settings.

## 5) Nothing appears in translation cards

Cause:

- Azure response did not include expected translations.

Fix:

- Check backend terminal logs for returned errors.
- Verify target language codes are valid.

## 6) py command not recognized

Fix:

Use alternatives:

```powershell
python backend.py
```

or

```powershell
python3 backend.py
```

## 7) Port 5000 already in use

Cause:

- Another process is using port 5000.

Fix options:

- Stop the other process.
- Or change HOST/PORT constants in backend.py and open the new URL.
