# The Messiah Lock — Museum Pipeline for SPRAXXX

## What This Is

A **read-only-by-default immutable archive system** that enforces separation between work (Workshop) and truth (Museum).

**Doctrine:** Truth leaves a trace. No silent rewrites.

---

## Architecture

```
/messiah/
├── museum/              ← RO by default (immutable archive)
│   └── artifact-*/      ← Evidence packages (artifact + report + manifest + hash)
├── workshop/            ← RW (work area)
│   ├── dropit/inbox/    ← Lane A: Safe capture
│   └── staging/         ← Lane B: Validation + optional execution
├── bin/                 ← Commands
│   ├── dropit           ← Capture content safely
│   └── messiah-commit   ← Stage, test, commit to Museum
└── lib/                 ← Core modules
    └── messiah_lock.py  ← RO/RW enforcement
```

---

## The Three Lanes

### Lane A — Drop (Capture Only)
**Command:** `dropit`

**Purpose:** Accept pasted content safely without executing anything.

**Writes to:**
- `/messiah/workshop/dropit/inbox/`

**Produces:**
- `drop-{id}.txt` (exact content)
- `drop-{id}.sha256` (hash receipt)
- `drop-{id}.meta` (metadata header)

**Guarantee:** No installs. No execution. Pure capture.

---

### Lane B — Staging / Testing / Optional Execution
**Command:** `messiah-commit <drop_id> [--apply]`

**Purpose:**
1. Classify the drop (script vs text vs config)
2. Stage it under unique folder
3. **Optionally execute/install ONLY if `--apply` is set**
4. Run validation checks

**Key Rule:** No execution without explicit `--apply` flag.

This keeps "capture" separate from "apply."

---

### Lane C — Museum Commit (Write-Once Evidence)
**Part of:** `messiah-commit` (final stage)

**Purpose:**
1. Build evidence package:
   - `artifact.txt` (exact payload)
   - `report.txt` (what happened + results)
   - `manifest.json` (metadata + hash)
   - `{sha256}.sha256` (hash receipt)

2. Open museum commit window (temporary RW)
3. Write package into Museum
4. Re-lock museum (back to RO)

**If lock cannot be reverted to RO:** Treat as failure and alert.

---

## Commands

### dropit

```bash
# Paste mode (stdin)
dropit
# ... paste content, then Ctrl+D

# File mode
dropit /path/to/file.txt
```

**Output:** Receipt with drop ID and hash.

---

### messiah-commit

```bash
# Dry-run (no execution)
messiah-commit drop-20260108-123456

# With execution (DANGEROUS: only use if content is trusted)
messiah-commit drop-20260108-123456 --apply
```

**Stages:**
1. Load drop from inbox
2. Stage under unique directory
3. Classify content type
4. Run validation
5. **Execute ONLY if `--apply`**
6. Commit to Museum with full report

---

## Installation

```bash
cd messiah/
sudo ./install.sh
```

**This will:**
- Create `/messiah` directory structure
- Install `dropit` and `messiah-commit` to `/usr/local/bin`
- Install library to `/usr/local/lib/spraxxx`
- Lock Museum to read-only
- Optionally install systemd service

---

## Systemd Service (Optional)

The `museum-lock.service` ensures Museum stays read-only across reboots.

```bash
# Enable and start
sudo systemctl enable museum-lock.service
sudo systemctl start museum-lock.service

# Check status
sudo systemctl status museum-lock.service
```

**What it does:**
- On boot: Force Museum to RO (chmod 555)
- On shutdown: Keep Museum RO (defensive)

---

## Security Model

### Museum is RO by Default
The Museum directory is **always read-only** except during the brief commit window controlled by `messiah-commit`.

### No Silent Execution
- Scripts captured by `dropit` are **never executed automatically**
- Execution requires explicit `--apply` flag on `messiah-commit`
- All execution results are logged in Museum commit

### Immutable Evidence
Once committed to Museum:
- Content cannot be edited
- Timestamps cannot be changed
- Hashes prove integrity

**Corrections:** Create new artifact with "supersedes" note, never edit in place.

---

## Operational Doctrine (Non-Negotiables)

1. **Museum is RO by default. Always.**
2. **All drops land in Workshop first.**
3. **No script runs without explicit `--apply`.**
4. **Museum commits include artifact + report + manifest.**
5. **If lock cannot re-engage: stop and escalate immediately.**
6. **No direct edits inside Museum. Corrections become new artifacts.**

