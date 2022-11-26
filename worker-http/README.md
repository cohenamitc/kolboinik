# Kolboinik - HTTP worker

## Description

Receiving a message from the queue with HTTP task configuration and makes the HTTP request

### YAML

```yaml
version: 0
kind: http
metadata: {}
inputs:
  targetUrl: 'https://microsoft.com'
  headers: {}
  method: 'GET'
```

### JSON

```json
{
    "inputs": {
        "headers": {},
        "method": "GET",
        "targetUrl": "https://microsoft.com"
    },
    "kind": "http",
    "metadata": {},
    "version": 0
}
```

## Run the app

```bash
 python src/main.py
```
