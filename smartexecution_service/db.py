import sqlite3

def get_connection():
    conn = sqlite3.connect("locators.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS locator_map (key TEXT PRIMARY KEY, locator TEXT)"
    )
    return conn
