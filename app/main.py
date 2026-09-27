"""Northgate Retail — Click & Collect Stock Service."""

import os
import random
import time

from flask import Flask, jsonify, request, send_from_directory

from app import db
from app.reservations import (
    ReservationError,
    available_quantity,
    create_reservation,
    get_reservation,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")


def _apply_chaos():
    mode = os.environ.get("CHAOS_MODE", "")
    if mode == "latency":
        time.sleep(random.uniform(3.0, 8.0))
    elif mode == "errors" and random.random() < 0.15:
        return jsonify({"error": "Internal server error"}), 500
    return None


def create_app():
    app = Flask(__name__, static_folder=None)
    db.create_schema()

    @app.before_request
    def before_request():
        return _apply_chaos()

    @app.get("/")
    def index():
        return send_from_directory(STATIC_DIR, "index.html")

    @app.get("/api/stores")
    def list_stores():
        stores = db.query("SELECT * FROM stores ORDER BY id")
        return jsonify(stores)

    @app.get("/api/stores/<int:store_id>/stock/<sku>")
    def stock_level(store_id, sku):
        store = db.query_one("SELECT * FROM stores WHERE id = ?", (store_id,))
        if store is None:
            return jsonify({"error": "Unknown store"}), 404

        quantity = available_quantity(store_id, sku)
        if quantity is None:
            return jsonify({"error": "Product not carried at this store"}), 404

        return jsonify(
            {
                "store_id": store_id,
                "store_name": store["name"],
                "sku": sku,
                "available": quantity,
            }
        )

    @app.post("/api/reservations")
    def post_reservation():
        payload = request.get_json(silent=True) or {}
        required = ("store_id", "sku", "quantity", "customer_email")
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        try:
            reservation = create_reservation(
                store_id=int(payload["store_id"]),
                sku=str(payload["sku"]),
                quantity=int(payload["quantity"]),
                customer_email=str(payload["customer_email"]),
            )
        except ReservationError as exc:
            return jsonify({"error": exc.message}), exc.status

        return jsonify(reservation), 201

    @app.get("/api/reservations/<reference>")
    def fetch_reservation(reference):
        reservation = get_reservation(reference)
        if reservation is None:
            return jsonify({"error": "Unknown reservation"}), 404
        return jsonify(reservation)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
