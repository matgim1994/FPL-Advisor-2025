import psycopg2
import requests
import json
from datetime import datetime, timezone
from src.models.pg_config import PGConfig
from src.models.event import Event
from src.models.element import Element
from src.models.team import Team
from src.models.fixture import Fixture
from src.models.player_history import PlayerHistory
from src.models.player_upcoming_fixtures import PlayerFixtures
from src.models.points_explain import PointsExplain
from src.logger import get_logger, setup_dbhandler_logger
from src.CONSTANS import MAIN_API, FIXTURES_API, PLAYER_API, PERFORMANCE_GW_API


class DBHandler:

    def __init__(self, pgconfig: PGConfig):
        setup_dbhandler_logger()
        self._logger = get_logger(logger_name='db_handler')
        self._pg_config = pgconfig
        self._pg_conn = self._setup_connection()

    def update_raw(self) -> None:
        """Function runs all of the upload methods that update raw schema."""

        self.update_teams()
        self.update_elements()
        self.update_events()
        self.update_fixtures()
        self.update_players_history()
        self.update_players_fixtures()
        self.update_points_explain()

    def _setup_connection(self):
        conn = psycopg2.connect(
            host=self._pg_config.host,
            dbname=self._pg_config.dbname,
            user=self._pg_config.user,
            password=self._pg_config.password,
            port=self._pg_config.port
        )
        return conn

    def _api_call(self, api: str):
        """Function makes an api call to given url.

        Args:
            api (str): api URL

        Returns:
            list[dict]: api result

        Raises:
            Exception: in case of an error during api call"""

        try:
            self._logger.info('Starting API call...')
            api_result = requests.get(api).json()
            self._logger.info('API call returned corectly.')
            return api_result
        except Exception as e:
            self._logger.error(f'Error occured during api call: {e}. Raising error.')
            self._pg_conn.close()
            raise e

    def _api_session(self) -> requests.sessions.Session:
        """Function creates api session.

        Returns:
            session(requests.sessions.Session): api session
        Raises:
            Exception: when there is an error with session creation."""

        try:
            self._logger.info('Creating API session.')
            session = requests.Session()
            session.headers.update({'User-Agent': 'FPL2025'})
            return session
        except Exception as e:
            self._logger.error(f'Error occured during api session creation: {e}. Raising error.')
            self._pg_conn.close()
            raise e

    def _serialize_arrays(self, record: dict) -> list:
        """Function seralizes dicts and lists before making an insert on database.

        Args:
            record (dict): one record mented to be written to db.

        Returns:
            record (dict): record with serialized values."""

        for key, value in record.items():
            if isinstance(value, (dict, list)):
                record[key] = json.dumps(value)

        return record

    def update_events(self) -> None:
        """Function updates the raw data for raw.events table.

        Raises:
            Exception: when data from API does not match Events model requirements."""

        self._logger.info('raw.events table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(Event.model_fields.keys())
        api_result = self._api_call(MAIN_API)

        try:
            self._logger.info('Validating events fields returned by API...')
            events = [Event.model_validate(event) for event in api_result['events']]
            self._logger.info('Events fields are correct.')
        except Exception as e:
            self._logger.error(f'An error occured during events fields validation: {e}. Raising error.')
            self._pg_conn.close()
            raise e

        self._upload_raw_data(schema='raw', table_name='events',
                              records=events, columns=columns, ingestion_time=ingestion_time)

    def update_elements(self):
        """Function updates the raw data for raw.elements table.

        Raises:
            Exception: when data from API does not match Element model requirements."""

        self._logger.info('raw.elements table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(Element.model_fields.keys())
        api_result = self._api_call(MAIN_API)

        try:
            self._logger.info('Validating elements fields returned by API...')
            elements = [Element.model_validate(element) for element in api_result['elements']]
            self._logger.info('Elements fields are correct.')
        except Exception as e:
            self._logger.error(f'An error occured during elements fields validation: {e}. Raising error.')
            self._pg_conn.close()
            raise e

        self._upload_raw_data(schema='raw', table_name='elements',
                              records=elements, columns=columns, ingestion_time=ingestion_time)

    def update_teams(self):
        """Function updates the raw data for raw.teams table.

        Raises:
            Exception: when data from API does not match Team model requirements."""

        self._logger.info('raw.teams table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(Team.model_fields.keys())
        api_result = self._api_call(MAIN_API)

        try:
            self._logger.info('Validating teams fields returned by API...')
            teams = [Team.model_validate(element) for element in api_result['teams']]
            self._logger.info('Teams fields are correct.')
        except Exception as e:
            self._logger.error(f'An error occured during teams fields validation: {e}. Raising error.')
            self._pg_conn.close()
            raise e

        self._upload_raw_data(schema='raw', table_name='teams',
                              records=teams, columns=columns, ingestion_time=ingestion_time)

    def update_fixtures(self):
        """Function updates the raw data for raw.fixtures table.

        Raises:
            Exception: when data from API does not match Fixture model requirements."""

        self._logger.info('raw.fixtures table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(Fixture.model_fields.keys())
        api_result = self._api_call(FIXTURES_API)

        try:
            self._logger.info('Validating fixtures fields returned by API...')
            fixtures = [Fixture.model_validate(element) for element in api_result]
            self._logger.info('Teams fields are correct.')
        except Exception as e:
            self._logger.error(f'An error occured during teams fields validation: {e}. Raising error.')
            self._pg_conn.close()
            raise e

        self._upload_raw_data(schema='raw', table_name='fixtures',
                              records=fixtures, columns=columns, ingestion_time=ingestion_time)

    def update_players_history(self):
        """Function updates the raw data for raw.players_history table.

        Raises:
            Exception: when data from API does not match PlayersHistory model requirements."""

        self._logger.info('raw.players_history table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(PlayerHistory.model_fields.keys())
        players_ids = self._get_players_ids()
        _api_session = self._api_session()

        for player_id in players_ids:
            api_result = _api_session.get(PLAYER_API + str(player_id)).json()
            api_result = api_result['history']

            try:
                self._logger.info(f'Validating player {player_id} history fields returned by API...')
                history = [PlayerHistory.model_validate(element) for element in api_result]
                self._logger.info(f'Players {player_id} history fields are correct.')
            except Exception as e:
                self._logger.error(f'An error occured during player {player_id} ' +
                                   f'history fields validation: {e}. Raising error.')
                self._pg_conn.close()
                raise e

            self._upload_raw_data(schema='raw', table_name='players_history',
                                  records=history, columns=columns, ingestion_time=ingestion_time)

    def update_players_fixtures(self):
        """Function updates the raw data for raw.players_upcoming_fixtures table.

        Raises:
            Exception: when data from API does not match PlayersHistory model requirements."""

        self._logger.info('raw.players_upcoming_fixtures table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(PlayerFixtures.model_fields.keys())
        players_ids = self._get_players_ids()
        _api_session = self._api_session()

        for player_id in players_ids:
            api_result = _api_session.get(PLAYER_API + str(player_id)).json()
            api_result = api_result['fixtures']
            for fixture in api_result:
                fixture['element'] = player_id

            try:
                self._logger.info(f'Validating player {player_id} upcoming fixtures fields returned by API...')
                player_fixtures = [PlayerFixtures.model_validate(element) for element in api_result]
                self._logger.info(f'Players {player_id} upcoming fixtures fields are correct.')
            except Exception as e:
                self._logger.error(f'An error occured during player {player_id} ' +
                                   f'upcoming fixtures fields validation: {e}. Raising error.')
                self._pg_conn.close()
                raise e

            self._upload_raw_data(schema='raw', table_name='players_fixtures',
                                  records=player_fixtures, columns=columns, ingestion_time=ingestion_time)

    def update_points_explain(self):
        """Function updates the raw data for raw.points_explain table.

        Raises:
            Exception: when data from API does not match PerformanceGW model requirements."""

        self._logger.info('raw.points_explain table update starting...')
        ingestion_time = datetime.now(timezone.utc)
        columns = list(PointsExplain.model_fields.keys())
        gw_ids = self._get_started_events()
        _api_session = self._api_session()

        for gw_id in gw_ids:
            api_result = _api_session.get(PERFORMANCE_GW_API+f'{gw_id}/live').json()
            api_result = api_result['elements']
            for element in api_result:
                for stat in element['explain'][0]['stats']:
                    stat['id'] = element['id']
                    stat['fixture'] = element['explain'][0]['fixture']
                try:
                    self._logger.info(f"Validating points explain values for player {stat['id']} " +
                                      f"in fixture {element['explain'][0]['fixture']} returned by API...")
                    explain = [PointsExplain.model_validate(stat) for stat in element['explain'][0]['stats']]
                    self._logger.info(f"Points explain fields for {stat['id']} "
                                      + f"in fixture {stat['fixture']} are correct.")
                except Exception as e:
                    self._logger.error(f"An error occured during points explain for {stat['id']} " +
                                       f"in fixture {stat['fixture']} fields validation: {e}. Raising error.")
                    self._pg_conn.close()
                    raise e

                self._upload_raw_data(schema='raw', table_name='points_explain',
                                      records=explain, columns=columns, ingestion_time=ingestion_time)

    def _upload_raw_data(self, schema: str, table_name: str, records: list,
                         columns: list, ingestion_time: datetime) -> None:
        """Function uploads raw data from API to given table in given schema.

        Args:
            schema (str): destination table schema
            table_name (str): destination table name
            records (list): list of dicts where single dict is a single record
            columns (list): list of columns in the destination table
            ingestion_time(datetime): time of data ingestion

        Raises:
            Exception: when there is an issue during data upload
        """

        try:
            self._logger.info(f'Starting data ingestion to {schema}.{table_name} table...')
            bind_values = []
            for record in records:
                record.ingestion_time = ingestion_time
                event_dict = record.model_dump()
                values = [json.dumps(event_dict[c]) if isinstance(event_dict[c], (dict, list))
                          else event_dict[c] for c in columns]
                values_tuple = tuple(values)
                bind_values.append(values_tuple)

            columns_str = ', '.join(f'"{c}"' for c in columns)
            placeholders = ', '.join(['%s'] * len(columns))
            sql_insert = f"""insert into {schema}.{table_name}({columns_str}) values({placeholders})"""
            with self._pg_conn.cursor() as cursor:
                cursor.executemany(sql_insert, bind_values)
                self._pg_conn.commit()
            self._logger.info(f'Data ingested to {schema}.{table_name} table successfully.')
        except Exception as e:
            self._logger.info(f'An error occured during data ingestion to {schema}.{table_name}: {e}. Raising error.')
            self._pg_conn.close()
            raise e

    def _get_players_ids(self) -> list[int]:
        """Function returns latests players ids.

        Returns:
            players_ids(list[int]): players ids in ascending order
        Raises:
            Exception: when there is an issue with selecting the data."""

        try:
            self._logger.info('Selecting most up to date list of players ids...')
            sql_select = """select id from raw.elements
                            where ingestion_time =
                                (select max(ingestion_time)
                                from raw.elements)
                            order by id asc"""
            with self._pg_conn.cursor() as cursor:
                cursor.execute(sql_select)
                players_ids = [result[0] for result in cursor.fetchall()]
            if len(players_ids) < 746:
                self._logger.warning("Number of players is lower that 746 (starting ammount). "
                                     "If necessary check latest players list.")
            return players_ids
        except Exception as e:
            self._logger.info(f'An error occured during selecting player ids: {e}. Raising error.')
            self._pg_conn.close()
            raise e

    def _get_started_events(self) -> list[int]:
        """Function returns ids of GW that already have started.

        Returns:
            gw_ids(list[int]): gw ids in ascending order
        Raises:
            Exception: when there is an issue with selecting the data."""
        try:
            self._logger.info('Selecting ids of GW that already have started...')
            sql_select = """select id from raw.events
                            where finished is true
                            or is_current is true
                            order by id asc"""
            with self._pg_conn.cursor() as cursor:
                cursor.execute(sql_select)
                gw_ids = [result[0] for result in cursor.fetchall()]
            return gw_ids
        except Exception as e:
            self._logger.info(f'An error occured during selecting gw ids: {e}. Raising error.')
            self._pg_conn.close()
            raise e
