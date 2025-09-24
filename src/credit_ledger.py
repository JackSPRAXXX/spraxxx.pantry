"""
SPRAXXX Pantry – Credit Ledger Module
Purpose: Log symbolic acknowledgments of contributions
Ethical: Nonprofit-only, no monetization
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from collections import defaultdict
from typing import Dict, List, Any
import time


class CreditLedger:
    def __init__(self):
        self.ledger = []
        self.bot_balances = defaultdict(int)  # Track credits per bot
        self.statistics = {
            "total_contributions": 0,
            "total_credits_issued": 0,
            "unique_contributors": set(),
            "by_bot_type": defaultdict(int),
            "contributions_over_time": []
        }

    def log_contribution(self, worker_id, contribution, credit_amount=None, metadata=None):
        """
        Log a symbolic credit for a worker with enhanced tracking.
        
        Args:
            worker_id: ID of the contributing worker/bot
            contribution: Description of the contribution
            credit_amount: Amount of credits to award (calculated if not provided)
            metadata: Additional information about the contribution
        """
        # Calculate credit amount based on contribution value if not provided
        if credit_amount is None:
            if isinstance(metadata, dict) and "yield_amount" in metadata:
                credit_amount = max(1, int(metadata["yield_amount"] * 0.1))  # 10% of yield as credits
            else:
                credit_amount = 1  # Default credit amount
        
        # Create ledger entry
        entry = {
            "worker": worker_id,
            "contribution": contribution,
            "credits": credit_amount,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        self.ledger.append(entry)
        self.bot_balances[worker_id] += credit_amount
        
        # Update statistics
        self._update_statistics(worker_id, credit_amount, metadata)
        
    def _update_statistics(self, worker_id, credit_amount, metadata):
        """Update internal statistics based on new contribution."""
        self.statistics["total_contributions"] += 1
        self.statistics["total_credits_issued"] += credit_amount
        self.statistics["unique_contributors"].add(worker_id)
        
        if metadata and isinstance(metadata, dict):
            if "bot_type" in metadata:
                self.statistics["by_bot_type"][metadata["bot_type"]] += credit_amount
        
        # Track contributions over time (for trend analysis)
        self.statistics["contributions_over_time"].append({
            "timestamp": time.time(),
            "worker": worker_id,
            "credits": credit_amount
        })

    def log_credit_spent(self, worker_id, amount_spent, purpose):
        """
        Log credits spent by a worker (for future resource allocation features).
        
        Args:
            worker_id: ID of the worker spending credits
            amount_spent: Amount of credits spent
            purpose: Purpose for spending credits
        """
        if self.bot_balances[worker_id] >= amount_spent:
            self.bot_balances[worker_id] -= amount_spent
            
            entry = {
                "worker": worker_id,
                "contribution": f"SPENT: {purpose}",
                "credits": -amount_spent,
                "timestamp": time.time(),
                "metadata": {"type": "expenditure", "purpose": purpose}
            }
            
            self.ledger.append(entry)
            return True
        return False

    def get_ledger(self):
        """Retrieve all logged contributions."""
        return self.ledger
    
    def get_bot_balance(self, worker_id) -> int:
        """Get current credit balance for a specific bot."""
        return self.bot_balances[worker_id]
    
    def get_all_balances(self) -> Dict[str, int]:
        """Get current credit balances for all bots."""
        return dict(self.bot_balances)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive ledger statistics."""
        stats = dict(self.statistics)
        stats["unique_contributors"] = len(self.statistics["unique_contributors"])
        stats["by_bot_type"] = dict(self.statistics["by_bot_type"])
        return stats
    
    def get_top_contributors(self, limit=10) -> List[Dict[str, Any]]:
        """Get top contributors by credit balance."""
        sorted_contributors = sorted(
            self.bot_balances.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [
            {"worker_id": worker_id, "credits": credits}
            for worker_id, credits in sorted_contributors[:limit]
        ]
    
    def generate_ledger_report(self) -> str:
        """Generate a formatted report of the credit ledger."""
        report = []
        report.append("=== SPRAXXX Pantry Credit Ledger Report ===")
        report.append(f"Total Contributions: {self.statistics['total_contributions']}")
        report.append(f"Total Credits Issued: {self.statistics['total_credits_issued']}")
        report.append(f"Unique Contributors: {len(self.statistics['unique_contributors'])}")
        
        if self.statistics["by_bot_type"]:
            report.append("\nCredits by Bot Type:")
            for bot_type, credits in self.statistics["by_bot_type"].items():
                report.append(f"  {bot_type}: {credits} credits")
        
        # Show top contributors
        top_contributors = self.get_top_contributors(5)
        if top_contributors:
            report.append("\nTop Contributors by Credits:")
            for contributor in top_contributors:
                report.append(f"  {contributor['worker_id']}: {contributor['credits']} credits")
        
        # Show recent activity
        recent_entries = self.ledger[-5:] if self.ledger else []
        if recent_entries:
            report.append("\nRecent Activity:")
            for entry in recent_entries:
                timestamp = time.strftime("%H:%M:%S", time.localtime(entry["timestamp"]))
                report.append(f"  {timestamp} - {entry['worker']}: {entry['contribution']} (+{entry['credits']} credits)")
        
        report.append("\n=== All credits are symbolic and nonprofit-only ===")
        return "\n".join(report)
