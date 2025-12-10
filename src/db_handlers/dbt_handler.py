import subprocess
from src.db_handlers.db_handler import DBHandler
from src.logger import get_logger


class DBTHandler(DBHandler):

    def __init__(self):
        self._logger = get_logger(logger_name='db_handler')
        self.dbt_path = './fpl_dbt'

    def run_dbt_snapshot(self):
        """Function runs dbt snapshot command."""

        self._logger.info("Running dbt snapshot command...")
        self._execute_command(['dbt', 'snapshot', '--project-dir', self.dbt_path])

    def run_dbt_models(self):
        """Function runs dbt run command."""

        self._logger.info("Running dbt run command...")
        self._execute_command(['dbt', 'run', '--project-dir', self.dbt_path])

    def run_dbt_tests(self):
        """Function runs dbt tests..."""

        self._logger.info("Running dbt tests...")
        self._execute_command(['dbt', 'test', '--project-dir', self.dbt_path])

    def _execute_command(self, command_parts: list[str]) -> None:
        """Function used to run terminal commands via python.

        Args:
            command_parts(list[str]): command you would like to run
        Raises:
            Exception: if there is an issue with the given command."""

        try:
            result = subprocess.run(
                command_parts,
                check=True,
                capture_output=False,
                text=True
            )
            if result.stdout:
                for line in result.stdout.splitlines():
                    self._logger.info(line)
            self._logger.info(f"dbt {' '.join(command_parts[1:])} ran successfully.")

        except subprocess.CalledProcessError as e:
            self._logger.error(f"dbt {' '.join(command_parts[1:])} returned error (code: {e.returncode}).")
            self._logger.error(f'Error details: {e.stderr}')
            raise e
