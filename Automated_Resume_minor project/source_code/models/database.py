import sqlite3


def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_email TEXT,

        filename TEXT,

        score INTEGER,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":
    init_db()