
from flask import Flask, jsonify
import requests

app = Flask(__name__)

CATALOG_URL = "http://127.0.0.1:5001"
ORDER_URL = "http://127.0.0.1:5002"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Bazar Frontend Server is running!"
    })


# Forward search requests to the Catalog Server
@app.route("/search/<path:topic>", methods=["GET"])
def search(topic):
    try:
        response = requests.get(
            f"{CATALOG_URL}/search/{topic}",
            timeout=5
        )

        return jsonify(response.json()), response.status_code

    except requests.RequestException:
        return jsonify({
            "error": "Catalog Server is unavailable"
        }), 503



    
# Get information about a specific book from Catalog
@app.route("/info/<int:item_number>", methods=["GET"])
def info(item_number):
    try:
        response = requests.get(
            f"{CATALOG_URL}/info/{item_number}",
            timeout=5
        )

        return jsonify(response.json()), response.status_code

    except requests.RequestException:
        return jsonify({
            "error": "Catalog Server is unavailable"
        }), 503




# Forward purchase requests to the Order Server
@app.route("/purchase/<int:item_number>", methods=["POST"])
def purchase(item_number):
    try:
        response = requests.post(
            f"{ORDER_URL}/purchase/{item_number}",
            timeout=10
        )

        return jsonify(response.json()), response.status_code

    except requests.RequestException:
        return jsonify({
            "error": "Order Server is unavailable"
        }), 503



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
