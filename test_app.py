# this is the food critic

import requests

# Confirms the GET /items route responds successfully
def test_get_items():
    response = requests.get("http://127.0.0.1:5000/items")
    assert response.status_code == 200
    
# Confirms the server accepts a new item and responds successfully
# (checks the request succeeded — not the returned content)
def test_post_item():
    items = {"id": 1, "name": "Book"}
    r = requests.post("http://127.0.0.1:5000/items", json=items)
    assert r.status_code == 200
    
# Confirms requesting a specific item by id (not just "any" item) returns that exact item
def test_get_single_item():
    response = requests.get("http://127.0.0.1:5000/items/1")
    assert response.json()["id"] == 1
    
# Confirms requesting a nonexistent id correctly returns a 404, not a crash or empty success
def test_get_item_not_found():
    response = requests.get("http://127.0.0.1:5000/items/2")
    assert response.status_code == 404