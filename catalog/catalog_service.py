
import sqlite3
from database import DB_PATH


def search_books(topic):
    # Connect to the Catalog database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Search for books matching the requested topic
    cursor = conn.execute(
        "SELECT id, title FROM books WHERE LOWER(topic) = LOWER(?)",
        (topic,)
    )

    # Convert database rows into dictionaries
    books = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return books

def get_book_info(item_number):
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Find the book by its ID
    cursor = conn.execute(
        "SELECT title, quantity, price FROM books WHERE id = ?",
        (item_number,)
    )

    book = cursor.fetchone()
    conn.close()

    # Return the book information, or None if not found
    return dict(book) if book else None



def update_book(item_number, price=None, quantity=None):
    conn = sqlite3.connect(DB_PATH)

    # Check whether the book exists
    cursor = conn.execute(
        "SELECT id FROM books WHERE id = ?",
        (item_number,)
    )

    if cursor.fetchone() is None:
        conn.close()
        return False

    # Update the price if provided
    if price is not None:
        conn.execute(
            "UPDATE books SET price = ? WHERE id = ?",
            (price, item_number)
        )

    # Update the quantity if provided
    if quantity is not None:
        conn.execute(
            "UPDATE books SET quantity = ? WHERE id = ?",
            (quantity, item_number)
        )

    conn.commit()
    conn.close()
    return True



def reserve_book(item_number):
    conn = sqlite3.connect(DB_PATH, timeout=10)

    # Decrease stock only if at least one copy is available
    cursor = conn.execute(
        """
        UPDATE books
        SET quantity = quantity - 1
        WHERE id = ? AND quantity > 0
        """,
        (item_number,)
    )

    # Check whether one book was successfully reserved
    success = cursor.rowcount == 1

    if success:
        conn.commit()
    else:
        conn.rollback()

    conn.close()
    return success




def release_book(item_number):
    conn = sqlite3.connect(DB_PATH, timeout=10)

    # Restore one reserved copy to the stock
    cursor = conn.execute(
        """
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?
        """,
        (item_number,)
    )

    success = cursor.rowcount == 1

    if success:
        conn.commit()
    else:
        conn.rollback()

    conn.close()
    return success
