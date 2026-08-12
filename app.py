# like a restaurant/kitchen: this file is the "cook," it builds the 
# actual app and does the real work (as opposed to test_app.py, which 
# just checks the work from outside)

# Flask to build the app itself, request to read incoming data
# jsonify to convert Python data into a proper JSON reponse
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

items = []  # in-memory storage — resets every time the server restarts

# Returns all items currently stored
@app.route("/items", methods=["GET"])
def get_items():
    # return all items as JSON
    return jsonify(items)

# Adds a new item, with the server assigning its id (not the client)
@app.route("/items", methods=["POST"])
def add_item():
    item = request.json
    # server generates id, not client — avoids duplicate ids
    item["id"] = len(items) + 1
    items.append(item)
    return jsonify(item)

# Returns a single item by id, or a 404 if it doesn't exist
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return jsonify({"error": "Item not found"}), 404

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)