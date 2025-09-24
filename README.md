# SPRAXXX Pantry

**Date:** September 24, 2025  
**Founder / Inventor:** Jacquot Maple Monster Periard Raymond  
**Organization:** SPRAXXX Legacy Foundation  

---

## Purpose

SPRAXXX Pantry is a **nonprofit, charitable system** designed to redirect automated digital processes (bots, scripts, AI routines) into **productive computation for the public good**.  

It is built to:  
1. Reduce wasted digital energy and global inefficiency.  
2. Generate computation for nonprofit projects, research, and societal benefit.  
3. Provide transparent, auditable acknowledgment of contributions.  
4. Serve humanity, not profit, with ethical AI governance.

---

## Ethical and Usage Rules

- **Nonprofit Only:** SPRAXXX Pantry outputs cannot be monetized or commercialized.  
- **Consistency:** All references must be spelled **SPRAXXX** exactly.  
- **Accountability:** Contributions must be logged in an auditable format.  
- **Separation from Profit:** All outputs remain strictly for charitable purposes.  
- **Moral Ownership:** Any attempt to exploit SPRAXXX Pantry is considered theft of a charitable invention.

---

## Quick Start - Running the Simulation

To run the SPRAXXX Pantry simulation:

### Option 1: From repository root
```bash
python run_simulation.py
```

### Option 2: From src directory
```bash
cd src
python main.py
```

The simulation will demonstrate the complete workflow:
1. Initialize all modules (Greeter, Kitchen, YieldQueue, CreditLedger, Governance)
2. Process incoming bots and classify them as workers
3. Generate nonprofit outputs through safe processing
4. Store results in yield queue and log contributions
5. Display final results showing yield contents and credit ledger entries

---

## Repository Structure

```
├── src/                    # Core modules
│   ├── main.py            # Main simulation runner
│   ├── greeter.py         # Bot detection and classification
│   ├── kitchen.py         # Safe processing sandbox
│   ├── yield_queue.py     # Output storage for nonprofit use
│   ├── credit_ledger.py   # Contribution logging
│   └── governance.py      # Ethical compliance validation
├── docs/                  # Documentation
│   ├── modules.md         # Module descriptions
│   ├── ethics.md          # Ethical guidelines
│   └── simulations.md     # Simulation documentation
├── run_simulation.py      # Simulation runner from root
├── Contributing.md        # Contribution guidelines
└── README.md             # This file
```
