# resumeAI-API

Backend API for the **resumeAI** project.  
This service processes resume PDFs, extracts text using OCR, and provides AI-powered resume improvement features for the frontend application.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [API Endpoints (Examples)](#api-endpoints-examples)
- [Docker (optional)](#docker-optional)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)
- [Author / Maintainers](#author--maintainers)

---

## Overview

`resumeAI-API` is a Python-based backend service that:

- Extracts text from uploaded resume PDFs
- Uses OCR (Tesseract) for scanned/rescanned documents
- Runs AI-powered resume improvement or parsing workflows
- Exposes REST API endpoints for integration with the frontend

This repository is intended to be paired with the frontend: `https://github.com/ap165/resumeAI`.

---

## Features

- PDF text extraction (native + OCR fallback)
- Support for scanned/rescanned resumes using Tesseract OCR
- Endpoints to process, analyze, and return enhanced resume content
- Simple Flask-based API that is easy to extend

---

## Tech Stack

- Python 3.8+
- Flask (or FastAPI — update as needed)
- pdf2image
- pytesseract (Tesseract OCR Python wrapper)
- Pillow (PIL)
- Poppler (system dependency for `pdf2image`)

---

## Project Structure

```
resumeAI-API
│
├── modules/             # Processing modules (pdf parsing, OCR, utils)
├── tests/               # Unit / integration tests
├── api.py               # Main Flask app (entrypoint)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Optional container file
├── README.md
└── LICENSE
```

---

## Prerequisites

- Python 3.8 or newer
- pip
- System packages:
  - **Poppler** (for `pdf2image`)
  - **Tesseract OCR** (for `pytesseract`)

### Installing Poppler

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install -y poppler-utils
```

**macOS (Homebrew)**
```bash
brew install poppler
```

### Installing Tesseract OCR

**Ubuntu / Debian**
```bash
sudo apt install -y tesseract-ocr
# Optional language packs (English)
sudo apt install -y tesseract-ocr-eng
```

**macOS (Homebrew)**
```bash
brew install tesseract
```

---

## Installation

1. Clone the repository
```bash
git clone https://github.com/ap165/resumeAI-API.git
cd resumeAI-API
```

2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate    # Windows (PowerShell)
```

3. Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root (example variables):

```
FLASK_ENV=development
FLASK_APP=api.py
SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=10485760  # 10 MB upload limit (optional)
```

Adjust values to your environment and secrets management practice (do not commit secrets to git).

---

## Running the API

Local development using Flask:
```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 5000
```

Or run directly with Python:
```bash
python api.py
```

For production, use a WSGI server (Gunicorn) behind a reverse proxy (Nginx) — see the **Deployment** section below.

---

## API Endpoints (Examples)

> These are example routes — update to match your implementation.

### `POST /upload`
Upload a resume PDF for parsing.

Request (multipart/form-data):
- `file` — PDF file

Response (JSON):
```json
{
  "status": "ok",
  "id": "job-id-123",
  "text": "Extracted resume text..."
}
```

### `POST /analyze`
Send raw text or extracted content for AI-powered improvements.

Request (application/json):
```json
{
  "resume_text": "Raw extracted text or pasted resume content",
  "options": { "target_role": "software engineer" }
}
```

Response (application/json):
```json
{
  "status": "ok",
  "improved_text": "Improved resume content..."
}
```

Add authentication, rate-limiting, and size checks as needed.

---

## Docker (optional)

Example `Dockerfile` workflow:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "api:app", "-b", "0.0.0.0:8000", "--workers=4"]
```

Build and run:
```bash
docker build -t resumeai-api:latest .
docker run -p 8000:8000 --env-file .env resumeai-api:latest
```

Note: You still need Poppler and Tesseract available in the image or installed on the host. Consider using a custom base image with these preinstalled.

---

## Testing

If tests exist in `tests/`, run them with pytest:
```bash
pip install -r requirements-dev.txt   # if present
pytest -q
```

Add unit tests for parsing modules and some integration tests for the main endpoints.

---

## Deployment

A common production setup:

- Gunicorn as WSGI server
- Nginx as reverse proxy (TLS termination, static assets)
- Systemd service to manage the Gunicorn process
- S3 (or similar) for storing uploaded/resumed files (optional)
- Use environment variables or secrets manager for configuration

Example systemd service fragment for Gunicorn:
```
[Unit]
Description=Gunicorn instance to serve resumeAI-API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/resumeai-api
EnvironmentFile=/srv/resumeai-api/.env
ExecStart=/srv/resumeai-api/.venv/bin/gunicorn -w 4 -b unix:resumeai.sock -m 007 api:app

[Install]
WantedBy=multi-user.target
```

---

## Contributing

Thanks for considering contributing — your help makes this project better! 🎉

If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a descriptive branch from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
3. Write clear, focused commits. Use present-tense, imperative messages, e.g. `feat: add OCR retry logic`.
4. Add or update tests for your changes.
5. Run tests locally and ensure linting passes.
6. Push your branch and open a Pull Request (PR) against `main`.
7. In the PR description, explain:
   - What you changed and why
   - Any migration or config changes required
   - How to test the change locally
8. Be responsive to review feedback. We'll iterate together.

### Contributor Tips & Guidelines
- Follow the existing project code style; add linting configs if missing.
- Keep changes small and scoped to a single concern.
- Use feature flags or config toggles for potentially risky changes.
- Document new endpoints, environment variables, or config in the README.
- If the change affects the public API, add migration notes and update example requests/responses.
- Add unit tests for new behavior; aim for predictable, deterministic tests (avoid depending on external APIs in unit tests).

---

## Code of Conduct

Please follow a respectful and constructive tone in issues and PRs. If you'd like, I can add a `CODE_OF_CONDUCT.md` template (Contributor Covenant) to the repository.

---

## License

This project is available under the **MIT License**. See `LICENSE` for details.

---

## Author / Maintainers

Built and maintained by **Arijit** (GitHub: `ap165`).  
If you want help improving this README, CI setup, or deployment scripts, I can generate those files for you.

---

*Thank you for contributing — and welcome to the project!*  
