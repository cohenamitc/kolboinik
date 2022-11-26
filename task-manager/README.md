# Kolboinik - Task Manager

## Description

An API endpoint to receive task configurations and put them in queue
Task configuration can be either YAML or JSON formatted

- API endpoint for submitting task configurations `POST /job_config`
- `Content-Type: application/json` / `Content-Type: application/yaml`

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
 python -m flask --app=task-manager/src/app run
```
