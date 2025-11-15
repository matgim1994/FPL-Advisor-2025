import argparse
from src.db_handlers.db_handler import DBHandler
from src.db_handlers.dbt_handler import DBTHandler
from src.pg_config import get_pg_config


def first_setup(dbhandler: DBHandler, dbthandler: DBTHandler):
    dbhandler.create_fpl_db_schema()
    dbhandler.setup_raw_tables()
    dbhandler.update_raw()
    dbthandler.run_dbt_models()
    dbthandler.run_dbt_tests()


def run_dbt(dbthandler: DBTHandler):
    dbthandler.run_dbt_models()
    dbthandler.run_dbt_tests()


def update_raw(dbhandler: DBHandler, dbthandler: DBTHandler):
    dbhandler.create_fpl_db_schema()
    dbhandler.setup_raw_tables()
    dbhandler.update_raw()
    dbthandler.run_dbt_models()
    dbthandler.run_dbt_tests()


def create_dotenv():
    fpl_pg_user = input('Your postgres master user name: ')
    fpl_pg_password = input('Your postgres master user password: ')
    fpl_pg_db = input('Your database name: ')
    fpl_pg_host = input('Your db host (write localhost if working locally): ')
    fpl_pg_port = input('Your database port: ')

    env_vars = {
        "FPL_PG_USER": fpl_pg_user,
        "FPL_PG_PASS": fpl_pg_password,
        "FPL_PG_DB": fpl_pg_db,
        "FPL_PG_HOST": fpl_pg_host,
        "FPL_PG_PORT": fpl_pg_port,
    }

    with open("./.env", "w") as file:
        file.write("\n".join(f"{k}={v.strip()}" for k, v in env_vars.items()))


def main():
    pgconfig = get_pg_config()
    dbhandler = DBHandler(pgconfig=pgconfig)
    dbthandler = DBTHandler()

    parser = argparse.ArgumentParser(
        description=(
            """This is a CLI for backend of the FPL Advisor app.
            You can use it to setup your db, update it, prune old data,
            run Django REST API or even schedule db updates for the future.
            Checkout possible actions in the description below."""
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-fs',
        '--first-setup',
        action='store_true',
        help="""Use this flag to setup raw schema in your db,
                create all necessary raw tables to fetch API data,
                collect all the data from API, run dbt to
                transform fetched data to bronze, silver and gold layers,
                and in the end run dbt test to check if all constrainst are met.
                Takes about 6 minutes."""
    )

    parser.add_argument(
        '-ur',
        '--update-raw',
        action='store_true',
        help="Use this flag to fetch fresh data to raw tables."
    )

    parser.add_argument(
        '-rd',
        '--run-dbt',
        action="store_true",
        help="Use this flag to run dbt transformations and tests."
    )

    parser.add_argument(
        '-cd',
        '--create-dotenv',
        action='store_true',
        help="Use this flag to create dotenv file with postgres credentials."
    )
    args = parser.parse_args()

    if args.first_setup:
        first_setup(dbhandler=dbhandler, dbthandler=dbthandler)
    elif args.update_raw:
        dbhandler.update_raw()
    elif args.run_dbt:
        run_dbt(dbthandler=dbthandler)
    elif args.create_dotenv:
        create_dotenv()
    else:
        print("Script used without specified command. Run -h to checkout possibilities.")


if __name__ == '__main__':
    main()
