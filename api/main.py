from src.logger import setup_api_logger, get_logger
from fastapi import FastAPI, Depends, HTTPException
from .dependencies import get_pg_conn
from psycopg2.extras import RealDictCursor

setup_api_logger()
logger = get_logger('api')
app = FastAPI(title="FPL Advisor API", version="1.0.0")


@app.get("/players")
def get_players(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all players data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.players;")
            elements = cursor.fetchall()
            logger.info("Fetched players data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching players data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/players/{id}")
def get_player(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific player data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.players where id = %s;", (id,))
            else:
                logger.error("Player ID is required.")
                raise HTTPException(status_code=400, detail="Player ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched player {id} data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching player {id} data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/players_history/{id}")
def get_players_history(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific players history data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.players_history where element = %s;", (id,))
            else:
                logger.error("Player ID is required.")
                raise HTTPException(status_code=400, detail="Player ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched player {id} history data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching player {id} data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/points_explain/{id}/{fixture}")
def get_points_explain(conn=Depends(get_pg_conn), id: int = None, fixture: int = None):
    """Endpoint to retrieve specific players points explanation from given fixture."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id and fixture:
                cursor.execute("select * from gold.points_explain where id = %s and fixture = %s;", (id, fixture))
            else:
                logger.error("Both Player ID and Fixture are required.")
                raise HTTPException(status_code=400, detail="Both Player ID and Fixture are required.")
            elements = cursor.fetchall()

            if len(elements) == 0:
                logger.info(f"No data found for given Player ID {id} and Fixture {fixture}.")
                return
            logger.info(f"Fetched player {id} points explanation for fixture {fixture} successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching player {id} points explanation for fixture {fixture}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/teams")
def get_teams(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve teams data from database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.teams;")
            elements = cursor.fetchall()
            logger.info("Fetched teams data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching teams data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/teams/{id}")
def get_team(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific team data from the database."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.teams where id = %s;", (id,))
            else:
                logger.error("Team ID is required.")
                raise HTTPException(status_code=400, detail="Team ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched team {id} data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching team {id} data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/top_players")
def get_top_players(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve data on top players from each event."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.top_players;")
            elements = cursor.fetchall()
            logger.info("Fetched top players data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching top players data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/top_players/{id}")
def get_gw_top_player(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific top players from given event."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.top_players where event = %s;", (id,))
            else:
                logger.error("Event ID is required.")
                raise HTTPException(status_code=400, detail="Event ID is required.")
            elements = cursor.fetchall()
            if not elements[0]['most_selected']:
                logger.info(f"No top players found for event {id}.")
                return
            logger.info(f"Fetched top players for event {id} successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching top players for event {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/chips_played")
def get_chips_played(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve data on number of chips played in each event."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.chips_played;")
            elements = cursor.fetchall()
            logger.info("Fetched chips played data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching chips played data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/chips_played/{id}")
def get_gw_chips_played(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific chips played from given event."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.chips_played where event = %s;", (id,))
            else:
                logger.error("Event ID is required.")
                raise HTTPException(status_code=400, detail="Event ID is required.")
            elements = cursor.fetchall()
            if not elements[0]['bboost']:
                logger.info(f"No chips played found for event {id}.")
                return
            logger.info(f"Fetched chips played in event {id} successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching chips played in event {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fdr")
def get_fdrs(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve fdr data for each team."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.fdr;")
            elements = cursor.fetchall()
            logger.info("Fetched fdr data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching fdr data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fdr/{id}")
def get_fdr(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve fdr for specific team."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.fdr where id = %s;", (id,))
            else:
                logger.error("Team ID is required.")
                raise HTTPException(status_code=400, detail="Team ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched fdr for team {id} successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching fdr for team {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fixtures")
def get_fixtures(conn=Depends(get_pg_conn)):
    """Endpoint to retrieve all fixtures data."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("select * from gold.fixtures_main;")
            elements = cursor.fetchall()
            logger.info("Fetched fixtures data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching fixtures data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fixtures/{id}")
def get_fixture(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific fixture data."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.fixtures_main where id = %s;", (id,))
            else:
                logger.error("Fixture ID is required.")
                raise HTTPException(status_code=400, detail="Fixture ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched fixture {id} data successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching fixture {id} data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/fixtures/stats/{id}")
def get_fixture_stats(conn=Depends(get_pg_conn), id: int = None):
    """Endpoint to retrieve specific fixture statistics."""

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id:
                cursor.execute("select * from gold.fixtures_stats where fixture = %s;", (id,))
            else:
                logger.error("Fixture ID is required.")
                raise HTTPException(status_code=400, detail="Fixture ID is required.")
            elements = cursor.fetchall()
            logger.info(f"Fetched fixture {id} stats successfully.")
            return elements
    except Exception as e:
        logger.error(f"Error fetching fixture {id} stats: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
