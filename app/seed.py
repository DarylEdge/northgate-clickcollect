"""Populate the database with representative Northgate data."""

from app import db

STORES = [
    (1, "Northgate Manchester Arndale", "Manchester", "09:00", "17:30"),
    (2, "Northgate Trafford Park", "Stretford", "00:00", "23:59"),
    (3, "Northgate Salford Quays", "Salford", "09:00", "18:00"),
    (4, "Northgate Bolton", "Bolton", "10:00", "16:00"),
    (5, "Northgate Preston", "Preston", "08:30", "19:00"),
    (6, "Northgate Lancaster", "Lancaster", "09:00", "17:00"),
]

PRODUCTS = [
    ("NG-1001", "Oak dining chair", 8900),
    ("NG-1002", "Oak dining table, 4 seat", 32900),
    ("NG-1003", "Linen cushion cover, grey", 1400),
    ("NG-1004", "Linen cushion cover, ochre", 1400),
    ("NG-1005", "Cast iron casserole dish, 4L", 5900),
    ("NG-1006", "Stoneware dinner plate", 1200),
    ("NG-1007", "Stoneware bowl", 1100),
    ("NG-1008", "Copper pendant light", 6400),
    ("NG-1009", "Wool throw, charcoal", 4200),
    ("NG-1010", "Wool throw, moss", 4200),
    ("NG-1011", "Bamboo bath mat", 2200),
    ("NG-1012", "Cotton bath towel", 1800),
    ("NG-1013", "Ceramic table lamp", 3900),
    ("NG-1014", "Rattan storage basket", 2700),
    ("NG-1015", "Walnut chopping board", 2400),
    ("NG-1016", "Glass tumbler, set of 4", 1900),
    ("NG-1017", "Enamel mug", 900),
    ("NG-1018", "Jute floor rug, 120x170", 7900),
    ("NG-1019", "Velvet footstool", 8900),
    ("NG-1020", "Brass picture frame, A4", 1600),
]

# Deliberate distribution. The rows at exactly 1 are what make the
# availability rule reachable by a test.
SINGLE_UNIT = [(1, "NG-1002"), (2, "NG-1008"), (3, "NG-1019"), (4, "NG-1018")]
OUT_OF_STOCK = [(1, "NG-1010"), (4, "NG-1005"), (5, "NG-1013"), (6, "NG-1002")]


def _quantity_for(store_id, sku, index):
    if (store_id, sku) in SINGLE_UNIT:
        return 1
    if (store_id, sku) in OUT_OF_STOCK:
        return 0
    return 3 + ((store_id * 7 + index * 3) % 18)


def run():
    db.create_schema()
    db.reset()

    conn = db.connect()
    try:
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO stores (id, name, town, opens_at, closes_at)"
            " VALUES (?, ?, ?, ?, ?)",
            STORES,
        )
        cur.executemany(
            "INSERT INTO products (sku, name, price_pence) VALUES (?, ?, ?)",
            PRODUCTS,
        )
        rows = []
        for store in STORES:
            for index, product in enumerate(PRODUCTS):
                rows.append(
                    (store[0], product[0], _quantity_for(store[0], product[0], index))
                )
        cur.executemany(
            "INSERT INTO stock (store_id, sku, quantity_on_hand) VALUES (?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()

    print(f"Seeded {len(STORES)} stores, {len(PRODUCTS)} products, {len(rows)} stock rows.")


if __name__ == "__main__":
    run()
