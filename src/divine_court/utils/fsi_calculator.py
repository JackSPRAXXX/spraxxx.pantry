"""
SPRAXXX Pantry – FSI Calculator Utility
Purpose: Calculate Forward-Seeding Index for institutions based on incidents
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from typing import List, Dict, Optional
from collections import defaultdict
import datetime
from ..models.incident import Incident, IncidentSeverity

class FSICalculator:
    """
    Forward-Seeding Index Calculator for institutional accountability tracking.
    
    The FSI represents the cumulative impact of incidents on an institution's
    accountability score. Higher FSI values indicate institutions requiring
    more attention and intervention.
    """
    
    def __init__(self):
        """Initialize FSI Calculator with base scoring parameters."""
        self.base_scores = {
            IncidentSeverity.GREEN: 1.0,
            IncidentSeverity.YELLOW: 5.0,
            IncidentSeverity.RED: 20.0
        }
        
        # Decay factor for older incidents (incidents lose impact over time)
        self.monthly_decay_factor = 0.95
        
        # Thresholds for risk categorization
        self.risk_thresholds = {
            "green": 10.0,   # Low risk institutions
            "yellow": 50.0,  # Medium risk institutions
            "red": 100.0     # High risk institutions (100+)
        }

    def calculate_institution_fsi(self, 
                                incidents: List[Incident], 
                                institution: str,
                                as_of_date: Optional[datetime.date] = None) -> Dict:
        """
        Calculate FSI for a specific institution based on its incidents.
        
        Args:
            incidents: List of all incidents
            institution: Name of institution to calculate FSI for
            as_of_date: Calculate FSI as of this date (defaults to today)
            
        Returns:
            dict: FSI calculation results and breakdown
        """
        if as_of_date is None:
            as_of_date = datetime.date.today()
            
        # Filter incidents for this institution
        institution_incidents = [
            incident for incident in incidents 
            if incident.institution.lower() == institution.lower() and 
            incident.approved and  # Only count approved incidents
            incident.date <= as_of_date
        ]
        
        if not institution_incidents:
            return {
                "institution": institution,
                "fsi_score": 0.0,
                "risk_level": "green",
                "incident_count": 0,
                "breakdown": {
                    "red_incidents": 0,
                    "yellow_incidents": 0,
                    "green_incidents": 0,
                    "total_base_score": 0.0,
                    "time_decay_factor": 1.0,
                    "final_score": 0.0
                }
            }
        
        # Calculate base scores by severity
        severity_counts = {
            IncidentSeverity.RED: 0,
            IncidentSeverity.YELLOW: 0,
            IncidentSeverity.GREEN: 0
        }
        
        total_base_score = 0.0
        oldest_incident_months = 0
        
        for incident in institution_incidents:
            severity_counts[incident.severity] += 1
            total_base_score += self.base_scores[incident.severity]
            
            # Calculate age of incident in months
            months_old = (as_of_date - incident.date).days / 30.44  # Average days per month
            oldest_incident_months = max(oldest_incident_months, months_old)
        
        # Apply time decay factor
        decay_factor = self.monthly_decay_factor ** oldest_incident_months
        final_score = total_base_score * max(decay_factor, 0.1)  # Minimum 10% of original score
        
        # Determine risk level
        risk_level = self._determine_risk_level(final_score)
        
        return {
            "institution": institution,
            "fsi_score": round(final_score, 2),
            "risk_level": risk_level,
            "incident_count": len(institution_incidents),
            "breakdown": {
                "red_incidents": severity_counts[IncidentSeverity.RED],
                "yellow_incidents": severity_counts[IncidentSeverity.YELLOW],
                "green_incidents": severity_counts[IncidentSeverity.GREEN],
                "total_base_score": round(total_base_score, 2),
                "time_decay_factor": round(decay_factor, 3),
                "final_score": round(final_score, 2),
                "oldest_incident_months": round(oldest_incident_months, 1)
            }
        }

    def calculate_all_institutions_fsi(self, 
                                     incidents: List[Incident],
                                     as_of_date: Optional[datetime.date] = None) -> Dict:
        """
        Calculate FSI for all institutions that have incidents.
        
        Args:
            incidents: List of all incidents
            as_of_date: Calculate FSI as of this date (defaults to today)
            
        Returns:
            dict: FSI results for all institutions
        """
        if as_of_date is None:
            as_of_date = datetime.date.today()
            
        # Get unique institutions
        institutions = set(
            incident.institution for incident in incidents 
            if incident.approved and incident.date <= as_of_date
        )
        
        results = {}
        for institution in institutions:
            results[institution] = self.calculate_institution_fsi(
                incidents, institution, as_of_date
            )
        
        # Sort by FSI score (highest first)
        sorted_results = dict(
            sorted(results.items(), 
                  key=lambda x: x[1]['fsi_score'], 
                  reverse=True)
        )
        
        return {
            "calculation_date": as_of_date.isoformat(),
            "total_institutions": len(sorted_results),
            "institutions": sorted_results,
            "summary": self._generate_summary(sorted_results)
        }

    def get_risk_categorization(self, incidents: List[Incident]) -> Dict:
        """
        Categorize all institutions by risk level.
        
        Args:
            incidents: List of all incidents
            
        Returns:
            dict: Institutions grouped by risk level
        """
        all_fsi = self.calculate_all_institutions_fsi(incidents)
        
        categorized = {
            "red": [],
            "yellow": [],
            "green": []
        }
        
        for institution, data in all_fsi["institutions"].items():
            risk_level = data["risk_level"]
            categorized[risk_level].append({
                "institution": institution,
                "fsi_score": data["fsi_score"],
                "incident_count": data["incident_count"]
            })
        
        return categorized

    def _determine_risk_level(self, fsi_score: float) -> str:
        """Determine risk level based on FSI score."""
        if fsi_score >= self.risk_thresholds["red"]:
            return "red"
        elif fsi_score >= self.risk_thresholds["yellow"]:
            return "yellow"
        else:
            return "green"

    def _generate_summary(self, results: Dict) -> Dict:
        """Generate summary statistics for FSI calculations."""
        if not results:
            return {
                "total_institutions": 0,
                "risk_distribution": {"red": 0, "yellow": 0, "green": 0},
                "average_fsi": 0.0,
                "highest_fsi": {"institution": None, "score": 0.0},
                "total_incidents": 0
            }
        
        risk_counts = {"red": 0, "yellow": 0, "green": 0}
        fsi_scores = []
        total_incidents = 0
        highest_fsi = {"institution": None, "score": 0.0}
        
        for institution, data in results.items():
            risk_level = data["risk_level"]
            risk_counts[risk_level] += 1
            
            fsi_score = data["fsi_score"]
            fsi_scores.append(fsi_score)
            total_incidents += data["incident_count"]
            
            if fsi_score > highest_fsi["score"]:
                highest_fsi = {"institution": institution, "score": fsi_score}
        
        return {
            "total_institutions": len(results),
            "risk_distribution": risk_counts,
            "average_fsi": round(sum(fsi_scores) / len(fsi_scores), 2) if fsi_scores else 0.0,
            "highest_fsi": highest_fsi,
            "total_incidents": total_incidents
        }

    def generate_trend_analysis(self, 
                              incidents: List[Incident], 
                              institution: str,
                              months_back: int = 12) -> Dict:
        """
        Generate trend analysis for an institution over time.
        
        Args:
            incidents: List of all incidents
            institution: Institution to analyze
            months_back: Number of months to analyze
            
        Returns:
            dict: Monthly FSI trends and analysis
        """
        today = datetime.date.today()
        monthly_data = []
        
        for month_offset in range(months_back, -1, -1):
            # Calculate date for this month
            analysis_date = today - datetime.timedelta(days=month_offset * 30)
            
            # Calculate FSI as of this date
            fsi_data = self.calculate_institution_fsi(
                incidents, institution, analysis_date
            )
            
            monthly_data.append({
                "month": analysis_date.strftime("%Y-%m"),
                "fsi_score": fsi_data["fsi_score"],
                "incident_count": fsi_data["incident_count"],
                "risk_level": fsi_data["risk_level"]
            })
        
        # Calculate trend direction
        if len(monthly_data) >= 2:
            recent_score = monthly_data[-1]["fsi_score"]
            previous_score = monthly_data[-2]["fsi_score"]
            
            if recent_score > previous_score * 1.1:
                trend = "increasing"
            elif recent_score < previous_score * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "institution": institution,
            "trend_direction": trend,
            "current_fsi": monthly_data[-1]["fsi_score"] if monthly_data else 0.0,
            "monthly_data": monthly_data,
            "analysis_period": f"{months_back} months"
        }