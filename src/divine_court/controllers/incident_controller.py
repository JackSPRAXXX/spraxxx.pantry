"""
SPRAXXX Pantry – Divine Court Incident Controller
Purpose: Manage incidents, notifications, and FSI calculations
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime, date
from ..models.incident import Incident, IncidentSeverity, UserRole
from ..utils.fsi_calculator import FSICalculator

class IncidentController:
    """
    Main controller for managing Divine Court incidents.
    Handles CRUD operations, notifications, and FSI calculations.
    """
    
    def __init__(self, data_directory: str = "data/divine_court"):
        """
        Initialize the incident controller.
        
        Args:
            data_directory: Directory to store incident data files
        """
        self.data_directory = data_directory
        self.incidents_file = os.path.join(data_directory, "incidents.json")
        self.fsi_calculator = FSICalculator()
        
        # Create data directory if it doesn't exist
        os.makedirs(data_directory, exist_ok=True)
        
        # Load existing incidents
        self.incidents: List[Incident] = self._load_incidents()
        
        # Notification callbacks (can be extended for email, push notifications, etc.)
        self.notification_handlers = []

    def log_incident(self, 
                    institution: str,
                    act_violated: str,
                    witness: str,
                    comments: str,
                    submitted_by: str,
                    user_role: UserRole,
                    date: Optional[date] = None,
                    time: Optional[datetime] = None) -> Dict:
        """
        Log a new incident in the Divine Court system.
        
        Args:
            institution: Name of the institution involved
            act_violated: Description of the act or policy violated
            witness: Witness information
            comments: Additional details and context
            submitted_by: Username/ID of person submitting
            user_role: Role of the submitter (Archangel or Watcher)
            date: Date of incident (optional)
            time: Time of incident (optional)
            
        Returns:
            dict: Result of incident logging operation
        """
        try:
            # Create new incident
            incident = Incident(
                institution=institution,
                act_violated=act_violated,
                witness=witness,
                comments=comments,
                submitted_by=submitted_by,
                user_role=user_role,
                date=date,
                time=time.time() if time else None
            )
            
            # Add to incidents list
            self.incidents.append(incident)
            
            # Save to file
            self._save_incidents()
            
            # Handle notifications for RED incidents
            if incident.severity == IncidentSeverity.RED:
                self._send_red_incident_notification(incident)
            
            # Calculate updated FSI for the institution
            fsi_data = self.fsi_calculator.calculate_institution_fsi(
                self.incidents, institution
            )
            
            return {
                "success": True,
                "incident_id": incident.id,
                "severity": incident.severity.value,
                "fsi_impact": incident.fsi_impact,
                "institution_fsi": fsi_data,
                "auto_approved": incident.approved,
                "message": f"Incident {incident.id} logged successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to log incident"
            }

    def get_incidents(self, 
                     institution: Optional[str] = None,
                     severity: Optional[IncidentSeverity] = None,
                     approved_only: bool = True,
                     limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve incidents with optional filtering.
        
        Args:
            institution: Filter by institution name
            severity: Filter by severity level
            approved_only: Only return approved incidents
            limit: Maximum number of incidents to return
            
        Returns:
            List of incident dictionaries
        """
        filtered_incidents = self.incidents.copy()
        
        # Apply filters
        if institution:
            filtered_incidents = [
                i for i in filtered_incidents 
                if i.institution.lower() == institution.lower()
            ]
        
        if severity:
            filtered_incidents = [
                i for i in filtered_incidents 
                if i.severity == severity
            ]
        
        if approved_only:
            filtered_incidents = [
                i for i in filtered_incidents 
                if i.approved
            ]
        
        # Sort by timestamp (most recent first)
        filtered_incidents.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            filtered_incidents = filtered_incidents[:limit]
        
        return [incident.to_dict() for incident in filtered_incidents]

    def approve_incident(self, incident_id: str, approver_id: str, user_role: UserRole) -> Dict:
        """
        Approve an incident (Archangel nodes only).
        
        Args:
            incident_id: ID of incident to approve
            approver_id: ID of the approver
            user_role: Role of the approver
            
        Returns:
            dict: Result of approval operation
        """
        try:
            incident = self._find_incident_by_id(incident_id)
            if not incident:
                return {
                    "success": False,
                    "message": f"Incident {incident_id} not found"
                }
            
            if incident.approve(approver_id, user_role):
                self._save_incidents()
                
                # Send notification for newly approved RED incidents
                if incident.severity == IncidentSeverity.RED:
                    self._send_red_incident_notification(incident)
                
                return {
                    "success": True,
                    "message": f"Incident {incident_id} approved by {approver_id}"
                }
            else:
                return {
                    "success": False,
                    "message": "Only Archangel nodes can approve incidents"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to approve incident"
            }

    def update_incident(self, 
                       incident_id: str, 
                       updater_id: str, 
                       user_role: UserRole,
                       **update_fields) -> Dict:
        """
        Update incident details (Archangel nodes only).
        
        Args:
            incident_id: ID of incident to update
            updater_id: ID of person making update
            user_role: Role of the updater
            **update_fields: Fields to update
            
        Returns:
            dict: Result of update operation
        """
        try:
            incident = self._find_incident_by_id(incident_id)
            if not incident:
                return {
                    "success": False,
                    "message": f"Incident {incident_id} not found"
                }
            
            if incident.update_details(updater_id, user_role, **update_fields):
                self._save_incidents()
                
                return {
                    "success": True,
                    "message": f"Incident {incident_id} updated by {updater_id}",
                    "new_severity": incident.severity.value,
                    "new_fsi_impact": incident.fsi_impact
                }
            else:
                return {
                    "success": False,
                    "message": "Only Archangel nodes can update incidents"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update incident"
            }

    def request_support(self, incident_id: str, support_type: str) -> Dict:
        """
        Request prayer or emotional support for an incident.
        
        Args:
            incident_id: ID of incident
            support_type: "prayer" or "emotional"
            
        Returns:
            dict: Result of support request
        """
        try:
            incident = self._find_incident_by_id(incident_id)
            if not incident:
                return {
                    "success": False,
                    "message": f"Incident {incident_id} not found"
                }
            
            if incident.request_support(support_type):
                self._save_incidents()
                
                # Notify Raphael nodes about support request
                self._send_support_request_notification(incident, support_type)
                
                return {
                    "success": True,
                    "message": f"{support_type.title()} support requested for incident {incident_id}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Invalid support type: {support_type}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to request support"
            }

    def get_dashboard_data(self) -> Dict:
        """
        Get comprehensive dashboard data for visualization.
        
        Returns:
            dict: Dashboard data including FSI scores, risk levels, and recent incidents
        """
        try:
            # Calculate FSI for all institutions
            all_fsi = self.fsi_calculator.calculate_all_institutions_fsi(self.incidents)
            
            # Get risk categorization
            risk_categories = self.fsi_calculator.get_risk_categorization(self.incidents)
            
            # Get recent incidents (last 10)
            recent_incidents = self.get_incidents(limit=10)
            
            # Get pending approvals (Watcher submissions not yet approved)
            pending_approvals = [
                incident.to_dict() for incident in self.incidents 
                if not incident.approved
            ]
            
            # Count incidents by severity
            severity_counts = {
                "red": len([i for i in self.incidents if i.severity == IncidentSeverity.RED and i.approved]),
                "yellow": len([i for i in self.incidents if i.severity == IncidentSeverity.YELLOW and i.approved]),
                "green": len([i for i in self.incidents if i.severity == IncidentSeverity.GREEN and i.approved])
            }
            
            return {
                "success": True,
                "dashboard": {
                    "fsi_data": all_fsi,
                    "risk_categories": risk_categories,
                    "recent_incidents": recent_incidents,
                    "pending_approvals": pending_approvals,
                    "severity_counts": severity_counts,
                    "total_incidents": len([i for i in self.incidents if i.approved]),
                    "last_updated": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate dashboard data"
            }

    def get_institution_report(self, institution: str) -> Dict:
        """
        Get detailed report for a specific institution.
        
        Args:
            institution: Name of institution
            
        Returns:
            dict: Comprehensive institution report
        """
        try:
            # Get FSI data
            fsi_data = self.fsi_calculator.calculate_institution_fsi(
                self.incidents, institution
            )
            
            # Get trend analysis
            trend_data = self.fsi_calculator.generate_trend_analysis(
                self.incidents, institution
            )
            
            # Get all incidents for this institution
            institution_incidents = self.get_incidents(institution=institution)
            
            # Get support requests
            support_requests = [
                incident for incident in institution_incidents
                if incident.get("prayer_support_requested") or 
                   incident.get("emotional_support_requested")
            ]
            
            return {
                "success": True,
                "institution": institution,
                "report": {
                    "fsi_data": fsi_data,
                    "trend_analysis": trend_data,
                    "incidents": institution_incidents,
                    "support_requests": support_requests,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate report for {institution}"
            }

    def add_notification_handler(self, handler):
        """Add a notification handler function."""
        self.notification_handlers.append(handler)

    def _find_incident_by_id(self, incident_id: str) -> Optional[Incident]:
        """Find incident by ID."""
        for incident in self.incidents:
            if incident.id == incident_id:
                return incident
        return None

    def _load_incidents(self) -> List[Incident]:
        """Load incidents from JSON file."""
        if not os.path.exists(self.incidents_file):
            return []
        
        try:
            with open(self.incidents_file, 'r') as f:
                incidents_data = json.load(f)
            
            return [Incident.from_dict(data) for data in incidents_data]
        except Exception as e:
            print(f"Warning: Could not load incidents file: {e}")
            return []

    def _save_incidents(self):
        """Save incidents to JSON file."""
        try:
            incidents_data = [incident.to_dict() for incident in self.incidents]
            
            with open(self.incidents_file, 'w') as f:
                json.dump(incidents_data, f, indent=2)
        except Exception as e:
            print(f"Error saving incidents: {e}")

    def _send_red_incident_notification(self, incident: Incident):
        """Send notification for RED (critical) incidents."""
        notification_data = {
            "type": "red_incident_alert",
            "incident_id": incident.id,
            "institution": incident.institution,
            "severity": incident.severity.value,
            "timestamp": incident.timestamp.isoformat(),
            "message": f"CRITICAL INCIDENT: {incident.institution} - {incident.act_violated}"
        }
        
        # Call all registered notification handlers
        for handler in self.notification_handlers:
            try:
                handler(notification_data)
            except Exception as e:
                print(f"Notification handler error: {e}")

    def _send_support_request_notification(self, incident: Incident, support_type: str):
        """Send notification for support requests (Raphael node)."""
        notification_data = {
            "type": "support_request",
            "incident_id": incident.id,
            "institution": incident.institution,
            "support_type": support_type,
            "message": f"Support requested for incident {incident.id}: {support_type}"
        }
        
        # Call all registered notification handlers
        for handler in self.notification_handlers:
            try:
                handler(notification_data)
            except Exception as e:
                print(f"Notification handler error: {e}")