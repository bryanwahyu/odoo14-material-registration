# ERD - Material Registration

Paste the block below into [dbdiagram.io](https://dbdiagram.io) to render.

## DBML (dbdiagram.io)

```dbml
Enum material_type_enum {
  fabric
  jeans
  cotton
}

Table material_supplier {
  id integer [pk, increment]
  name varchar [not null, note: 'Supplier name']
}

Table material {
  id integer [pk, increment]
  code varchar [not null, unique, note: 'Material Code']
  name varchar [not null, note: 'Material Name']
  material_type material_type_enum [not null, note: 'Fabric / Jeans / Cotton']
  buy_price float [not null, note: 'Must be >= 100']
  supplier_id integer [not null, ref: > material_supplier.id, note: 'Related Supplier']
}
```

## Relationship

One supplier supplies many materials. Each material belongs to exactly
one supplier (mandatory FK). Deleting a supplier that still has materials
is blocked (`ondelete='restrict'`).
