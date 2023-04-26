import sqlite3
from typing import List, Union, Tuple


def create_connection(database: str) -> Union[sqlite3.Connection, None]:
    """Create a connection to database.

    params:
    - database (str): the path to database file

    returns:
    - conn (sqlite3.Connection): the connection object
    """
    try:
        conn = sqlite3.connect(database, check_same_thread=False)
        print(f"Successfully connected to {database}")
        return conn
    except sqlite3.Error as e:
        print(e)


def create_cursor(conn: sqlite3.Connection) -> Union[sqlite3.Cursor, None]:
    """Create a cursor object from connection.

    params:
    - conn (sqlite3.Connection): the connection object

    returns:
    - cursor (sqlite3.Cursor): the cursor object
    """
    try:
        cursor = conn.cursor()
        return cursor
    except sqlite3.Error as e:
        print(e)


def create_table(
        cursor: sqlite3.Cursor, 
        table_name: str, 
        columns: List[str]
        ) -> None:
    """Create a table in database.

    params:
    - cursor (sqlite3.Cursor): the cursor object
    - table_name (str): the name of the table to create
    - columns (list of str): a list of column names and data types, e.g. 
    ["id INTEGER", "name TEXT", "age INTEGER"]

    returns:
    - None
    """
    try:
        columns_string = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_string})"
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)

def insert_data(
        conn: sqlite3.Connection, 
        cursor: sqlite3.Cursor,
        table_name: str, 
        item: Tuple[str, str]
        ) -> None:
    """Insert data into database.
    If the data already exists, update it.

    params:
    - conn (sqlite3.Connection): the connection object
    - cursor (sqlite3.Cursor): the cursor object
    - table_name (str): the name of the table to insert data into
    - item (tuple of str): a tuple of data to insert into database

    returns:
    - None
    """
    user_id, pagination_status = item
    cursor.execute(
        f"SELECT * FROM {table_name} WHERE user_id = ?", 
        (user_id,))
    if cursor.fetchone():
        cursor.execute(
            f"UPDATE {table_name} SET pagination_status = ? WHERE user_id = ?", 
            (pagination_status, user_id))
    else:
        cursor.execute(
            f"INSERT INTO {table_name} (user_id, pagination_status) VALUES (?, ?)", 
            (user_id, pagination_status))
    conn.commit()


def select_pagination_status(
        cursor: sqlite3.Cursor,
        condition: str
        ) -> List[Tuple[str]]:
    """Select data from database.

    params:
    - cursor (sqlite3.Cursor): the cursor object
    - table_name (str): the name of the table to select data from
    - column (str): column name to select
    - condition (str): the condition to filter data

    returns:
    - data (list of tuple of str): a list of tuples of data
    """
    # query = f"SELECT {column} FROM {table_name} WHERE {condition}"

    cursor.execute(
        "SELECT pagination_status FROM settings WHERE user_id = ?", 
        (condition,))
    return cursor.fetchall()
