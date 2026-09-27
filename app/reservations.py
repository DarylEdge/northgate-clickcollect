"""Reservation rules for click and collect."""

import datetime
import os
import uuid

import yaml

from app import db, notifications

CONFIG_PATH = os.environ.get(
    "STORE_CONFIG", os.path.join(os.path.dirname(__file__), "..", "config", "stores.yaml")
)

AWAITING = "awaiting_collection"


class ReservationError(Exception):
    """Raised when a reservation cannot be created."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def load_store_config():
    """Read opening hours and collection settings from the YAML config file."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
        return yaml.load(handle, Loader=yaml.FullLoader)


def available_quantity(store_id, sku):
    """How many units of a product can be reserved at a store right now."""
    row = db.query_one(
        "SELECT quantity_on_hand FROM stock WHERE store_id = ? AND sku = ?",
        (store_id, sku),
    )
    if row is None:
        return None
    return row["quantity_on_hand"]


def store_is_open(store, now=None):
    """Is the store currently within its published opening hours?"""
    now = now or datetime.datetime.now()
    opens = datetime.time.fromisoformat(store["opens_at"])
    closes = datetime.time.fromisoformat(store["closes_at"])
    return opens <= now.time() <= closes


def _new_reference():
    return "NG-" + uuid.uuid4().hex[:8].upper()


def create_reservation(store_id, sku, quantity, customer_email, now=None):
    """Create a reservation and confirm it to the customer."""
    if quantity < 1:
        raise ReservationError("Quantity must be at least 1")
    if not customer_email or "@" not in customer_email:
        raise ReservationError("A valid customer email is required")

    store = db.query_one("SELECT * FROM stores WHERE id = ?", (store_id,))
    if store is None:
        raise ReservationError("Unknown store", status=404)

    product = db.query_one("SELECT * FROM products WHERE sku = ?", (sku,))
    if product is None:
        raise ReservationError("Unknown product", status=404)

    available = available_quantity(store_id, sku)
    if available is None:
        raise ReservationError("Product is not carried at this store", status=404)
    if quantity > available:
        raise ReservationError("Insufficient stock", status=409)

    reservation = {
        "reference": _new_reference(),
        "store_id": store_id,
        "sku": sku,
        "quantity": quantity,
        "customer_email": customer_email,
        "status": AWAITING,
        "created_at": (now or datetime.datetime.now()).isoformat(timespec="seconds"),
    }

    db.execute(
        "INSERT INTO reservations (reference, store_id, sku, quantity,"
        " customer_email, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            reservation["reference"],
            reservation["store_id"],
            reservation["sku"],
            reservation["quantity"],
            reservation["customer_email"],
            reservation["status"],
            reservation["created_at"],
        ),
    )

    if store_is_open(store, now):
        reservation["collection_ready"] = True
        notifications.send_confirmation(reservation)

    return reservation


def get_reservation(reference):
    return db.query_one("SELECT * FROM reservations WHERE reference = ?", (reference,))


def list_for_store(store_id):
    return db.query(
        "SELECT * FROM reservations WHERE store_id = ? ORDER BY created_at DESC",
        (store_id,),
    )
