import os
import streamlit as st


def get_db_url() -> str:
    """Build PostgreSQL connection URL from environment variables.

    Uses BI_USER/BI_PASS (read-only role) to connect to the gold schema.
    Fails fast with KeyError if any required var is missing.
    """
    user = os.environ["BI_USER"]
    password = os.environ["BI_PASS"]
    host = os.environ["FPL_PG_HOST"]
    port = os.environ["FPL_PG_PORT"]
    db = os.environ["FPL_PG_DB"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def get_connection():
    """Return a cached Streamlit SQL connection to the gold schema.

    st.connection caches internally — no @st.cache_resource needed.
    """
    return st.connection("fpl_gold", type="sql", url=get_db_url())
