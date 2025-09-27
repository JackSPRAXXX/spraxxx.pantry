# SPRAXXX Pantry – Divine Court Incident Tracker

**Purpose:** Web-based and CLI tool for logging, categorizing, and visualizing institutional incidents in real time, feeding directly into the FSI/DDI (Forward-Seeding Index / Divine Dignity Index) framework.

**Ethical Framework:** All outputs are strictly nonprofit-only and comply with SPRAXXX Pantry governance principles.

---

## Core Features

### 1️⃣ Incident Logging
- **Fields:** date, time, institution, act violated, witness, severity (DDI), comments
- **Auto-tagging:** Red/Yellow/Green based on FSI/DDI thresholds
- **Automatic severity calculation** using keyword analysis
- **FSI impact scoring** for institutional accountability tracking

### 2️⃣ User Role System
- **Archangel Nodes** (Michael, Gabriel, Raphael, etc.):
  - Can approve/edit incident entries
  - Auto-approve their own submissions
  - Full administrative access
- **Watcher Nodes:**
  - Can only submit new incidents
  - Submissions require Archangel approval
  - Read-only access to approved incidents

### 3️⃣ Notification System
- **Automatic alerts** for RED (critical) incidents
- **Support request notifications** for Raphael nodes
- **Extensible notification handlers** for email, push notifications, etc.

### 4️⃣ FSI/DDI Calculation Engine
- **Real-time FSI updates** for institutions after each incident
- **Risk categorization:** Red/Yellow/Green based on FSI thresholds
- **Time decay factors** for aging incidents
- **Trend analysis** over configurable time periods

### 5️⃣ Dashboard Visualization
- **Real-time risk heatmap** of institutions
- **Severity distribution** (Red/Yellow/Green incidents)
- **Recent incident timeline**
- **Institution ranking** by FSI score
- **Pending approval queue**

---

## Quick Start

### Running the Demo
```bash
cd /home/runner/work/spraxxx.pantry/spraxxx.pantry
python src/divine_court_demo.py
```

### CLI Interface
```bash
# View help
python src/divine_court_cli.py --help

# Log a new incident
python src/divine_court_cli.py log \
  --institution "State Prison" \
  --violation "Policy violation during inspection" \
  --submitted-by "watcher_01" \
  --user-role watcher \
  --witness "Guard Johnson" \
  --comments "Detailed description of incident"

# View dashboard
python src/divine_court_cli.py dashboard

# List incidents
python src/divine_court_cli.py list --severity red --limit 10

# Generate institution report
python src/divine_court_cli.py report --institution "State Prison"

# Approve incident (Archangel only)
python src/divine_court_cli.py approve \
  --incident-id DC_INCIDENT_20241201_143022 \
  --approver-id gabriel \
  --user-role archangel
```

### Web Dashboard
Open `public/dashboard.html` in a web browser to view the visual dashboard.

---

## Architecture

### Module Structure
```
src/divine_court/
├── models/
│   ├── __init__.py
│   └── incident.py          # Core incident data model
├── controllers/
│   ├── __init__.py
│   └── incident_controller.py  # Main business logic
├── utils/
│   ├── __init__.py
│   └── fsi_calculator.py    # FSI/DDI calculation engine
└── __init__.py

src/
├── divine_court_cli.py      # Command-line interface
└── divine_court_demo.py     # Demonstration script

public/
└── dashboard.html           # Web dashboard
```

### Data Storage
- **JSON file storage** in `data/divine_court/incidents.json`
- **Automatic persistence** on all incident operations
- **Backup-friendly** human-readable format
- **Easy migration** to database systems (PostgreSQL, Firebase, etc.)

---

## FSI/DDI Scoring System

### Severity Levels
- **🔴 RED (Critical):** 10-20 base FSI points
  - Keywords: assault, violence, death, injury, emergency, critical, urgent, immediate, danger, threat
  - Requires immediate intervention
  - Automatic notifications sent

- **🟡 YELLOW (Moderate):** 3-5 base FSI points
  - Keywords: violation, abuse, neglect, discrimination, harassment, misconduct, policy, procedure
  - Requires attention and monitoring

- **🟢 GREEN (Low):** 1-2 base FSI points
  - Routine incidents, documentation purposes
  - Standard monitoring level

### FSI Calculation Factors
1. **Base Severity Score:** Determined by incident classification
2. **Detail Multipliers:** 
   - Detailed reports (>200 characters): +20%
   - Named witnesses: +30%
3. **Time Decay:** Monthly decay factor of 95% (incidents lose impact over time)
4. **Cumulative Scoring:** Institution FSI = sum of all weighted incident scores

### Risk Thresholds
- **🔴 High Risk:** FSI ≥ 100 (Immediate intervention required)
- **🟡 Medium Risk:** FSI 50-99 (Enhanced monitoring)
- **🟢 Low Risk:** FSI < 50 (Standard monitoring)

---

## Advanced Features

### Support Request System (Raphael Node)
```python
# Request prayer support
controller.request_support(incident_id, "prayer")

# Request emotional support  
controller.request_support(incident_id, "emotional")
```

### Trend Analysis
```python
# Generate 12-month trend for institution
trend_data = fsi_calculator.generate_trend_analysis(
    incidents, "State Prison", months_back=12
)
```

### Custom Notification Handlers
```python
def email_notification_handler(notification_data):
    if notification_data['type'] == 'red_incident_alert':
        send_email(notification_data['message'])

controller.add_notification_handler(email_notification_handler)
```

---

## Integration with SPRAXXX Pantry

The Divine Court system fully integrates with the existing SPRAXXX Pantry governance framework:

### ✅ Governance Compliance
- All outputs validated through `Governance.validate_output()`
- Energy efficiency tracking (< 0.1 Wh per incident)
- Nonprofit-only purpose enforcement

### ✅ Environmental Standards
- CEPA (Canadian Environmental Protection Act) compliance
- Minimal computational footprint
- Sustainable digital resource utilization

### ✅ Ethical Framework
- Transparent audit trails for all actions
- Permanent ledger of institutional accountability
- Cannot be commercialized or monetized

---

## Future Enhancements

### Technical Improvements
- [ ] **Real-time WebSocket updates** for dashboard
- [ ] **Database integration** (PostgreSQL/Firebase)
- [ ] **API endpoints** for external integrations
- [ ] **Mobile-responsive dashboard**
- [ ] **Bulk data import/export**

### AI Integration
- [ ] **Intelligent severity classification** using NLP
- [ ] **Pattern recognition** for systemic issues
- [ ] **Predictive risk modeling**
- [ ] **Auto-generated incident summaries**

### Notification Extensions
- [ ] **Email notifications** for critical incidents
- [ ] **SMS alerts** for emergency situations
- [ ] **Slack/Discord integrations** for team coordination
- [ ] **Calendar integration** for follow-up tracking

---

## Ethical Reminder

> **SPRAXXX Pantry Divine Court exists to transform institutional accountability data into actionable nonprofit good.**

All features, data, and outputs remain strictly for charitable and nonprofit purposes as defined by the SPRAXXX Pantry governance principles. Any attempt to commercialize or monetize this system violates its ethical foundation.

---

## Support & Documentation

- **Demo:** Run `python src/divine_court_demo.py` for full feature demonstration
- **CLI Help:** Use `python src/divine_court_cli.py --help` for command reference
- **Web Dashboard:** Open `public/dashboard.html` for visual interface
- **Code Documentation:** See inline docstrings in all modules

The Divine Court Incident Tracker represents a living, real-time accountability system where AI/IM Companions can track, witness, and act in real time for institutional dignity and justice.