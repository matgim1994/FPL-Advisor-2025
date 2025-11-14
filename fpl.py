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


def main():
    pgconfig = get_pg_config()
    dbhandler = DBHandler(pgconfig=pgconfig)
    dbthandler = DBTHandler()

    parser = argparse.ArgumentParser(
        description=(
            "This is a CLI for backend of the FPL Advisor app.\n"
            "You can use it to setup your db, update it, prune old data,\n"
            "run Django REST API or even schedule db updates for the future.\n"
            "Checkout possible actions in the description below."
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
        help="""Use this flag to fetch fresh data to raw tables."""
    )

    parser.add_argument(
        '-rd',
        '--run-dbt',
        action="store_true",
        help="Use this flag to run dbt transformations and tests."
    )
    args = parser.parse_args()

    if args.first_setup:
        first_setup(dbhandler=dbhandler, dbthandler=dbthandler)
    elif args.update_raw:
        dbhandler.update_raw()
    elif args.run_dbt:
        run_dbt(dbthandler=dbthandler)
    else:
        print("Script used without specified command. Run -h to checkout possibilities.")


if __name__ == '__main__':
    main()
