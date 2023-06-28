import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from configparser import ConfigParser

import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")


def config(file_name="./ggsheet/db/database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(file_name)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {file_name} file")

    return db


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


def import_csv_to_postgresql(csv_file_path, table_name):
    # Establish a connection to the PostgreSQL database
    # read connection parameters
    params = config()
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Create a new database (if required)
    # cur = conn.cursor()
    # cur.execute(
    #     sql.SQL("CREATE DATABASE {}").format(sql.Identifier(params["database"]))
    # )
    # cur.close()
    # conn.close()

    # Reconnect to the new database
    # conn = psycopg2.connect(**params)

    # Create the table based on the CSV file structure
    cur = conn.cursor()

    with open(csv_file_path, "r") as f:
        header = f.readline().strip()
        columns = [sql.Identifier(column.strip()) for column in header.split(",")]

        logging.debug(header)
        logging.debug(columns)

        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {}({})").format(
            sql.Identifier(table_name), sql.SQL(", ").join(columns)
        )
        logging.debug(create_table_query)
        cur.execute(
            """CREATE TABLE IF NOT EXISTS public.test_gg_sheet(
                No INTEGER,
                Components VARCHAR(255), 
                Description TEXT, 
                Link_description TEXT, 
                Quantity INTEGER,
                Price DECIMAL(10,2)
            )
            """
        )

    # Import the data from the CSV file into the PostgreSQL table
    copy_query = sql.SQL("COPY {} FROM STDIN CSV HEADER").format(
        sql.Identifier(table_name)
    )

    logging.debug(copy_query)

    with open(csv_file_path, "r") as f:
        cur = conn.cursor()
        cur.copy_expert(copy_query, f)
        logging.debug(conn.commit())
        cur.close()
        conn.close()
