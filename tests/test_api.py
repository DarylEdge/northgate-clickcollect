import os
import tempfile

import pytest

os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(
    tempfile.gettempdir(), "clickcollect_test.db"
)

from app import db, notifications, seed  # noqa: E402
from app.main import create_app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database():
    seed.run()
    notifications.clear()
    yield
    db.reset()


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_list_stores_returns_every_store(client):
    response = client.get("/api/stores")
    assert response.status_code == 200
    assert len(response.get_json()) == 6


def test_store_record_includes_town_and_hours(client):
    store = client.get("/api/stores").get_json()[0]
    assert store["town"] == "Manchester"
    assert store["opens_at"] == "09:00"
    assert store["closes_at"] == "17:30"


def test_stock_lookup_returns_available_quantity(client):
    response = client.get("/api/stores/1/stock/NG-1001")
    assert response.status_code == 200
    body = response.get_json()
    assert body["sku"] == "NG-1001"
    assert body["available"] >= 0


def test_stock_lookup_for_unknown_store_is_404(client):
    assert client.get("/api/stores/99/stock/NG-1001").status_code == 404


def test_stock_lookup_for_unknown_sku_is_404(client):
    assert client.get("/api/stores/1/stock/NG-9999").status_code == 404


def test_create_reservation_returns_a_reference(client):
    response = client.post(
        "/api/reservations",
        json={
            "store_id": 2,
            "sku": "NG-1003",
            "quantity": 2,
            "customer_email": "a.patel@example.com",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["reference"].startswith("NG-")


def test_create_reservation_rejects_zero_quantity(client):
    response = client.post(
        "/api/reservations",
        json={
            "store_id": 2,
            "sku": "NG-1003",
            "quantity": 0,
            "customer_email": "a.patel@example.com",
        },
    )
    assert response.status_code == 400


def test_create_reservation_rejects_missing_fields(client):
    response = client.post("/api/reservations", json={"store_id": 2})
    assert response.status_code == 400


def test_create_reservation_for_unknown_sku_is_404(client):
    response = client.post(
        "/api/reservations",
        json={
            "store_id": 2,
            "sku": "NG-9999",
            "quantity": 1,
            "customer_email": "a.patel@example.com",
        },
    )
    assert response.status_code == 404


def test_reservation_can_be_retrieved_by_reference(client):
    created = client.post(
        "/api/reservations",
        json={
            "store_id": 2,
            "sku": "NG-1006",
            "quantity": 1,
            "customer_email": "j.okafor@example.com",
        },
    ).get_json()

    response = client.get(f"/api/reservations/{created['reference']}")
    assert response.status_code == 200
    assert response.get_json()["customer_email"] == "j.okafor@example.com"


def test_unknown_reservation_reference_is_404(client):
    assert client.get("/api/reservations/NG-NOPE").status_code == 404
