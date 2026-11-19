"""Employee Support Ticket App (Day 5 Challenge).

A small Flask app. Run it, test it, and find the 3 planted bugs:
one in the logic, one in the API input checks, and one on the screen.
"""
from datetime import date

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

CATEGORIES = ["Hardware", "Software", "Network", "Access", "Other"]
PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

TICKETS = []


def reset_tickets():
    """Load the 5 sample tickets (used at start-up and by the tests)."""
    TICKETS.clear()
    samples = [
        ("Laptop not charging", "Hardware", "High", "Open"),
        ("Cannot log in to VPN", "Network", "High", "In Progress"),
        ("Need access to the shared project folder", "Access", "Medium", "Open"),
        ("Excel keeps crashing on startup", "Software", "Medium", "Resolved"),
        ("Request a second monitor", "Hardware", "Low", "Closed"),
    ]
    for i, (title, category, priority, status) in enumerate(samples, start=1):
        TICKETS.append({
            "id": i,
            "title": title,
            "description": f"Sample ticket: {title.lower()}.",
            "category": category,
            "priority": priority,
            "status": status,
            "created": str(date(2026, 11, 18)),
        })


def find_ticket(ticket_id):
    for ticket in TICKETS:
        if ticket["id"] == ticket_id:
            return ticket
    return None


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def sort_by_priority(tickets):
    """Return tickets with the most urgent first: High, then Medium, then Low."""
    return sorted(tickets, key=lambda t: PRIORITY_ORDER[t["priority"]])


# ---------- API ----------

@app.get("/api/tickets")
def list_tickets():
    return jsonify(sort_by_priority(TICKETS))


@app.get("/api/tickets/<int:ticket_id>")
def get_ticket(ticket_id):
    ticket = find_ticket(ticket_id)
    if ticket is None:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(ticket)


@app.post("/api/tickets")
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description", "")
    category = data.get("category", "Other")
    priority = data.get("priority", "Medium")

    if title is None:
        return jsonify({"error": "Title is required"}), 400
    if category not in CATEGORIES:
        return jsonify({"error": "Unknown category"}), 400
    if priority not in PRIORITIES:
        return jsonify({"error": "Unknown priority"}), 400

    ticket = {
        "id": max((t["id"] for t in TICKETS), default=0) + 1,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "created": str(date.today()),
    }
    TICKETS.append(ticket)
    return jsonify(ticket), 201


@app.patch("/api/tickets/<int:ticket_id>/status")
def change_status(ticket_id):
    ticket = find_ticket(ticket_id)
    if ticket is None:
        return jsonify({"error": "Ticket not found"}), 404
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in STATUSES:
        return jsonify({"error": "Unknown status"}), 400
    ticket["status"] = status
    return jsonify(ticket)


# ---------- Screen ----------

STATUS_LABELS = {
    "Open": "Open",
    "In Progress": "In Progress",
    "Resolved": "Open",
    "Closed": "Closed",
}

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Support Tickets</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 32px; color: #2E2E2E; }
    h1 { color: #1A7FA0; }
    table { border-collapse: collapse; width: 100%; max-width: 900px; }
    th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid #ddd; }
    th { background: #1E1E1E; color: #fff; }
    .badge { padding: 2px 10px; border-radius: 12px; background: #E6F7FD; }
  </style>
</head>
<body>
  <h1>Tickets</h1>
  <table>
    <tr><th>ID</th><th>Title</th><th>Category</th><th>Priority</th><th>Status</th></tr>
    {% for t in tickets %}
    <tr>
      <td>{{ t.id }}</td>
      <td>{{ t.title }}</td>
      <td>{{ t.category }}</td>
      <td>{{ t.priority }}</td>
      <td><span class="badge">{{ labels[t.status] }}</span></td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(PAGE, tickets=sort_by_priority(TICKETS), labels=STATUS_LABELS)


reset_tickets()

if __name__ == "__main__":
    app.run(debug=True)
