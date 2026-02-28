import os

from src.models.pg_config import PGConfig
from dotenv import load_dotenv


def load_environment():
    env = os.getenv("FPL_ENV", "dev")
    dotenv_path = f'./config/{env}/.env'

    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"Environment file not found: {dotenv_path}")

    load_dotenv(dotenv_path)


def get_pg_config():
    load_environment()
    pgconfig = PGConfig(
        host=os.getenv("FPL_PG_HOST"),
        dbname=os.getenv("FPL_PG_DB"),
        user=os.getenv("FPL_PG_USER"),
        password=os.getenv("FPL_PG_PASS"),
        port=os.getenv("FPL_PG_PORT_INTERNAL")
    )
    return pgconfig
