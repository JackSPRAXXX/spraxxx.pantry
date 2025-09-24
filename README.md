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

## Repository Structure

```
SPRAXXX Pantry/
├── src/
│   ├── main.py              # Main simulation with visual outputs
│   ├── greeter.py           # Bot detection and classification
│   ├── kitchen.py           # Safe processing sandbox
│   ├── yield_queue.py       # Output storage for nonprofit use
│   ├── credit_ledger.py     # Contribution logging
│   ├── governance.py        # Ethical compliance validation
│   ├── visualization.py     # Visual analytics module
│   └── main_with_visuals.py # Enhanced simulation example
├── docs/                    # Documentation and guidelines
├── visualizations/          # Generated charts and graphs
└── README.md               # This file
```

## Getting Started

### Basic Simulation

Run the basic SPRAXXX Pantry simulation:

```bash
cd src
python main.py
```

This will process mock bots and display text results. Visual charts will be generated automatically if matplotlib is installed.

### Visual Analytics

To generate bar charts and line graphs showing yield production and credit balances:

1. **Install visualization dependencies:**
   ```bash
   pip install matplotlib
   ```

2. **Run the simulation:**
   ```bash
   python src/main.py
   ```

3. **View generated visualizations:**
   - Check the `visualizations/` directory for PNG files
   - **Bar Chart:** Shows yield production by each bot
   - **Line Graph:** Displays credit balance accumulation over time

### Enhanced Simulation

For more advanced features including custom bot configurations:

```bash
python src/main_with_visuals.py
```

## Visual Outputs

The SPRAXXX Pantry system generates two types of visual analytics:

### 1. Yield Queue Bar Chart
**Purpose:** Depicts yield production by each bot in the simulation  
**Features:**
- Individual bot yield counts
- Color-coded bars for easy identification
- Nonprofit disclaimer included
- Saved as high-resolution PNG

### 2. Credit Ledger Line Graph
**Purpose:** Illustrates credit balance accumulation over time  
**Features:**
- Multi-bot timeline tracking
- Cumulative credit progression
- Time-based x-axis with proper formatting
- Legend for bot identification

## Adding Custom Bots

You can extend the simulation with specialized bots:

```python
# Example: Adding research and educational bots
custom_bots = [
    {
        "bot_id": "research_bot_alpha",
        "type": "academic_researcher", 
        "yield_multiplier": 1.5,
        "specialization": "climate_data"
    },
    {
        "bot_id": "education_bot_beta",
        "type": "educational_content",
        "yield_multiplier": 1.2,
        "specialization": "stem_tutorials"
    }
]
```

### Integration Steps:
1. Add bot IDs to the `incoming_bots` list in `main.py`
2. Modify `Kitchen.process_worker()` to handle specialized types
3. Update `YieldQueue` to track yield multipliers
4. Run simulation to see enhanced visual outputs

## Technical Requirements

- **Python 3.7+**
- **matplotlib** (for visualizations): `pip install matplotlib`
- **numpy** (automatically installed with matplotlib)

## Output Files

All generated visualizations are saved to the `visualizations/` directory:
- `spraxxx_yield_chart_[timestamp].png` - Yield production bar chart
- `spraxxx_credit_graph_[timestamp].png` - Credit balance line graph

**Note:** All visual outputs include nonprofit disclaimers and SPRAXXX branding.
