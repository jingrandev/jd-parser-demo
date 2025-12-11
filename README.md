# JD Parser API

FastAPI backend service for JD parsing coding assignment

---

## How to install dependencies

This project uses [uv](https://github.com/astral-sh/uv) to manage the virtual environment and dependencies.

1. **Create / activate the virtual environment and install deps**

   ```bash
   # from the project root
   uv venv --python 3.13 --seed
   uv sync
   ```

   This will create `.venv/` and install all dependencies listed in `pyproject.toml`.

2. **Activate the virtual environment manually**

   ```bash
   source .venv/bin/activate
   ```

---

## How to configure environment

Configuration is managed via Pydantic Settings and a `.env` file.

Create a `.env` file in the project root (if you have not already):

```env
# env
APP_ENV=local

# base
APP_TITLE="JD Parser API (Local)"
DEBUG=true

# llm
OPENAI_API_KEY=your_real_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

---

## How to run the FastAPI server

You can run the app using either `fastapi dev` or `uvicorn`.

### Option 1: fastapi dev (with auto-reload)

```bash
fastapi dev entry.py
```

### Option 2: uvicorn

```bash
uvicorn entry:app --reload
```

By default the API will be served on:

- `http://127.0.0.1:8000`

Health check:

- `GET http://127.0.0.1:8000/api/v1/health`

---

## Example API request

### Endpoint

Parse a job description:

- `POST /api/v1/hr/parse_jd`

### Request body

```json
{
  "text": "We are hiring a backend engineer to design and implement scalable backend services and APIs. You will work closely with product and ML engineers to build and maintain RESTful/GraphQL endpoints, integrate third-party services, and support our AI-powered features. The ideal candidate is comfortable with Python, FastAPI, relational databases, and modern cloud-native dev practices (CI/CD, observability, containers)."
}
```

### Example with `curl`

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/hr/parse_jd" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We are hiring a backend engineer to design and implement scalable backend services and APIs. You will work closely with product and ML engineers to build and maintain RESTful/GraphQL endpoints, integrate third-party services, and support our AI-powered features. The ideal candidate is comfortable with Python, FastAPI, relational databases, and modern cloud-native dev practices (CI/CD, observability, containers)."
  }'
```

### Example response

```json
{
  "role_title": "Backend Engineer",
  "mission": "Design and implement scalable backend services and APIs to support AI-powered features.",
  "core_responsibilities": [
    "Design backend services",
    "Implement APIs",
    "Build RESTful/GraphQL endpoints",
    "Integrate third-party services",
    "Support AI features",
    "Work with product and ML teams"
  ],
  "required_skills": [
    "Python",
    "FastAPI",
    "Relational databases",
    "CI/CD",
    "Observability",
    "Containers"
  ]
}
```

> Note: The exact response depends on the LLM output and prompt. The above is an example of the expected structure.

---

## Running tests
Please make sure to run test and reformat code before commiting.

Run all tests:

```bash
make test
```

### Code Style

```bash
make format
```


## Pre-commit hooks

Additionally, it is highly recommended to install `pre-commit` hooks when developing:

```bash
uv add pre-commit --dev
pre-commit install
```

To manually run pre-commit hooks on all files:

```bash
make check
```

> Not recommended: `git commit --no-verify` will bypass the checks for this commit.
