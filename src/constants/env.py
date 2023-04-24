import os
from dotenv import load_dotenv

load_dotenv(".env")

dev = os.environ.get("ENV") != "production"


def is_dev() -> bool:
    return dev


def set_dev(new_dev: bool) -> bool:
    global dev
    dev = new_dev
