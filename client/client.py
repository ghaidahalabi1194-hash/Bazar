
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


def purchase_book():
    item_number = input("Enter book ID to purchase: ")

    if not item_number.isdigit():
        print("Invalid book ID. Please enter a number.")
        return

    try:
        response = requests.post(
            f"{FRONTEND_URL}/purchase/{item_number}",
            timeout=15
        )

        result = response.json()

        if response.status_code == 200:
            print("Purchase successful!")
            print(result)
        else:
            print("Purchase failed:", result.get("error", result))

    except requests.RequestException:
        print("Frontend Server is unavailable.")




def main():
    while True:
        print("\n===== Bazar.com =====")
        print("1. Search for books")
        print("2. View book information")
        print("3. Purchase a book")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            search_books()
        elif choice == "2":
            book_info()
        elif choice == "3":
            purchase_book()
        elif choice == "4":
            print("Thank you for using Bazar.com!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()




