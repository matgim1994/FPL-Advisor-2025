from src.logger import setup_api_logger, get_logger
from fastapi import FastAPI, Depends, HTTPException
from .dependencies import get_pg_conn
from psycopg2.extras import RealDictCursor

setup_api_logger()
logger = get_logger('api')
app = FastAPI(title="FPL Advisor API", version="1.0.0")


@app.get("/goalkeepers")
def get_goalkeepers(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all goalkeepers data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.goalkeepers;")
            elements = cursor.fetchall()
            logger.info("Fetched goalkeepers data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching goalkeepers data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/defenders")
def get_defenders(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all defenders data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.defenders;")
            elements = cursor.fetchall()
            logger.info("Fetched defenders data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching defenders data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/midfielders")
def get_midfielders(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all midfielders data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.midfielders;")
            elements = cursor.fetchall()
            logger.info("Fetched midfielders data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching midfielders data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/forwards")
def get_forwards(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all forwards data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.forwards;")
            elements = cursor.fetchall()
            logger.info("Fetched forwards data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching forwards data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
