import os

from src.models.pg_config import PGConfig
from dotenv import load_dotenv

load_dotenv()


def get_pg_config():
    pgconfig = PGConfig(
        host=os.getenv("FPL_PG_HOST"),
        dbname=os.getenv("FPL_PG_DB"),
        user=os.getenv("FPL_PG_USER"),
        password=os.getenv("FPL_PG_PASS"),
        port=os.getenv("FPL_PG_PORT_INTERNAL")
    )
    return pgconfig
