import sqlite3

from langchain_core.tools import Tool

conn = sqlite3.connect('db.sqlite')


def run_sqlite_query(query):
    c = conn.cursor()

    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as error:
        return f"The following error occurred: {str(error)}"


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a query on the SQLite database",
    func=run_sqlite_query,
)
