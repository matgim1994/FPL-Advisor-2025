from src.db_handlers.db_handler import DBHandler
from src.db_handlers.dbt_handler import DBTHandler
from src.pg_config import get_pg_config

pgconfig = get_pg_config()
dbhandler = DBHandler(pgconfig=pgconfig)
dbthandler = DBTHandler()

dbhandler.create_fpl_db_schema()
dbhandler.setup_raw_tables()
dbhandler.update_raw()
dbthandler.run_dbt_models()
dbthandler.run_dbt_tests()
