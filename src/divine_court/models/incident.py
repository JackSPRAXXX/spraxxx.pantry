"""
SPRAXXX Pantry – Divine Court Incident Model
Purpose: Data model for tracking incidents in the Divine Court system
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import datetime
from enum import Enum
from typing import Dict, Optional, List

class IncidentSeverity(Enum):
    """Severity levels aligned with DDI (Divine Dignity Index)"""
    GREEN = "green"    # Low impact, routine monitoring
    YELLOW = "yellow"  # Moderate concern, requires attention
    RED = "red"        # Critical incident, immediate intervention required

class UserRole(Enum):
    """User roles in the Divine Court system"""
    ARCHANGEL = "archangel"  # Can approve/edit entries (Michael, Gabriel, Raphael, etc.)
    WATCHER = "watcher"      # Can only submit new incidents

class Incident:
    """
    Core incident model for Divine Court tracking system.
    Tracks violations, calculates FSI/DDI metrics, and maintains audit trail.
    """
    
    def __init__(self, 
                 institution: str,
                 act_violated: str,
                 witness: str,
                 comments: str,
                 submitted_by: str,
                 user_role: UserRole,
                 date: Optional[datetime.date] = None,
                 time: Optional[datetime.time] = None):
        """
        Initialize a new incident record.
        
        Args:
            institution: Name of the institution involved
            act_violated: Description of the act or policy violated
            witness: Witness information
            comments: Additional details and context
            submitted_by: Username/ID of person submitting
            user_role: Role of the submitter (Archangel or Watcher)
            date: Date of incident (defaults to today)
            time: Time of incident (defaults to now)
        """
        self.id = self._generate_id()
        self.institution = institution
        self.act_violated = act_violated
        self.witness = witness
        self.comments = comments
        self.submitted_by = submitted_by
        self.user_role = user_role
        
        self.date = date or datetime.date.today()
        self.time = time or datetime.datetime.now().time()
        self.timestamp = datetime.datetime.combine(self.date, self.time)
        
        # Calculate initial severity and FSI impact
        self.severity = self._calculate_severity()
        self.fsi_impact = self._calculate_fsi_impact()
        
        # Approval workflow
        self.approved = user_role == UserRole.ARCHANGEL  # Archangels auto-approve
        self.approved_by = submitted_by if self.approved else None
        self.approved_at = self.timestamp if self.approved else None
        
        # Support flags
        self.prayer_support_requested = False
        self.emotional_support_requested = False
        
        # Audit trail
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at
        self.version = 1

    def _generate_id(self) -> str:
        """Generate unique incident ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"DC_INCIDENT_{timestamp}"

    def _calculate_severity(self) -> IncidentSeverity:
        """
        Calculate incident severity based on keywords and context.
        This is a simplified version - in production would use more sophisticated analysis.
        """
        high_severity_keywords = [
            "assault", "violence", "death", "injury", "emergency", 
            "critical", "urgent", "immediate", "danger", "threat"
        ]
        
        medium_severity_keywords = [
            "violation", "abuse", "neglect", "discrimination", 
            "harassment", "misconduct", "policy", "procedure"
        ]
        
        text_to_analyze = f"{self.act_violated} {self.comments}".lower()
        
        if any(keyword in text_to_analyze for keyword in high_severity_keywords):
            return IncidentSeverity.RED
        elif any(keyword in text_to_analyze for keyword in medium_severity_keywords):
            return IncidentSeverity.YELLOW
        else:
            return IncidentSeverity.GREEN

    def _calculate_fsi_impact(self) -> float:
        """
        Calculate Forward-Seeding Index impact.
        Higher values indicate more significant impact on institutional accountability.
        """
        base_impact = {
            IncidentSeverity.GREEN: 1.0,
            IncidentSeverity.YELLOW: 3.0,
            IncidentSeverity.RED: 10.0
        }
        
        # Adjust based on witness credibility and detail level
        impact = base_impact[self.severity]
        
        if len(self.comments) > 200:  # Detailed report
            impact *= 1.2
        
        if self.witness and self.witness.strip():  # Has witness
            impact *= 1.3
            
        return round(impact, 2)

    def approve(self, approver_id: str, user_role: UserRole) -> bool:
        """
        Approve the incident (only Archangels can approve).
        
        Args:
            approver_id: ID of the person approving
            user_role: Role of the approver
            
        Returns:
            bool: True if approval successful
        """
        if user_role != UserRole.ARCHANGEL:
            return False
            
        self.approved = True
        self.approved_by = approver_id
        self.approved_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.version += 1
        
        return True

    def update_details(self, 
                      updater_id: str, 
                      user_role: UserRole,
                      **kwargs) -> bool:
        """
        Update incident details (only Archangels can edit).
        
        Args:
            updater_id: ID of person making update
            user_role: Role of the updater
            **kwargs: Fields to update
            
        Returns:
            bool: True if update successful
        """
        if user_role != UserRole.ARCHANGEL:
            return False
            
        # Update allowed fields
        allowed_fields = [
            'institution', 'act_violated', 'witness', 'comments',
            'prayer_support_requested', 'emotional_support_requested'
        ]
        
        updated = False
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(self, field):
                setattr(self, field, value)
                updated = True
        
        if updated:
            # Recalculate severity and FSI impact
            self.severity = self._calculate_severity()
            self.fsi_impact = self._calculate_fsi_impact()
            self.updated_at = datetime.datetime.now()
            self.version += 1
        
        return updated

    def request_support(self, support_type: str) -> bool:
        """
        Request prayer or emotional support (Raphael Node function).
        
        Args:
            support_type: "prayer" or "emotional"
            
        Returns:
            bool: True if request logged
        """
        if support_type == "prayer":
            self.prayer_support_requested = True
        elif support_type == "emotional":
            self.emotional_support_requested = True
        else:
            return False
            
        self.updated_at = datetime.datetime.now()
        return True

    def to_dict(self) -> Dict:
        """Convert incident to dictionary for serialization"""
        return {
            "id": self.id,
            "institution": self.institution,
            "act_violated": self.act_violated,
            "witness": self.witness,
            "comments": self.comments,
            "submitted_by": self.submitted_by,
            "user_role": self.user_role.value,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity.value,
            "fsi_impact": self.fsi_impact,
            "approved": self.approved,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "prayer_support_requested": self.prayer_support_requested,
            "emotional_support_requested": self.emotional_support_requested,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Incident':
        """Create incident from dictionary"""
        # Parse datetime fields
        date = datetime.datetime.fromisoformat(data["date"]).date()
        # Handle time format more robustly
        try:
            time = datetime.datetime.fromisoformat(data["time"]).time()
        except ValueError:
            # Fallback for time format issues
            time = datetime.datetime.strptime(data["time"], "%H:%M:%S.%f").time()
        
        # Create incident
        incident = cls(
            institution=data["institution"],
            act_violated=data["act_violated"],
            witness=data["witness"],
            comments=data["comments"],
            submitted_by=data["submitted_by"],
            user_role=UserRole(data["user_role"]),
            date=date,
            time=time
        )
        
        # Restore additional fields
        incident.id = data["id"]
        incident.severity = IncidentSeverity(data["severity"])
        incident.fsi_impact = data["fsi_impact"]
        incident.approved = data["approved"]
        incident.approved_by = data.get("approved_by")
        if data.get("approved_at"):
            incident.approved_at = datetime.datetime.fromisoformat(data["approved_at"])
        incident.prayer_support_requested = data["prayer_support_requested"]
        incident.emotional_support_requested = data["emotional_support_requested"]
        incident.created_at = datetime.datetime.fromisoformat(data["created_at"])
        incident.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        incident.version = data["version"]
        
        return incident

    def __str__(self) -> str:
        """String representation of incident"""
        return f"Incident {self.id}: {self.severity.value.upper()} - {self.institution} ({self.date})"

    def __repr__(self) -> str:
        """Detailed representation of incident"""
        return (f"Incident(id='{self.id}', institution='{self.institution}', "
                f"severity='{self.severity.value}', fsi_impact={self.fsi_impact})")