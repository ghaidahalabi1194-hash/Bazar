
from flask import Flask, jsonify
from database import init_db
from order_service import purchase_book

app = Flask(__name__)

# Initialize the Order database when the server starts
init_db()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Order Server is running"
    }), 200


@app.route("/purchase/<int:item_number>", methods=["POST"])
def purchase(item_number):
    success, message = purchase_book(item_number)

    if success:
        print(message, flush=True)
        return jsonify({
            "message": message
        }), 200

    print(f"Purchase failed: {message}", flush=True)

    return jsonify({
        "error": message
    }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=False
    )
