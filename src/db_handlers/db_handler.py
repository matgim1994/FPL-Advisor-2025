import psycopg2
import requests
import pandas as pd

from src.models.pg_config import PGConfig
from src.CONSTANS import MAIN_API


class DBHandler:

    def __init__(self, pgconfig: PGConfig):
        self._pg_config = pgconfig
        self._pg_conn = self._setup_connection()

    def _setup_connection(self):
        conn = psycopg2.connect(
            host=self._pg_config.host,
            dbname=self._pg_config.dbname,
            user=self._pg_config.user,
            password=self._pg_config.password,
            port=self._pg_config.port
        )
        return conn

    def api_call(self, api: str):
        """Function makes an api call to given url.

        Args:
            api (str): api URL

        Returns:
            list[dict]: api result"""

        api_result = requests.get(api).json()
        return api_result

    def update_events(self):
        api_result = self.api_call(MAIN_API)
        df_events = pd.json_normalize(api_result['events'])
        return df_events
