# SPRAXXX Pantry – Visual Analytics Documentation

**Purpose:** Generate visual outputs for batch simulation analytics  
**Ethical:** Nonprofit-only, outputs cannot be monetized  
**Branding:** Always use SPRAXXX (S-P-R-A-X-X-X)

---

## Overview

The SPRAXXX Pantry visualization module creates two primary visual outputs:

1. **Bar Chart:** Yield Queue analysis showing production by bot
2. **Line Graph:** Credit Ledger tracking showing credit accumulation over time

All visualizations are generated with nonprofit disclaimers and maintain SPRAXXX branding consistency.

## Generated Visualizations

### Yield Queue Bar Chart
- **File naming:** `spraxxx_yield_chart_[timestamp].png`
- **Content:** Individual bot yield production counts
- **Features:**
  - Color-coded bars for each bot
  - Value labels on each bar
  - Nonprofit disclaimer at bottom
  - High-resolution PNG output (300 DPI)

### Credit Ledger Line Graph
- **File naming:** `spraxxx_credit_graph_[timestamp].png`
- **Content:** Cumulative credit balance progression over time
- **Features:**
  - Multi-line graph for multiple bots
  - Time-based x-axis with proper date formatting
  - Legend for bot identification
  - Grid overlay for readability
  - Nonprofit disclaimer at bottom

## Technical Implementation

### Dependencies
- `matplotlib` - Primary visualization library
- `numpy` - Numerical operations (installed with matplotlib)
- `datetime` - Time-based data generation

### Installation
```bash
pip install matplotlib
```

### Usage Examples

#### Basic Usage
```python
from visualization import SPRAXXXVisualizer

# Initialize visualizer
visualizer = SPRAXXXVisualizer()

# Generate yield bar chart
yield_chart = visualizer.generate_yield_bar_chart(
    yield_queue_data, bot_ids
)

# Generate credit line graph
credit_graph = visualizer.generate_credit_line_graph(
    credit_ledger_data, bot_ids
)
```

#### Complete Simulation Report
```python
# Generate both visualizations at once
report = visualizer.generate_batch_simulation_report(
    yield_queue_data, credit_ledger_data, bot_ids
)
```

### Custom Bot Integration

The visualization module supports custom bot configurations:

```python
custom_bots = [
    {
        "bot_id": "research_bot_alpha",
        "type": "academic_researcher", 
        "yield_multiplier": 1.5,
        "specialization": "climate_data"
    }
]
```

Visual outputs will automatically adapt to include custom bots in charts and graphs.

## File Organization

```
visualizations/
├── spraxxx_yield_chart_20240924_084556.png
├── spraxxx_credit_graph_20240924_084556.png
└── spraxxx_batch_report_[timestamp]_*.png
```

## Error Handling

The visualization module includes robust error handling:

- **Missing matplotlib:** Graceful degradation with informative messages
- **Invalid data:** Clear error reporting with suggested fixes
- **File system issues:** Automatic directory creation and permission checks

## Ethical Compliance

All generated visualizations include:
- ✅ Nonprofit-only disclaimers
- ✅ SPRAXXX branding consistency
- ✅ Transparent data sourcing
- ✅ Charitable purpose statements

## Future Enhancements

Planned visualization improvements:
- **Interactive charts** using Plotly
- **Dashboard generation** with multiple metrics
- **Export to PDF** for reporting
- **Real-time updates** for live simulations

---

> **Remember:** All SPRAXXX Pantry outputs are for nonprofit use only and cannot be monetized.  
> SPRAXXX Legacy Foundation - Serving Humanity Through Technology