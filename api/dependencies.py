import logging
from .db import connection_pool

logger = logging.getLogger('api')


def get_pg_conn():
    """Function to get a new PostgreSQL connection from the pool."""

    try:
        conn = connection_pool.getconn()
        if conn.closed == 0:
            logger.info("Successfully retrieved connection from pool.")
            yield conn
        else:
            logger.error("Failed to retrieve connection from pool.")
            raise Exception("No connection available in the pool.")
    except Exception as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise e
    finally:
        if conn:
            connection_pool.putconn(conn)
            logger.info("Connection returned to pool.")
