import json
import os
from pathlib import Path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent


def get_variables_list():

    secret_file = os.path.join(BASE_DIR, "secrets.json")
    with open(secret_file) as f:
        secrets = json.loads(f.read())

    return secrets
