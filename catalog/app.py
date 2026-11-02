
from flask import Flask, jsonify, request
from catalog_service import search_books, get_book_info, update_book

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bazar Catalog Server is running!"})


# Search for books by topic
@app.route("/search/<path:topic>", methods=["GET"])
def search(topic):
    books = search_books(topic)
    return jsonify(books), 200



# Get information about a specific book
@app.route("/info/<int:item_number>", methods=["GET"])
def info(item_number):
    book = get_book_info(item_number)

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book), 200



# Update a book's price or stock quantity
@app.route("/update/<int:item_number>", methods=["PUT"])
def update(item_number):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    price = data.get("price")
    quantity = data.get("quantity")

    if price is None and quantity is None:
        return jsonify({"error": "Provide price or quantity"}), 400

    if price is not None and (
        isinstance(price, bool) or
        not isinstance(price, (int, float)) or price < 0
    ):
        return jsonify({"error": "Invalid price"}), 400

    if quantity is not None and (
        type(quantity) is not int or quantity < 0
    ):
        return jsonify({"error": "Invalid quantity"}), 400

    success = update_book(item_number, price, quantity)

    if not success:
        return jsonify({"error": "Book not found"}), 404

    return jsonify({"message": "Book updated successfully"}), 200




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
