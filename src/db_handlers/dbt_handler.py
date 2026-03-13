import subprocess
from src.db_handlers.db_handler import DBHandler
from src.logger import get_logger, setup_dbt_logger
from src.CONSTANS import PROJECT_ROOT


class DBTHandler(DBHandler):

    def __init__(self):
        setup_dbt_logger()
        self._logger = get_logger(logger_name='dbt')
        self.dbt_path = str(PROJECT_ROOT / 'fpl_dbt')

    def run_dbt_snapshot(self):
        """Function runs dbt snapshot command."""

        self._logger.info("Running dbt snapshot command...")
        self._execute_command(['dbt', 'snapshot', '--project-dir', self.dbt_path, '--profiles-dir', self.dbt_path, '--no-use-colors'])

    def run_dbt_models(self):
        """Function runs dbt run command."""

        self._logger.info("Running dbt run command...")
        self._execute_command(['dbt', 'run', '--project-dir', self.dbt_path, '--profiles-dir', self.dbt_path, '--no-use-colors'])

    def run_dbt_tests(self):
        """Function runs dbt tests..."""

        self._logger.info("Running dbt tests...")
        self._execute_command(['dbt', 'test', '--project-dir', self.dbt_path, '--profiles-dir', self.dbt_path, '--no-use-colors'])

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
                capture_output=True,
                text=True
            )
            if result.stdout:
                for line in result.stdout.splitlines():
                    self._logger.info(line)
            self._logger.info(f"dbt {' '.join(command_parts[1:])} ran successfully.")

        except subprocess.CalledProcessError as e:
            self._logger.error(f"dbt {' '.join(command_parts[1:])} returned error (code: {e.returncode}).")
            if e.stdout:
                for line in e.stdout.splitlines():
                    self._logger.error(line)
            if e.stderr:
                for line in e.stderr.splitlines():
                    self._logger.error(line)
            raise e
