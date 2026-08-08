# this is the food critic

import requests

# Checks that GET works
def test_get_items():
    response = requests.get("http://127.0.0.1:5000/items")
    assert response.status_code == 200
    
# Checks that POST works
def test_post_item():
    items = {"id": 1, "name": "Book"}
    r = requests.post("http://127.0.0.1:5000/items", json=items)
    assert r.status_code == 200
    
# Checks that GET-by-id works
def test_get_single_item():
    response = requests.get("http://127.0.0.1:5000/items/1")
    assert response.json()["id"] == 1
    
# Check a 404 for a nonexistent id
def test_get_item_not_found():
    response = requests.get("http://127.0.0.1:5000/items/2")
    assert response.status_code == 404