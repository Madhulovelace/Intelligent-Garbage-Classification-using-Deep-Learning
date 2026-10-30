# Intelligent Garbage Classification

Flask application classifying an image into cardboard, glass, metal, paper, plastic, or trash.

## Layout
```
Project Files/
  app.py
  Garbage1.h5
  requirements.txt
  Garbage Classification/
    templates/
    static/
```

## Run locally
Use Python 3.10 or 3.11. From the repository root:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r "Project Files/requirements.txt"
python "Project Files/app.py"
```

Open http://127.0.0.1:8000. Upload a JPG, JPEG, PNG, or WEBP image up to 8 MB. Images are processed in memory, not saved to disk.

Inference resizes images to 128x128 RGB and scales pixels to [0, 1], matching the training notebook's rescale=1./255 setting. Class order is cardboard, glass, metal, paper, plastic, trash.

## Security
Never commit Kaggle API credentials or other secrets. Revoke and rotate any Kaggle API key previously committed to this repository. The Flask development server is for local testing only; configure a secure secret key and production WSGI server before deployment.
