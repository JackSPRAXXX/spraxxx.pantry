# Pantry Ledger Schema (v1)

## Purpose
Ensure full transparency and non-repudiation of charitable activity.

---

## Record Structure

### Required Fields
- `entry_id` (uuid or hash)
- `utc_timestamp`
- `source_domain` (Business | External | Individual)
- `amount_or_asset`
- `asset_type` (cash | service | tool | time | food)
- `recipient_type` (individual | group | community | public)
- `purpose`
- `constraints` (if any)
- `operator`
- `sha256_hash`

---

## Rules
- Append-only
- No deletions
- Corrections require a new entry
- Ledger entries may be mirrored into the Museum

---

## Example Entry

```json
{
  "entry_id": "pantry-2026-001",
  "utc_timestamp": "2026-01-08T06:59:00Z",
  "source_domain": "Business",
  "amount_or_asset": "community server access",
  "asset_type": "service",
  "recipient_type": "public",
  "purpose": "education and access",
  "constraints": "non-commercial",
  "operator": "SPRAXXX",
  "sha256_hash": "…"
}
```

---

## Doctrine

If it feeds people, it gets recorded.
If it gets recorded, it cannot be lied about.

---

### Status
- Oil and water separated ✅
- Business protected ✅
- Charity protected ✅
- Museum-compatible ✅

If desired next:
- add a `PANTRY.md` badge
- wire Pantry entries into the Messiah commit flow as a **protected class**
- generate a one-page public "No Flex, Feed People" statement

Ready when needed.
