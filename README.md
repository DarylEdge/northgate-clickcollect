# Click & Collect Stock Service

Northgate Retail's click and collect service. Reports stock by store, takes
reservations for collection, and confirms them to the customer.

## Running it locally

```
pip install -r requirements-dev.txt
python -m app.seed
flask --app app.main run
```

The service listens on http://localhost:5000.

## Tests

```
pytest
```

## Endpoints

| Method | Path                                   |
|--------|----------------------------------------|
| GET    | /api/stores                            |
| GET    | /api/stores/{store_id}/stock/{sku}     |
| POST   | /api/reservations                      |
| GET    | /api/reservations/{reference}          |

## Configuration

| Variable      | Default                      |
|---------------|------------------------------|
| DATABASE_URL  | sqlite:///clickcollect.db    |
| STORE_CONFIG  | config/stores.yaml           |
| PORT          | 5000                         |

## Decision log

`DECISIONS.md` in this repository is your decision log. It is assessed, and it
is what your technical commentary is built from. Start it in Week 5 and commit
to it as you go.

## Infrastructure

`infra/` holds the Terraform configuration for the environment this runs in.
See `infra/README.md`. You extend it in Week 7.
