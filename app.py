#### for understandment this is the restaurant ####

# Flask to build the app itself, request to read incoming data
# jsonify to convert Python data into a proper JSON reponse
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

items = []  # this will hold our data in memory

@app.route("/items", methods=["GET"])
def get_items():
    # return all items as JSON
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    # get the new item from the request, add it to `items`, return it
    item = request.json
    item["id"] = len(items) + 1
    items.append(item)
    return jsonify(item)
    
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    # find and return the one item matching item_id
    for item in items:
        if item["id"] == item_id:
            return item
    return jsonify({"error": "Item not found"}), 404

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)