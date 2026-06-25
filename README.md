# Python Calculator HTTP Server

A lightweight REST API calculator built with Python's built-in `http.server` module. No external dependencies required.

## Requirements

- Python 3

## Usage

### Start the server

```bash
python3 calculator.py
```

The server runs at `http://localhost:5000`.

## Endpoints

| Endpoint | Operation | Example |
|----------|-----------|---------|
| `/add` | Addition | `/add?a=5&b=3` → `8` |
| `/subtract` | Subtraction | `/subtract?a=10&b=4` → `6` |
| `/multiply` | Multiplication | `/multiply?a=6&b=7` → `42` |
| `/divide` | Division | `/divide?a=10&b=2` → `5` |

All endpoints accept two query parameters: `a` and `b`.

## Example Requests

```bash
# Addition
curl "http://localhost:5000/add?a=5&b=3"

# Subtraction
curl "http://localhost:5000/subtract?a=10&b=4"

# Multiplication
curl "http://localhost:5000/multiply?a=6&b=7"

# Division
curl "http://localhost:5000/divide?a=10&b=2"
```

## Example Response

```json
{
    "a": 5,
    "b": 3,
    "operation": "addition",
    "result": 8
}
```

## Error Handling

The server returns descriptive JSON errors for:

**404 — Unknown endpoint**
```json
{
    "error": "Unknown endpoint",
    "available_endpoints": ["/add", "/subtract", "/multiply", "/divide"]
}
```

**400 — Missing parameters**
```json
{
    "error": "Missing query parameters. Provide both 'a' and 'b'.",
    "example": "http://localhost:5000/add?a=5&b=3"
}
```

**400 — Invalid parameters**
```json
{
    "error": "Parameters 'a' and 'b' must be numbers."
}
```

**400 — Division by zero**
```json
{
    "error": "Division by zero is not allowed."
}
```

## Stopping the Server

Press `Ctrl+C` to stop the server gracefully.
