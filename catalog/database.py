
import sqlite3
from pathlib import Path

# Database file location
import os

DB_PATH = Path(
    os.getenv(
        "CATALOG_DB_PATH",
        str(Path(__file__).resolve().parent / "catalog.db")
    )
)

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite (creates the database if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    # Insert the four initial books only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        books = [
            (1, "How to get a good grade in DOS in 40 minutes a day",
             "distributed systems", 40, 10),
            (2, "RPCs for Noobs",
             "distributed systems", 50, 5),
            (3, "Xen and the Art of Surviving Undergraduate School",
             "undergraduate school", 25, 8),
            (4, "Cooking for the Impatient Undergrad",
             "undergraduate school", 20, 6)
        ]

        cursor.executemany("""
            INSERT INTO books (id, title, topic, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, books)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Catalog database initialized successfully!")
