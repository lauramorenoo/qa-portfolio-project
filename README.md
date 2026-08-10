# QA Portfolio Project — Flask API with Automated Test Suite

A small Flask API for managing items, with a full automated test suite covering the API and front-end.

## What This Project Demonstrates
- Automated API testing with pytest and requests
- Browser automation and end-to-end UI testing with Selenium
- CI/CD pipeline using GitHub Actions (tests run automatically on every push)
- RESTful API design (Flask)

## Tech Stack
Python, HTML, Javascript, Flask, pytest, Selenium, webdriver-manager, Git, GitHub

## Project Structure
```
app.py — Flask REST API with GET/POST endpoints for managing items
test_app.py — pytest suite testing the API directly (status codes, response data)
test_frontend.py — Selenium test simulating a real user adding an item through the browser
templates/index.html — front-end page for viewing and adding items
```

## How to Run Locally
```
git clone https://github.com/lauramorenoo/qa-portfolio-project.git
cd qa-portfolio-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run the Tests
Terminal 1 (start the server):
```
source venv/bin/activate
python3 app.py
```

Terminal 2 (run tests):
```
source venv/bin/activate
pytest test_app.py -v
pytest test_frontend.py -v
```

## Continuous Integration
Tests run automatically via GitHub Actions on every push.

## Future Improvements
- Better error handling
- Empty-list messaging
- Persistent storage instead of in-memory list (data resets every server restart)