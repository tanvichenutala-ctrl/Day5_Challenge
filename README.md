# Employee Support Ticket App – Day 5 Challenge

A small Flask app for raising and tracking support tickets.
**It has 3 planted bugs:** one in the logic, one in the API input checks, and one on the screen.
Your job: find each bug, fix the root cause, and prove the fix with a test.

## Run it

1. Install Python 3.10 or newer.
2. In this folder, run:
   ```
   python -m venv .venv
   .venv\Scripts\activate        (Windows)
   source .venv/bin/activate     (Mac/Linux)
   pip install -r requirements.txt
   python app.py
   ```
3. Open http://127.0.0.1:5000 to see the ticket list.

## Run the tests

```
pytest
```
3 tests are included and they pass. Add your own.

## The API

| Method | Path | What it does |
|---|---|---|
| GET | /api/tickets | List all tickets, most urgent first |
| GET | /api/tickets/{id} | Get one ticket |
| POST | /api/tickets | Create a ticket. JSON body: title, description, category, priority |
| PATCH | /api/tickets/{id}/status | Change status. JSON body: status |

**Rules the app should follow**
- The list shows the most urgent tickets first: High, then Medium, then Low.
- A ticket must have a title. An empty title is not allowed.
- Category: Hardware, Software, Network, Access or Other.
- Priority: Low, Medium or High.
- Status: Open, In Progress, Resolved or Closed. The screen shows each ticket's real status.

## For each bug you find

1. Reproduce it: exact steps, expected vs actual.
2. Capture the log, response or screenshot.
3. Write your guess, then ask AI. Record both.
4. Find the root cause, not the symptom.
5. Make the smallest fix.
6. Write a test that fails before the fix and passes after.
7. Run all tests.

Then add at least 5 negative tests, and write a defect report for each bug.
Commit after every fix.
