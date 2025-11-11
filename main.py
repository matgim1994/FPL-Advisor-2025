import os

from src.db_handlers.db_handler import DBHandler
from src.models.pg_config import PGConfig
from dotenv import load_dotenv

load_dotenv()
pgconfig = PGConfig(
    host=os.getenv("FPL_PG_HOST"),
    dbname=os.getenv("FPL_PG_DB"),
    user=os.getenv("FPL_PG_USER"),
    password=os.getenv("FPL_PG_PASS"),
    port=os.getenv("FPL_PG_PORT")
)
dbhandler = DBHandler(pgconfig=pgconfig)

dbhandler.update_raw()
# dbhandler._execute_sql_script(filepath='./src/db_handlers/sql/teams.sql')
