import psycopg2
import logging
from src.pg_config import get_pg_config
from psycopg2 import pool

logger = logging.getLogger('api')
pg_config = get_pg_config()

try:
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        host=pg_config.host,
        dbname=pg_config.dbname,
        user=pg_config.user,
        password=pg_config.password,
        port=pg_config.port
    )
except Exception as e:
    logger.error(f"Error creating connection pool: {e}")
    raise e
