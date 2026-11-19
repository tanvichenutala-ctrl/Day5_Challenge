import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404

def test_tickets_sorted_high_medium_low(client):
    priorities = [t["priority"] for t in client.get("/api/tickets").get_json()]
    assert priorities == ["High", "High", "Medium", "Medium", "Low"]

def test_empty_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": ""})
    assert response.status_code == 400


def test_blank_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": "   "})
    assert response.status_code == 400

def test_resolved_ticket_shows_resolved_on_screen(client):
    html = client.get("/").get_data(as_text=True)
    assert "Resolved" in html
# Add your own tests below: one failing test for each bug you find,
# plus at least 5 negative tests.
