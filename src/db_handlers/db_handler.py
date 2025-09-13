import psycopg2
from src.models.pg_config import PGConfig


class DBHandler:

    def __init__(self, pgconfig: PGConfig):
        self._fpl_db_host = pgconfig.host
        self._fpl_db_name = pgconfig.dbname
        self._fpl_db_user = pgconfig.user
        self._fpl_db_pass = pgconfig.password
        self._fpl_db_port = pgconfig.port

    def setup_connection(self):
        print('Proba polaczenia z postgresem')
        conn = psycopg2.connect(
            host=self._fpl_db_host,
            dbname=self._fpl_db_name,
            user=self._fpl_db_user,
            password=self._fpl_db_pass,
            port=self._fpl_db_port
        )
        cursor = conn.cursor()
        sql = 'SELECT * FROM public.test'
        cursor.execute(sql)
        records = cursor.fetchall()
        print("proba udana")
        print(records)
