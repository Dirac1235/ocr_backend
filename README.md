# ID OCR Backend (FastAPI)

This project provides a small FastAPI-based backend service for extracting text from images (ID documents) and for checking image quality (blur detection) before running OCR.

Key features

- HTTP API built with FastAPI
- Image-quality check endpoint to detect blurry images
- OCR extraction using Tesseract via the `pytesseract` Python wrapper

## Quick overview

Routes (prefix `/api/v1`):

- `POST /api/v1/extract-id` — Upload an image (JPEG/PNG). Returns extracted text and metadata.
- `POST /api/v1/check-blur` — Upload an image to receive a simple image-quality score (whether the image is clear enough for OCR).

## Prerequisites (what to install on your machine)

1. Python 3.10+ (the repo contains a virtual environment named `env`; you can use it or create a fresh venv).
2. System Tesseract OCR engine (pytesseract requires the `tesseract` executable).

   - macOS (Homebrew):

     ```bash
     brew install tesseract
     ```

   - Ubuntu / Debian:

     ```bash
     sudo apt update
     sudo apt install -y tesseract-ocr libtesseract-dev
     ```

   - Other platforms: see https://github.com/tesseract-ocr/tesseract for platform-specific instructions.

3. (Optional) If you use custom language data, ensure the TESSDATA_PREFIX environment variable points to the tessdata folder.

## Install Python dependencies

1. Create and activate a virtual environment (recommended). On macOS / zsh:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

   If this repository already contains a prepared `env/` (virtual environment), you can activate it instead:

   ```bash
   source env/bin/activate
   ```

2. Install Python packages:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

- By default the app expects the Tesseract binary to be available on PATH. If tesseract is installed in a non-standard location, set `TESSDATA_PREFIX` or ensure the binary is on PATH.

## Run the app (development)


Using the FastAPI development runner (if you have the `fastapi` CLI installed) — this provides similar live-reload behavior:

```bash
fastapi dev app/main.py
```

After starting the server, the API will be available at http://127.0.0.1:8000.

FastAPI includes interactive API documentation you can use to test and play with the endpoints:

- Open the Swagger UI at: http://127.0.0.1:8000/docs
- Open the ReDoc UI at: http://127.0.0.1:8000/redoc

From the Swagger UI (`/docs`) you can upload image files to the `POST /api/v1/extract-id` and `POST /api/v1/check-blur` endpoints, view the response, and iterate quickly without needing curl.

## Project layout (important files)

- `app/main.py` — FastAPI app and router registration
- `app/api/routes.py` — API endpoints (/extract-id, /check-blur)
- `app/services/ocr_engine.py` — OCR integration (pytesseract usage)
- `app/services/image_utils.py` — Image quality / blur detection
- `requirements.txt` — Python dependencies

## Troubleshooting

- If you get errors about `tesseract` not found, ensure the tesseract binary is installed and on your PATH.
- If OCR output is empty or poor, check that the image is clear using `/api/v1/check-blur` and try different lighting or resolution.

## Contributing

Contributions are welcome. Please open issues or submit pull requests. Keep changes small and add tests if you add functionality.

---
