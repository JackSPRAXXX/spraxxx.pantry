"""
SPRAXXX Pantry – Yield Queue Module
Purpose: Store outputs from Kitchen for nonprofit consumption
Ethical: Nonprofit-only
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from collections import defaultdict
from typing import Dict, List, Any


class YieldQueue:
    def __init__(self):
        self.queue = []
        self.statistics = {
            "total_items": 0,
            "total_yield": 0,
            "by_bot_type": defaultdict(int),
            "by_quality": defaultdict(int),
            "total_resources_used": 0.0
        }

    def add_yield(self, yield_output):
        """Add a Kitchen output to the queue and update statistics."""
        self.queue.append(yield_output)
        self._update_statistics(yield_output)

    def _update_statistics(self, yield_output):
        """Update internal statistics based on new yield output."""
        self.statistics["total_items"] += 1
        
        # Handle both old format (simple) and new format (detailed)
        if isinstance(yield_output, dict):
            # New detailed format from mock bots
            if "yield_amount" in yield_output:
                self.statistics["total_yield"] += yield_output["yield_amount"]
            if "bot_type" in yield_output:
                self.statistics["by_bot_type"][yield_output["bot_type"]] += 1
            if "quality_score" in yield_output:
                quality_level = "high" if yield_output["quality_score"] > 0.8 else \
                               "medium" if yield_output["quality_score"] > 0.5 else "basic"
                self.statistics["by_quality"][quality_level] += 1
            if "resources_used" in yield_output:
                self.statistics["total_resources_used"] += yield_output["resources_used"]
        else:
            # Legacy format - assign default values
            self.statistics["total_yield"] += 10  # Default yield amount
            self.statistics["by_bot_type"]["legacy"] += 1
            self.statistics["by_quality"]["basic"] += 1

    def get_yield(self):
        """Retrieve all queued outputs for nonprofit consumption."""
        return self.queue
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive yield statistics."""
        return dict(self.statistics)
    
    def get_yield_by_bot(self) -> Dict[str, List[Any]]:
        """Get yields organized by bot ID."""
        by_bot = defaultdict(list)
        for item in self.queue:
            if isinstance(item, dict) and "bot_id" in item:
                by_bot[item["bot_id"]].append(item)
            else:
                by_bot["unknown"].append(item)
        return dict(by_bot)
    
    def generate_yield_report(self) -> str:
        """Generate a formatted report of yield queue contents and statistics."""
        report = []
        report.append("=== SPRAXXX Pantry Yield Queue Report ===")
        report.append(f"Total Items: {self.statistics['total_items']}")
        report.append(f"Total Yield Generated: {self.statistics['total_yield']}")
        report.append(f"Total Resources Used: {self.statistics['total_resources_used']:.2f}")
        
        if self.statistics["by_bot_type"]:
            report.append("\nYield by Bot Type:")
            for bot_type, count in self.statistics["by_bot_type"].items():
                report.append(f"  {bot_type}: {count} items")
        
        if self.statistics["by_quality"]:
            report.append("\nYield by Quality:")
            for quality, count in self.statistics["by_quality"].items():
                report.append(f"  {quality}: {count} items")
        
        # Show top contributors
        by_bot = self.get_yield_by_bot()
        if by_bot:
            report.append("\nTop Contributors:")
            sorted_bots = sorted(by_bot.items(), key=lambda x: len(x[1]), reverse=True)
            for bot_id, items in sorted_bots[:5]:  # Top 5
                total_yield = sum(item.get("yield_amount", 0) for item in items if isinstance(item, dict))
                report.append(f"  {bot_id}: {len(items)} tasks, {total_yield} total yield")
        
        report.append("\n=== All outputs are nonprofit-only and ethically processed ===")
        return "\n".join(report)
