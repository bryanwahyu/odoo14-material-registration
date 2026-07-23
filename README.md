# Material Registration (Odoo 14)

[![Odoo 14 Tests](https://github.com/bryanwahyu/odoo14-material-registration/actions/workflows/tests.yml/badge.svg)](https://github.com/bryanwahyu/odoo14-material-registration/actions/workflows/tests.yml)

Odoo 14 module to register materials to be sold. Covers the KeDA Tech
Backend test: ERD, models, REST controllers, and unit tests.

## Requirements covered

Material record holds:

1. Material Code (`code`) — required, unique
2. Material Name (`name`) — required
3. Material Type (`material_type`) — required selection: Fabric, Jeans, Cotton
4. Material Buy Price (`buy_price`) — required, **must be >= 100**
5. Related Supplier (`supplier_id`) — required, dropdown of supplier names

Client can:

- List all materials and **filter by Material Type** (backend search filters + REST query param)
- Update one material (backend form + `PUT` endpoint)
- Delete one material (backend + `DELETE` endpoint)

## Design

Layered on top of Odoo conventions — SOLID applied without over-building
(YAGNI / KISS). The Odoo ORM is already the persistence layer, so no
extra repository abstraction is added.

- **Domain** (`models/material.py`, `models/material_supplier.py`) —
  entities and invariants (required fields, unique code, min buy price).
  Rules hold no matter who calls (UI, API, tests).
- **Application** (`models/material_service.py`) — `material.service`
  (`AbstractModel`) holds the use cases: list/filter, create, read,
  update, delete, plus serialization. Single source of truth reused by
  both the controller and the tests.
- **Interface** (`controllers/main.py`) — thin REST adapter. Only
  translates HTTP <-> use case and maps domain errors to status codes.

## REST API

All endpoints return JSON `{"success": bool, "data"|"error": ...}` and
require an authenticated Odoo session (`auth='user'`).

| Method | Path                          | Purpose                          |
|--------|-------------------------------|----------------------------------|
| GET    | `/api/materials`              | List all (optional filter)       |
| GET    | `/api/materials?material_type=fabric` | List filtered by type    |
| POST   | `/api/materials`              | Create a material                |
| GET    | `/api/materials/<id>`         | Read one material                |
| PUT    | `/api/materials/<id>`         | Update one material              |
| DELETE | `/api/materials/<id>`         | Delete one material              |

### Create example

```bash
curl -X POST http://localhost:8069/api/materials \
  -H "Content-Type: application/json" \
  -b session_cookie.txt \
  -d '{
    "code": "MAT-010",
    "name": "Blue Denim",
    "material_type": "jeans",
    "buy_price": 250,
    "supplier_id": 1
  }'
```

### Filter by type

```bash
curl -b session_cookie.txt \
  "http://localhost:8069/api/materials?material_type=cotton"
```

Error responses: `400` for validation failures (e.g. buy price < 100,
bad JSON), `404` for a missing material or unknown type on read, `500`
for anything unexpected.

## Install

Copy `material_registration/` into your Odoo 14 addons path, then:

```bash
./odoo-bin -d <db> -i material_registration
```

## Run tests

```bash
./odoo-bin -d <db> -i material_registration --test-enable --stop-after-init
```

Tests live in `material_registration/tests/`:

- `test_material.py` — domain entity + invariants (price, unique code, selection)
- `test_material_service.py` — every use case (CRUD + filter, error paths)