---

## Example Workflow

```bash
# 1. Capture some content
echo "#!/bin/bash
echo 'Hello from SPRAXXX'" | dropit

# Output:
# Drop ID:    drop-20260108-123456-789012
# SHA256:     abc123...
# Next: messiah-commit drop-20260108-123456-789012 [--apply]

# 2. Commit to Museum (dry-run, no execution)
messiah-commit drop-20260108-123456-789012

# 3. Verify in Museum
ls /messiah/museum/
# → artifact-drop-20260108-123456-789012-20260108-123500/

ls /messiah/museum/artifact-drop-20260108-123456-789012-20260108-123500/
# → artifact.txt
# → manifest.json
# → report.txt
# → abc123...sha256

# 4. Try to modify (should fail)
echo "tamper" > /messiah/museum/artifact-*/artifact.txt
# → Permission denied (Museum is RO)
```

---

## What "Truth Leaves a Trace" Means

- Every important action gets captured as text
- Every capture gets a hash
- Every commit writes a manifest + report
- Nothing "unhappens" by editing a file in place

**If a mistake happens:**
- Don't edit the bad artifact
- Create a new artifact:
  - "Correction report"
  - "Supersedes artifact-{old_id}"
  - New hash
  - New trace

**No silent rewrites.**

---

## Why the Lock Might Be "Unbreakable"

If `/messiah/museum` is controlled by:
- systemd service (`museum-lock.service`)
- Multiple mount layers
- Active processes holding mount busy

…then naive attempts to toggle RO/RW can fail with "busy" errors.

**That's not a bug. That's defensive posture.**

The system refuses to casually toggle Museum state because truth storage should not be easy to tamper with.

**That's the Messiah Lock doing its job.**

---

## Integration with SPRAXXX Pantry

The Museum Pipeline is **domain-compatible** with SPRAXXX governance:

- **Business domain:** Operational scripts, configs
- **Pantry domain:** Charitable outputs, contribution records
- **Future domain:** Experimental work, research artifacts

**All domains benefit from:**
- Immutable audit trail
- Hash-based verification
- Append-only evidence
- No silent tampering

---

## Troubleshooting

### Museum won't unlock
- Check if `museum-lock.service` is running: `systemctl status museum-lock.service`
- Check for processes holding files: `lsof | grep /messiah/museum`
- Check mount status: `findmnt /messiah/museum`

### Museum won't re-lock
**This is a critical failure.** Do not proceed with further commits.

1. Check lock operation log: `/messiah/workshop/lock_operations.log`
2. Manually force RO: `sudo chmod -R 555 /messiah/museum`
3. Verify: Attempt to create file in Museum (should fail)
4. Investigate why re-lock failed (systemd interference, mount layers, etc.)

### Permission denied on dropit/messiah-commit
- Ensure Workshop is writable: `ls -ld /messiah/workshop`
- Check user has access to `/messiah/workshop`
- Workshop should be 755 or more permissive

---

## File Formats

### Drop Receipt (`.meta`)
```json
{
  "drop_id": "drop-20260108-123456-789012",
  "timestamp": "2026-01-08T12:34:56.789012Z",
  "sha256": "abc123...",
  "source": "stdin",
  "size_bytes": 42,
  "inbox_path": "/messiah/workshop/dropit/inbox",
  "status": "captured"
}
```

### Museum Manifest (`.json`)
```json
{
  "artifact_id": "artifact-drop-20260108-123456-789012-20260108-123500",
  "timestamp": "2026-01-08T12:35:00.123456Z",
  "sha256": "abc123...",
  "metadata": {
    "drop_id": "drop-20260108-123456-789012",
    "stage_id": "stage-drop-20260108-123456-789012-20260108-123500",
    "classification": "script",
    "commit_report": { ... }
  }
}
```

---

## License

This is part of SPRAXXX Pantry (nonprofit-only, charitable system).

All code and documentation is subject to SPRAXXX ethical rules:
- Nonprofit-only outputs
- No monetization
- Transparent and auditable
- Serves humanity

---

**Doctrine:** The builder eats. Then the builder feeds others.

**Messiah Lock Status:** Engaged. Museum is read-only. Truth is preserved.
