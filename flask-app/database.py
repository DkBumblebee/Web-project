import sqlite3

def create_database():
        
    # Connect to the SQLite database (or create it if it doesn't exist)
    con = sqlite3.connect('database.db')
    c = con.cursor()

    # Create a table to store user information
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def add_user(first_name, last_name, username, email, password):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    c.execute("""
        INSERT INTO users (first_name, last_name, username, email, password)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, username, email, password))
    con.commit()
    con.close()

def update_user_password(username, new_password):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    try:
        c.execute("""
            UPDATE users
            SET password = ?
            WHERE username = ?
        """, (new_password, username))
        con.commit()
        print(f"Updated password for user: {username} is successful")
        print(f"Rows affected: {c.rowcount}")
        result = c.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error updating password for user: {username}: {e}")
    finally:
        con.close()


def query(sql_query, params=()):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    c.execute(sql_query, params)
    results = c.fetchall()
    con.commit()
    con.close()
    return results



def get_data():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row  # allows dictionary-style access
    print(con.row_factory)
    c = con.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    con.close()
    return rows