# QA Portfolio Project — Progress Notes

## Setup
- Project folder: `qa-portfolio-project`
- Activate venv: `source venv/bin/activate`
- Confirm venv is active: `which python3` → should point inside `.../venv/bin/python3`
- Installed so far: `pytest`, `requests`, `selenium`, `webdriver-manager`

## Terminal notes
- Using iTerm2 (not Warp) — removed `zsh-autosuggestions` plugin from `~/.zshrc` because it was causing dropped/ghosted keystrokes after `source` commands
- If typing ever looks broken again after a shell command: fully quit and reopen iTerm2, don't just re-`source` the config

## EVERY TIME YOU START A SESSION — do this first
1. Open Terminal 1 → navigate to `qa-portfolio-project` → run:
   ```
   source venv/bin/activate
   python3 app.py
   ```
   Leave this running the whole session. This is your server (the "restaurant").
2. Open Terminal 2 (separate tab, same folder) → run:
   ```
   source venv/bin/activate
   ```
   This is where you'll run `curl` or `pytest` commands (the "critic" ordering food and checking it).
3. Remember: saving `app.py` auto-restarts the server AND wipes the in-memory `items` list back to `[]`.
   If you POST test data, then edit+save app.py again, you'll need to re-POST before testing GET again.
---

## Exercise 1 — pytest fundamentals ✅ DONE
- Built `calculator.py`: `add`, `subtract`, `multiply`, `divide` (raises `ValueError` on divide-by-zero)
- Built `test_calculator.py`: 5 tests, all passing
- Run tests: `pytest` or `pytest -v` for detail

**Concepts learned:**
- `def function_name(params):` + indented body — that's an actual function, not just a name
- `assert condition` — checks something is true; fails loudly if not. Different from `print()`, which just displays a value and checks nothing.
- `assert(x)` alone only checks "truthy" — NOT the same as `assert x == expected_value`. Watch for this trap.
- `pytest.raises(ValueError):` — wrap the line expected to raise an error inside a `with` block

## Exercise 2 — API testing with `requests` ✅ DONE
- Built `test_api.py` — GET request to JSONPlaceholder, checked status code and response JSON
- Fixed same truthy-assert trap: `assert response.status_code == 200` (not just `assert(response.status_code)`)

**Concepts learned:**
- `requests.get(url)` → returns a response object
- `.status_code` and `.json()` are called ON the response object, not on `requests` itself
- `"key" in response.json()` — checks a key exists in the returned data

## Exercise 3 — Selenium basics ✅ DONE
- Built `test_selenium.py` — opens example.com, finds "Learn more" link, checks its href
- **Important:** pytest only discovers files STARTING with `test_` (e.g. `test_selenium.py`, not `selenium_test.py`)

**Concepts learned:**
- `driver.find_element(By.LINK_TEXT, "exact text")` — must match visible text exactly, case-sensitive
- Must SAVE the found element to a variable — otherwise it's found and immediately discarded
- Call `.get_attribute("href")` on the found ELEMENT, not on `driver`
- Real bug caught: assumed URL was `https://www.iana.org/...`, actual was `https://iana.org/...` (no www) — tests should match reality, not assumptions. Always verify expected values instead of guessing.

---

## THE PLAN — Portfolio Project (Flask API + Selenium front-end)

Pace: ~2-3 hrs/week, alongside DSA/Swift study plan

## Week 1 — Flask API ✅ DONE
- Built `app.py` with 3 routes: GET /items, POST /items, GET /items/<id>
- Two terminals needed: one runs the server (`python3 app.py`), one tests it (`curl ...`)
- Server auto-restarts on save (debug mode) — this WIPES the in-memory `items` list back to []
  - Always re-POST test data after any save if you're about to GET/test again

**Bugs I hit and fixed:**
- `request.json()` → wrong, it's a property not a method → fixed to `request.json`
- `items.add(item)` → lists don't have `.add()`, that's a set method → use `.append()`
- `return items.append(item)` → `.append()` always returns None → split into 2 lines: append, then separately `return jsonify(item)`
- `for id in items:` then `if id == item_id` → wrong, `id` was the whole dict not the number → fixed to `for item in items:` then `if item["id"] == item_id:`
- Forgot a `return` for the "no match found" case (after the for loop ends) → caused "did not return a valid response" error even though the matching logic was correct

