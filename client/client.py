
import requests

FRONTEND_URL = "http://127.0.0.1:5000"


def search_books():
    topic = input("Enter book topic: ")

    try:
        response = requests.get(
            f"{FRONTEND_URL}/search/{topic}",
            timeout=5
        )

        books = response.json()

        if response.status_code == 200:
            if books:
                print("\nSearch Results:")
                for book in books:
                    print(f"{book['id']}: {book['title']}")
            else:
                print("No books found.")
        else:
            print("Error:", books)

    except requests.RequestException:
        print("Frontend Server is unavailable.")

def book_info():
    item_number = input("Enter book ID: ")

    if not item_number.isdigit():
        print("Invalid book ID. Please enter a number.")
        return

    try:
        response = requests.get(
            f"{FRONTEND_URL}/info/{item_number}",
            timeout=5
        )

        book = response.json()

        if response.status_code == 200:
            print("\nBook Information:")
            print(f"Title: {book['title']}")
            print(f"Price: ${book['price']}")
            print(f"Quantity: {book['quantity']}")
        else:
            print("Error:", book.get("error", "Unknown error"))

    except requests.RequestException:
        print("Frontend Server is unavailable.")        


book_info()



