# ADR-001: Use String Literals for Shipment Status Instead of an Enum

## Status
Accepted

## Context
`compute_status()` needs to return one of three shipment states —
`on_time`, `minor_delay`, or `major_delay` — based on `delay_days`.
This value is stored directly in `shipments_db` and returned as-is in
the API response body via FastAPI, so whatever type is chosen here
becomes part of the API's public contract with any client consuming it.

## Decision
Return plain string literals (`'on_time'`, `'minor_delay'`,
`'major_delay'`) from `compute_status()`, rather than a Python `Enum`
or integer status code.

## Alternatives Considered
- **Python `Enum`** (e.g. `class ShipmentStatus(Enum): ...`): gives
  type safety and IDE autocomplete in code, but FastAPI/Pydantic needs
  extra serialization handling to turn an Enum member into clean JSON,
  and it adds an import and a layer of abstraction for little practical
  gain at this stage of the project.
- **Integer status codes** (`0`, `1`, `2`): more compact on the wire,
  but meaningless to a human reading a raw API response or a log line
  without a separate lookup table mapping numbers back to meaning.

## Consequences
Loses compile-time protection against typos in status strings — nothing
currently stops a future caller or contributor from writing `'on-time'`
instead of `'on_time'` and silently breaking a client's status check.
In exchange, the API response stays self-explanatory with zero
serialization logic required, which matters more while the service is
this small and the status values are unlikely to change often.
