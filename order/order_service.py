
import os
import requests

# Catalog Server address
CATALOG_URL = os.getenv(
    "CATALOG_URL",
    "http://127.0.0.1:5001"
)


def purchase_book(item_number):
    """
    Purchase a book:
    1. Get book information from Catalog.
    2. Check if the book is available.
    3. Reserve one copy from Catalog.
    4. Save the purchase in Order database.
    """

    from database import DB_PATH
    import sqlite3

    # Step 1: Get book information
    try:
        response = requests.get(
            f"{CATALOG_URL}/info/{item_number}",
            timeout=5
        )
    except requests.RequestException:
        return False, "Catalog Server is unavailable"

    if response.status_code != 200:
        return False, "Book not found"

    book = response.json()

    # Step 2: Check availability
    if book["quantity"] <= 0:
        return False, "Book is out of stock"

    # Step 3: Reserve one copy
    try:
        response = requests.post(
            f"{CATALOG_URL}/reserve/{item_number}",
            timeout=5
        )
    except requests.RequestException:
        return False, "Could not contact Catalog Server"

    if response.status_code != 200:
        return False, "Book is no longer available"

    # Step 4: Save the order
    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute(
            """
            INSERT INTO orders (book_id, book_title, price)
            VALUES (?, ?, ?)
            """,
            (item_number, book["title"], book["price"])
        )

        conn.commit()

    except sqlite3.Error:
        conn.rollback()

        # Restore the reserved copy if saving fails
        try:
            requests.post(
                f"{CATALOG_URL}/release/{item_number}",
                timeout=5
            )
        except requests.RequestException:
            pass

        return False, "Failed to save order"

    finally:
        conn.close()

    return True, f"bought book {book['title']}"
