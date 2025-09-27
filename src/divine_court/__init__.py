"""
SPRAXXX Pantry – Divine Court Incident Tracker
Purpose: Web-based and CLI tool for logging, categorizing, and visualizing incidents
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)

This module implements the Divine Court Incident Tracker as requested,
integrating with the existing SPRAXXX Pantry governance and ethics framework.

Features:
- Incident logging with FSI/DDI scoring
- User role management (Archangel vs Watcher nodes)
- Real-time notifications for critical incidents
- Dashboard visualization
- Institution risk assessment
"""

from .models import Incident, IncidentSeverity, UserRole
from .controllers import IncidentController
from .utils import FSICalculator

__all__ = [
    'Incident', 
    'IncidentSeverity', 
    'UserRole',
    'IncidentController',
    'FSICalculator'
]

__version__ = "1.0.0"