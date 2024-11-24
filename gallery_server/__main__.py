"""Run gallery server."""

import os

from . import app

if __name__ == "__main__":
    if os.environ.get("FLASK_ENV") == "production":
        # This is only a requirement when running in production mode, has to be installed explicitly
        from waitress import serve  # type: ignore

        serve(app, host="0.0.0.0", port=8080)
    else:
        app.run(debug=True, port=8080)
