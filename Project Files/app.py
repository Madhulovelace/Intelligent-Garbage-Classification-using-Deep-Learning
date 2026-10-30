"""Flask web application for six-class garbage image classification."""
from pathlib import Path

import numpy as np
from flask import Flask, flash, redirect, render_template, request, url_for
from PIL import Image, UnidentifiedImageError
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "Garbage Classification" / "templates"
STATIC_DIR = BASE_DIR / "Garbage Classification" / "static"
MODEL_PATH = BASE_DIR / "Garbage1.h5"
CLASS_NAMES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
IMAGE_SIZE = (128, 128)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

app = Flask(__name__, template_folder=str(TEMPLATE_DIR), static_folder=str(STATIC_DIR))
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["SECRET_KEY"] = "replace-with-a-random-secret-before-deployment"

if not MODEL_PATH.is_file():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}. Keep Garbage1.h5 beside app.py.")
model = load_model(str(MODEL_PATH), compile=False)


def predict_image(upload):
    if Path(upload.filename or "").suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Upload a JPG, JPEG, PNG, or WEBP image.")
    try:
        with Image.open(upload.stream) as source:
            image = source.convert("RGB").resize(IMAGE_SIZE)
            pixels = np.asarray(image, dtype=np.float32) / 255.0
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc

    output = model.predict(np.expand_dims(pixels, axis=0), verbose=0)
    if output.ndim != 2 or output.shape[1] != len(CLASS_NAMES):
        raise RuntimeError(f"Unexpected model output shape: {output.shape}")
    return CLASS_NAMES[int(np.argmax(output[0]))]


@app.get("/")
@app.get("/index.html")
def index():
    return render_template("index.html")


@app.get("/prediction.html")
def prediction():
    return render_template("prediction.html", prediction=None)


@app.post("/result")
def result():
    upload = request.files.get("image")
    if upload is None or not upload.filename:
        flash("Choose an image before submitting.")
        return redirect(url_for("prediction"))
    try:
        predicted_class = predict_image(upload)
    except ValueError as exc:
        flash(str(exc))
        return redirect(url_for("prediction"))
    return render_template("prediction.html", prediction=predicted_class)


@app.errorhandler(413)
def file_too_large(_error):
    flash("Image is too large. Maximum upload size is 8 MB.")
    return redirect(url_for("prediction"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
