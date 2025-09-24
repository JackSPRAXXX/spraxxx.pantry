"""
Governance Layer Module - Ethical Rule Enforcement

The Governance Layer enforces ethical guidelines and nonprofit-only rules
across all SPRAXXX Pantry operations, ensuring compliance with the manifesto.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from credit_ledger import CreditLedger, TransactionType, CreditType

class ViolationType(Enum):
    """Types of governance violations"""
    COMMERCIAL_USE = "commercial_use"
    ENERGY_WASTE = "energy_waste"
    UNETHICAL_CONTENT = "unethical_content"
    CAPACITY_ABUSE = "capacity_abuse"
    TRANSPARENCY_VIOLATION = "transparency_violation"
    MISSION_MISALIGNMENT = "mission_misalignment"

class ActionType(Enum):
    """Types of governance actions"""
    WARNING = "warning"
    RESTRICTION = "restriction"
    SUSPENSION = "suspension"
    TERMINATION = "termination"
    EDUCATION = "education"
    REHABILITATION = "rehabilitation"

@dataclass
class GovernanceRule:
    """Represents a governance rule"""
    rule_id: str
    name: str
    description: str
    violation_type: ViolationType
    severity: int  # 1-10, 10 being most severe
    enforcement_function: str  # Name of the enforcement function
    active: bool = True

@dataclass
class Violation:
    """Represents a governance violation"""
    violation_id: str
    actor_id: str
    rule_id: str
    violation_type: ViolationType
    description: str
    severity: int
    evidence: Dict[str, Any]
    timestamp: float
    resolved: bool = False
    resolution_action: Optional[ActionType] = None
    resolution_notes: Optional[str] = None

class GovernanceLayer:
    """
    Governance Layer Module - Enforces ethical, nonprofit-only rules
    
    Monitors all system activities and enforces compliance with the
    SPRAXXX Pantry manifesto and ethical obligations.
    """
    
    def __init__(self, credit_ledger: CreditLedger):
        self.logger = logging.getLogger(__name__)
        self.credit_ledger = credit_ledger
        self.rules = {}
        self.violations = {}
        self.actor_standings = {}  # Track standing/reputation of actors
        self.enforcement_callbacks = {}
        
        # Initialize core rules
        self._initialize_core_rules()
        
        # Performance metrics
        self.governance_metrics = {
            'total_violations_detected': 0,
            'total_violations_resolved': 0,
            'active_restrictions': 0,
            'rehabilitation_programs_active': 0
        }
    
    def _initialize_core_rules(self):
        """Initialize core governance rules"""
        core_rules = [
            GovernanceRule(
                "NONPROFIT_ONLY",
                "Nonprofit Purpose Only",
                "All activities must serve charitable, educational, or nonprofit purposes",
                ViolationType.COMMERCIAL_USE,
                10,  # Maximum severity
                "_enforce_nonprofit_only"
            ),
            GovernanceRule(
                "ENERGY_EFFICIENCY",
                "Energy Conservation",
                "Computational resources must be used efficiently without waste",
                ViolationType.ENERGY_WASTE,
                7,
                "_enforce_energy_efficiency"
            ),
            GovernanceRule(
                "TRANSPARENCY_REQUIRED",
                "Full Transparency",
                "All activities must be logged and available for community review",
                ViolationType.TRANSPARENCY_VIOLATION,
                8,
                "_enforce_transparency"
            ),
            GovernanceRule(
                "ETHICAL_CONTENT",
                "Ethical Content Standards",
                "All content and outputs must align with charitable values",
                ViolationType.UNETHICAL_CONTENT,
                9,
                "_enforce_ethical_content"
            ),
            GovernanceRule(
                "FAIR_CAPACITY_USE",
                "Fair Resource Usage",
                "Resources must be shared fairly and not monopolized",
                ViolationType.CAPACITY_ABUSE,
                6,
                "_enforce_fair_capacity"
            ),
            GovernanceRule(
                "MISSION_ALIGNMENT",
                "Mission Alignment",
                "All activities must align with the SPRAXXX Pantry mission",
                ViolationType.MISSION_MISALIGNMENT,
                8,
                "_enforce_mission_alignment"
            )
        ]
        
        for rule in core_rules:
            self.rules[rule.rule_id] = rule
    
    def register_enforcement_callback(self, rule_id: str, callback: Callable):
        """Register a callback function for rule enforcement"""
        self.enforcement_callbacks[rule_id] = callback
    
    def evaluate_action(self, actor_id: str, action_type: str, action_data: Dict[str, Any]) -> bool:
        """
        Evaluate an action against all governance rules
        
        Args:
            actor_id: ID of the actor performing the action
            action_type: Type of action being performed
            action_data: Data about the action
            
        Returns:
            True if action is allowed, False if blocked
        """
        violations_detected = []
        
        # Check each active rule
        for rule_id, rule in self.rules.items():
            if not rule.active:
                continue
            
            # Get enforcement function
            enforcement_func = getattr(self, rule.enforcement_function, None)
            if not enforcement_func:
                self.logger.error(f"Enforcement function {rule.enforcement_function} not found")
                continue
            
            # Evaluate rule
            violation = enforcement_func(actor_id, action_type, action_data, rule)
            if violation:
                violations_detected.append(violation)
        
        # Process violations
        if violations_detected:
            for violation in violations_detected:
                self._record_violation(violation)
            
            # Determine if action should be blocked
            max_severity = max(v.severity for v in violations_detected)
            if max_severity >= 8:  # High severity violations block action
                return False
        
        return True
    
    def _enforce_nonprofit_only(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce nonprofit-only rule"""
        # Check for commercial indicators
        commercial_keywords = [
            'profit', 'revenue', 'monetize', 'commercial', 'advertising',
            'marketing', 'sales', 'business', 'enterprise', 'corporate'
        ]
        
        # Analyze action data for commercial indicators
        text_to_check = []
        if 'description' in action_data:
            text_to_check.append(action_data['description'].lower())
        if 'purpose' in action_data:
            text_to_check.append(action_data['purpose'].lower())
        if 'content' in action_data and isinstance(action_data['content'], str):
            text_to_check.append(action_data['content'].lower())
        
        full_text = ' '.join(text_to_check)
        
        commercial_matches = [keyword for keyword in commercial_keywords if keyword in full_text]
        
        if commercial_matches:
            return Violation(
                violation_id=f"violation_{int(time.time())}_{actor_id}",
                actor_id=actor_id,
                rule_id=rule.rule_id,
                violation_type=rule.violation_type,
                description=f"Commercial indicators detected: {', '.join(commercial_matches)}",
                severity=rule.severity,
                evidence={
                    'commercial_keywords_found': commercial_matches,
                    'action_type': action_type,
                    'text_analyzed': full_text[:500]  # First 500 chars
                },
                timestamp=time.time()
            )
        
        return None
    
    def _enforce_energy_efficiency(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce energy efficiency rule"""
        if action_type == 'task_submission':
            # Check for energy waste indicators
            task_description = action_data.get('description', '').lower()
            
            # Red flags for energy waste
            waste_indicators = [
                'infinite loop', 'endless', 'perpetual', 'waste',
                'pointless', 'meaningless', 'spam', 'flood'
            ]
            
            waste_matches = [indicator for indicator in waste_indicators if indicator in task_description]
            
            if waste_matches:
                return Violation(
                    violation_id=f"violation_{int(time.time())}_{actor_id}",
                    actor_id=actor_id,
                    rule_id=rule.rule_id,
                    violation_type=rule.violation_type,
                    description=f"Potential energy waste detected: {', '.join(waste_matches)}",
                    severity=rule.severity,
                    evidence={
                        'waste_indicators': waste_matches,
                        'task_description': task_description
                    },
                    timestamp=time.time()
                )
        
        return None
    
    def _enforce_transparency(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce transparency rule"""
        # Check if required metadata is missing
        required_fields = ['description']
        if action_type == 'task_submission':
            required_fields.extend(['charitable_impact'])
        
        missing_fields = [field for field in required_fields if not action_data.get(field)]
        
        if missing_fields:
            return Violation(
                violation_id=f"violation_{int(time.time())}_{actor_id}",
                actor_id=actor_id,
                rule_id=rule.rule_id,
                violation_type=rule.violation_type,
                description=f"Missing required transparency fields: {', '.join(missing_fields)}",
                severity=max(3, rule.severity - 3),  # Lower severity for transparency issues
                evidence={
                    'missing_fields': missing_fields,
                    'action_type': action_type
                },
                timestamp=time.time()
            )
        
        return None
    
    def _enforce_ethical_content(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce ethical content standards"""
        unethical_keywords = [
            'harm', 'exploit', 'discriminat', 'hate', 'violence',
            'illegal', 'fraud', 'scam', 'malicious', 'destructive'
        ]
        
        # Check content for unethical indicators
        content_to_check = []
        for field in ['description', 'content', 'purpose']:
            if field in action_data and isinstance(action_data[field], str):
                content_to_check.append(action_data[field].lower())
        
        full_content = ' '.join(content_to_check)
        
        unethical_matches = [keyword for keyword in unethical_keywords if keyword in full_content]
        
        if unethical_matches:
            return Violation(
                violation_id=f"violation_{int(time.time())}_{actor_id}",
                actor_id=actor_id,
                rule_id=rule.rule_id,
                violation_type=rule.violation_type,
                description=f"Potentially unethical content detected: {', '.join(unethical_matches)}",
                severity=rule.severity,
                evidence={
                    'unethical_keywords': unethical_matches,
                    'content_sample': full_content[:200]
                },
                timestamp=time.time()
            )
        
        return None
    
    def _enforce_fair_capacity(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce fair capacity usage"""
        # This would integrate with other modules to check resource usage
        # For now, implement basic checks
        
        if action_type == 'task_submission':
            # Check if actor is submitting too many tasks
            actor_standing = self.actor_standings.get(actor_id, {'recent_tasks': 0, 'last_reset': time.time()})
            
            # Reset counter every hour
            if time.time() - actor_standing['last_reset'] > 3600:
                actor_standing['recent_tasks'] = 0
                actor_standing['last_reset'] = time.time()
            
            actor_standing['recent_tasks'] += 1
            self.actor_standings[actor_id] = actor_standing
            
            # Check if exceeding fair usage
            if actor_standing['recent_tasks'] > 20:  # Max 20 tasks per hour
                return Violation(
                    violation_id=f"violation_{int(time.time())}_{actor_id}",
                    actor_id=actor_id,
                    rule_id=rule.rule_id,
                    violation_type=rule.violation_type,
                    description=f"Excessive task submission: {actor_standing['recent_tasks']} tasks in last hour",
                    severity=rule.severity,
                    evidence={
                        'tasks_per_hour': actor_standing['recent_tasks'],
                        'threshold_exceeded': True
                    },
                    timestamp=time.time()
                )
        
        return None
    
    def _enforce_mission_alignment(self, actor_id: str, action_type: str, action_data: Dict[str, Any], rule: GovernanceRule) -> Optional[Violation]:
        """Enforce mission alignment"""
        # Check for alignment with SPRAXXX Pantry mission
        mission_keywords = [
            'charitable', 'community', 'help', 'benefit', 'support',
            'education', 'research', 'nonprofit', 'humanitarian', 'social good'
        ]
        
        # Analyze action for mission alignment
        text_to_check = []
        for field in ['description', 'purpose', 'charitable_impact']:
            if field in action_data and isinstance(action_data[field], str):
                text_to_check.append(action_data[field].lower())
        
        full_text = ' '.join(text_to_check)
        
        mission_matches = [keyword for keyword in mission_keywords if keyword in full_text]
        
        # If no mission alignment indicators found, flag as potential violation
        if not mission_matches and len(full_text) > 50:  # Only for substantial content
            return Violation(
                violation_id=f"violation_{int(time.time())}_{actor_id}",
                actor_id=actor_id,
                rule_id=rule.rule_id,
                violation_type=rule.violation_type,
                description="No clear mission alignment indicators found",
                severity=max(3, rule.severity - 4),  # Lower severity for alignment issues
                evidence={
                    'text_analyzed': full_text[:300],
                    'mission_keywords_found': mission_matches
                },
                timestamp=time.time()
            )
        
        return None
    
    def _record_violation(self, violation: Violation):
        """Record a governance violation"""
        self.violations[violation.violation_id] = violation
        self.governance_metrics['total_violations_detected'] += 1
        
        # Log to credit ledger
        self.credit_ledger.record_transaction(
            TransactionType.GOVERNANCE_ACTION,
            violation.actor_id,
            f"Violation detected: {violation.description}",
            {},  # No credits for violations
            {
                'violation_id': violation.violation_id,
                'violation_type': violation.violation_type.value,
                'severity': violation.severity,
                'rule_id': violation.rule_id
            }
        )
        
        self.logger.warning(f"Governance violation recorded: {violation.violation_id} - {violation.description}")
    
    def resolve_violation(self, violation_id: str, action: ActionType, notes: str = "") -> bool:
        """
        Resolve a governance violation
        
        Args:
            violation_id: ID of the violation to resolve
            action: Action taken to resolve the violation
            notes: Additional notes about the resolution
            
        Returns:
            True if resolution successful
        """
        if violation_id not in self.violations:
            return False
        
        violation = self.violations[violation_id]
        violation.resolved = True
        violation.resolution_action = action
        violation.resolution_notes = notes
        
        # Record resolution in ledger
        self.credit_ledger.record_transaction(
            TransactionType.GOVERNANCE_ACTION,
            violation.actor_id,
            f"Violation resolved: {action.value} - {notes}",
            self._get_resolution_credits(action),
            {
                'violation_id': violation_id,
                'resolution_action': action.value,
                'original_severity': violation.severity
            }
        )
        
        self.governance_metrics['total_violations_resolved'] += 1
        
        self.logger.info(f"Violation {violation_id} resolved with action: {action.value}")
        return True
    
    def _get_resolution_credits(self, action: ActionType) -> Dict[CreditType, float]:
        """Get credits awarded for violation resolution"""
        credit_awards = {
            ActionType.EDUCATION: {CreditType.TRANSPARENCY: 1.0},
            ActionType.REHABILITATION: {CreditType.COMMUNITY: 2.0},
            ActionType.WARNING: {CreditType.TRANSPARENCY: 0.5},
        }
        
        return credit_awards.get(action, {})
    
    def get_actor_standing(self, actor_id: str) -> Dict[str, Any]:
        """Get governance standing for an actor"""
        actor_violations = [v for v in self.violations.values() if v.actor_id == actor_id]
        
        total_violations = len(actor_violations)
        resolved_violations = len([v for v in actor_violations if v.resolved])
        unresolved_violations = total_violations - resolved_violations
        
        # Calculate reputation score (0-100)
        base_score = 100
        severity_penalty = sum(v.severity for v in actor_violations if not v.resolved) * 2
        reputation_score = max(0, base_score - severity_penalty)
        
        return {
            'actor_id': actor_id,
            'reputation_score': reputation_score,
            'total_violations': total_violations,
            'resolved_violations': resolved_violations,
            'unresolved_violations': unresolved_violations,
            'recent_violations': len([
                v for v in actor_violations 
                if time.time() - v.timestamp < 86400  # Last 24 hours
            ]),
            'standing': self._calculate_standing_level(reputation_score)
        }
    
    def _calculate_standing_level(self, reputation_score: float) -> str:
        """Calculate standing level based on reputation score"""
        if reputation_score >= 95:
            return "Exemplary"
        elif reputation_score >= 85:
            return "Good"
        elif reputation_score >= 70:
            return "Fair"
        elif reputation_score >= 50:
            return "Poor"
        else:
            return "Restricted"
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        rule_violations = {}
        for rule_id in self.rules:
            rule_violations[rule_id] = len([
                v for v in self.violations.values() 
                if v.rule_id == rule_id
            ])
        
        return {
            'report_generated_at': time.time(),
            'governance_metrics': self.governance_metrics,
            'rule_violations_by_type': rule_violations,
            'active_rules': len([r for r in self.rules.values() if r.active]),
            'resolution_rate': (
                self.governance_metrics['total_violations_resolved'] / 
                max(1, self.governance_metrics['total_violations_detected'])
            ),
            'top_violation_types': self._get_top_violation_types(),
            'system_compliance_score': self._calculate_system_compliance_score()
        }
    
    def _get_top_violation_types(self) -> List[Dict[str, Any]]:
        """Get top violation types by frequency"""
        violation_counts = {}
        for violation in self.violations.values():
            vtype = violation.violation_type.value
            violation_counts[vtype] = violation_counts.get(vtype, 0) + 1
        
        return sorted([
            {'violation_type': vtype, 'count': count}
            for vtype, count in violation_counts.items()
        ], key=lambda x: x['count'], reverse=True)
    
    def _calculate_system_compliance_score(self) -> float:
        """Calculate overall system compliance score"""
        if self.governance_metrics['total_violations_detected'] == 0:
            return 100.0
        
        resolution_rate = (
            self.governance_metrics['total_violations_resolved'] / 
            self.governance_metrics['total_violations_detected']
        )
        
        # Base score affected by resolution rate and violation frequency
        base_score = 100.0
        violation_penalty = min(30.0, self.governance_metrics['total_violations_detected'] * 0.5)
        resolution_bonus = resolution_rate * 20.0
        
        return max(0.0, base_score - violation_penalty + resolution_bonus)