# gallery-server

A gallery server for simple frontend devices

Start the server with `python -m gallery_server` or use the docker image.

## Scripts

### User credentials

There is a script to prepare a user credentials file which is required to access the api. Have a look at `./scripts/generate-password-hashes.py`, add your user/password combinations and run the script to create a `users.json` file at the root of the repo. It uses the function `generate_password_hash` from `werkzeug.security` with the `scrypt:32768:8:1` algorithm.

### Dithering test

There is a test script to run simple dithering, which is useful the check how the images look like and to test new palettes. All images in the `media` folder are converted to the `out` folder.

## Dev

Setup the dev environment using VSCode, it is highly recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install [pre-commit](https://pre-commit.com)

```bash
pre-commit install

# Run the commit hooks manually
pre-commit run --all-files
```

Following VSCode integrations may be helpful:

- [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [mypy](https://marketplace.visualstudio.com/items?itemName=matangover.mypy)
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