**Key lesson:** "did not return a valid response" doesn't always mean the logic is wrong — check if there's actually a return path for EVERY case, including "not found" / loop finished without matching.

**To do later (optional improvements):**
- [ ] Return a proper 404 + error message when item id doesn't exist: `return jsonify({"error": "Item not found"}), 404`
- [ ] Handle empty `items` list gracefully with a clear message

## Week 2 — API test suite (pytest against own Flask API) ✅ DONE
- Built `test_app.py` — 4 tests, all passing:
  - `test_get_items` — GET /items returns 200
  - `test_post_item` — POST /items with JSON data returns 200
  - `test_get_single_item` — GET /items/1 returns the correct item
  - `test_get_item_not_found` — GET /items/2 (doesn't exist) returns 404

**Key concept — tests call the API from the OUTSIDE, they don't reuse the app's own logic:**
Restaurant analogy: `app.py` is the restaurant (does the actual work). `test_app.py` is the food critic —
places an order via `requests.get()/.post()`, gets a response back, and checks (`assert`) that it's correct.
Tests should never re-loop through data or recreate the route's logic — just call the URL and check the result.

**Bugs I hit and fixed:**
- `assert r == 200` → wrong, compares the whole response object to a number → fixed to `r.status_code == 200`
- POST with no data → 415 Unsupported Media Type → fixed by adding `json=items` param to `requests.post(...)`,
  which sends the data AND sets the right content-type header automatically
- Function named `get_single_item` (no `test_` prefix) → pytest silently skipped it → same rule as filenames,
  function names must start with `test_` too
- `assert 1 in response.json()["id"]` → wrong, `in` checks membership in a collection; `response.json()["id"]`
  is already a single number, not a collection → fixed to `==` for exact value comparison
- Forgetting the server needs to be running in a separate terminal before running tests → 403 errors with
  nothing obviously wrong in the test code itself — always check the server terminal first when confused

**Key lesson:** `in` = "does this exist somewhere inside a collection" vs `==` = "does this exact value match."
Mixing these up is one of the most common beginner errors — worth double-checking every assert line.

**Progress % in `pytest -v` output** = how many of the total tests have finished running so far, NOT a score
or grade for each test. 2 tests → 50%, 100%. 4 tests → 25%, 50%, 75%, 100%.

## Week 3 — Minimal front-end ✅ DONE
- Added `templates/index.html` (must live in a folder literally named `templates`, directly inside the
  project folder — Flask looks there specifically via `render_template()`)
- Added new route + import in `app.py`:
  ```python
  from flask import Flask, request, jsonify, render_template
  ...
  @app.route("/")
  def home():
      return render_template("index.html")
  ```
- `index.html` now:
  - Loads existing items on page load and displays them in a `<ul>`
  - Has a form to add a new item — submits via JavaScript `fetch` (no full page reload)
  - New items appear on the page immediately after adding, no refresh needed

**Key concept — `fetch` is JavaScript's version of Python's `requests`:**
Same idea as `requests.get()`/`requests.post()` in Python — `fetch()` lets the BROWSER make HTTP calls
to the Flask API. `.then()` chains handle each step: get the raw response → convert to JSON → do
something with the data.

**Key concept — DOM manipulation (writing to the actual page):**
- `document.getElementById("some-id")` — grabs an existing HTML element by its id
- `document.createElement("li")` — creates a new element in memory (not on the page yet)
- `element.textContent = "..."` — sets the visible text of an element
- `parent.appendChild(child)` — actually attaches a created element onto the page

**Bugs I hit and fixed:**
- `TemplateNotFound` error → `index.html` was saved outside the project folder instead of inside
  `templates/` — Flask needs the exact folder name/location
- POST from the form failed silently at first (form only did `console.log`, nothing visible changed
  on the page) → had to manually add DOM code (createElement/appendChild) inside the POST's
  `.then(data => {...})`, not just the GET block — each `.then()` block only affects the page if you
  explicitly write code to do so
- `ReferenceError: li is not defined` → used `li.textContent = ...` without ever creating `li` first
  with `document.createElement("li")` in that block — variables must be created before use
- Reused the variable name `name` twice in the SAME function (once for the typed input value, once
  attempted for the list element) → caused a conflict. Fixed by renaming the second one to `list`.
  **Rule:** variable names can safely repeat across DIFFERENT functions/blocks (each is its own separate
  scope), but NOT twice within the same function.

**Feature bug caught and fixed — duplicate IDs:**
- Originally hardcoded `id: 1` in the form's fetch body → adding a 2nd/3rd item all shared id 1,
  making `GET /items/<id>` unable to ever reach items after the first
- Fixed properly server-side in `app.py`'s `add_item()`:
  ```python
  item = request.json
  item["id"] = len(items) + 1
  items.append(item)
  ```
  Server now assigns unique, incrementing ids — client no longer sends an `id` at all
- **Lesson on `=` vs updating a dict key:** `item = len(items) + 1` completely REPLACES the `item`
  variable (throwing away the dict). `item["id"] = len(items) + 1` correctly ADDS/UPDATES just the
  `"id"` key while keeping the rest of the dict (like `"name"`) intact.
- id counter keeps climbing as long as the server stays running (expected) — only resets to 1 when
  the server restarts and wipes `items` back to `[]`

**Real-world pattern note:** save-then-update-the-page-live (instead of forcing a full reload) is how
most modern web apps work (adding a comment, a to-do, a post, etc.) — not just a training exercise.

**Localhost note:** `http://127.0.0.1:5000` only works on your own machine — it's not a real public
URL. In a real job, the API would live at a real domain (e.g. `https://api.company.com`), often with
a separate "staging"/test environment — but the testing approach/code is otherwise identical.

## Week 4 — Selenium tests for the front-end ✅ DONE
- Built `test_frontend.py` — end-to-end test:
  1. Loads the page, confirms `<h1>` heading text is "Items"
  2. Types "Bananas" into the item-name input
  3. Clicks the Add Item button
  4. Waits for "Bananas" to actually appear in the item list, then asserts it's there

**New locator used — `By.TAG_NAME`:**
- Finds elements by their HTML tag (e.g. `"h1"`, `"p"`), NOT by the text inside them
- Used when an element has no `id`/`class` to target — e.g. `driver.find_element(By.TAG_NAME, "h1")`

**Reading text off an element:**
- `.text` — a property (no parentheses) that gives the visible text content of an element
- Different from `.get_attribute("href")` used earlier — that was specific to pulling a link's URL

**Interacting with elements:**
- `.send_keys("some text")` — types into an input field
- `.click()` — clicks a button/element

**Bugs I hit and fixed:**
- `link.get_header("h1")` → not a real Selenium method, doesn't exist → correct property is `.text`
- Targeted `By.ID, "add-form"` (the whole `<form>`) instead of the actual button, because the button
  had no `id` of its own → fixed properly by adding `id="add-button"` directly to the `<button>` tag
  in `index.html`, then targeting that instead. Lesson: if the right element isn't identifiable,
  it's often better to fix the HTML (give it a proper id) than to work around it in the test.
- `IndentationError: unindent does not match any outer indentation level` → caused by mixing TABS and
  SPACES in the same file, even though it looked visually identical on screen. Fixed via VS Code's
  bottom-right indentation menu → "Convert Indentation to Tabs" (normalizes the whole file at once).
  This bug is invisible to the eye — if it happens again, check the indentation-mode setting first,
  don't just keep re-tabbing the same line.

**Explicit waits (replacing blind `time.sleep()`):**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
wait.until(EC.text_to_be_present_in_element((By.ID, "item-list"), "Bananas"))
```
- Instead of guessing a fixed pause, this actively checks (up to a max timeout) until a specific
  condition becomes true, then continues immediately
- Needed here because the `<ul id="item-list">` element itself exists on page load (starts empty) —
  it's specifically the TEXT inside it that takes a moment to update after the POST/fetch completes.
  The wait is for the content to update, not for the element to exist.
- `time.sleep(x)` is fine for visually confirming something works while learning, but explicit waits
  are the real pattern used in production test suites

**Key lesson (general):** "in" vs "==" distinction applies here too — checking `"Bananas" in item_list.text`
(does this text appear somewhere within the list) vs `==` (exact match) — same pattern from the API tests.





- [ ] **Week 5 — CI setup:** GitHub Actions to auto-run both test suites on push
- [ ] **Week 6 — README + interview prep:** Clean README (what/why/how to run), 90-second verbal walkthrough

---

## Questions / things to revisit
(add anything confusing here as you go, so we can circle back)
-
