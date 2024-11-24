"""Gallery server."""

import json
import logging
import os
import time

from flask import Flask, jsonify, make_response, request, send_file
from flask_httpauth import HTTPBasicAuth
from PIL import Image
from werkzeug.security import check_password_hash

from .helpers import normalize_timestamp
from .pickers import pick_random_image_by_seed
from .processors import format_image

_LOGGER = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
auth = HTTPBasicAuth()


# Load user credentials from file
def load_users(file_path):
    """Load the users for the basic auth."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ReferenceError("Users could not be loaded for basic auth") from e
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format in users file.") from e


users = load_users("users.json")


@auth.verify_password
def verify_password(username, password):
    """Check for a valid username/password combination."""
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@app.route("/")
def home():
    """Return home."""
    return jsonify(
        {"message": "Welcome to the Image API! Use Basic Auth to access the endpoints."}
    )


@app.route("/random", defaults={"resolution": None}, methods=["GET"])
@app.route("/random/<resolution>", methods=["GET"])
@auth.login_required
def get_image(resolution: str):
    """Route to get a random image based on resolution and query parameters.

    Query Parameters:
    - format: The format of the image (e.g., "jpeg", "png", "bmp").
    - size: The size of the image (e.g., "1024x768").
    - fit: How the image should fit (e.g., "cover", "contain").
    - filter: Any filters to apply (e.g., "grayscale", "sepia", "blur", "dithering").
    - dithering_palette: The palette to use for dithering (e.g., "black-white", "4-color", "n-color").
    """
    try:
        image_format = request.args.get("format", None)
        size = request.args.get("size", None)
        fit = request.args.get("fit", "cover")
        filter = request.args.get("filter", None)
        dithering_palette = request.args.get("dithering_palette", "black-white")

        image_path = pick_random_image_by_seed(
            normalize_timestamp(resolution).isoformat()
            if resolution
            in ["year", "month", "week", "day", "hour", "minute", "second"]
            else None,
        )
        _, image_raw_format = os.path.splitext(image_path)
        format = image_format or image_raw_format[1:].lower()
        format = "jpeg" if format == "jpeg" else format  # fix jpeg vs jpg ambiguity
        with Image.open(image_path) as img:
            img_io = format_image(
                img,
                format,
                size,
                fit,
                filter,
                dithering_palette,
            )
        response = make_response(send_file(img_io, mimetype=f"image/{format}"))
        response.headers[
            "Content-Disposition"
        ] = f"attachment; filename=random_{resolution or '-'}_{int(time.time())}.{format}"
    except Exception as e:
        _LOGGER.warning(e)
        return jsonify({"error": str(e)}), 500
    else:
        return response


__all__ = ["app"]
