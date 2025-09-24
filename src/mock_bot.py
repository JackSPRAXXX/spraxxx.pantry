"""
SPRAXXX Pantry – Mock Bot Module
Purpose: Define configurable mock bots for batch simulation
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import random
from typing import Dict, Any


class MockBot:
    """
    Represents a configurable mock bot for SPRAXXX Pantry simulation.
    Each bot has adjustable parameters affecting its performance and resource usage.
    """
    
    def __init__(self, bot_id: str, efficiency: float = 1.0, 
                 resource_allocation: float = 1.0, bot_type: str = "worker"):
        """
        Initialize a mock bot with configurable parameters.
        
        Args:
            bot_id: Unique identifier for the bot
            efficiency: Bot's work efficiency (0.1 to 2.0, default 1.0)
            resource_allocation: Resource usage multiplier (0.5 to 3.0, default 1.0)
            bot_type: Type of bot ("worker", "indexer", "processor")
        """
        self.bot_id = bot_id
        self.efficiency = max(0.1, min(2.0, efficiency))  # Clamp between 0.1 and 2.0
        self.resource_allocation = max(0.5, min(3.0, resource_allocation))  # Clamp between 0.5 and 3.0
        self.bot_type = bot_type
        self.total_yield = 0
        self.total_credits = 0
        self.task_count = 0
        
    def generate_work_output(self) -> Dict[str, Any]:
        """
        Simulate bot work output based on its parameters.
        Higher efficiency produces better results, higher resource allocation uses more resources.
        
        Returns:
            Dictionary containing task information and results
        """
        # Base work types for different bot types
        work_types = {
            "worker": ["indexing", "cataloging", "organizing"],
            "indexer": ["metadata_extraction", "content_analysis", "classification"],
            "processor": ["data_processing", "computation", "analysis"]
        }
        
        available_tasks = work_types.get(self.bot_type, work_types["worker"])
        task_type = random.choice(available_tasks)
        
        # Calculate work quality based on efficiency
        base_quality = random.uniform(0.5, 1.0)
        adjusted_quality = min(1.0, base_quality * self.efficiency)
        
        # Calculate resource consumption
        base_resources = random.uniform(1.0, 5.0)
        actual_resources = base_resources * self.resource_allocation
        
        # Generate results based on quality
        if adjusted_quality > 0.8:
            result_quality = "high"
            yield_amount = random.randint(80, 120) * self.efficiency
        elif adjusted_quality > 0.5:
            result_quality = "medium"
            yield_amount = random.randint(50, 80) * self.efficiency
        else:
            result_quality = "basic"
            yield_amount = random.randint(20, 50) * self.efficiency
            
        output = {
            "bot_id": self.bot_id,
            "task": task_type,
            "result": f"{result_quality} {task_type} completed",
            "quality_score": adjusted_quality,
            "yield_amount": int(yield_amount),
            "resources_used": round(actual_resources, 2),
            "efficiency": self.efficiency,
            "bot_type": self.bot_type
        }
        
        self.task_count += 1
        self.total_yield += output["yield_amount"]
        
        return output
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics for this bot.
        
        Returns:
            Dictionary containing bot performance statistics
        """
        avg_yield = self.total_yield / max(1, self.task_count)
        
        return {
            "bot_id": self.bot_id,
            "bot_type": self.bot_type,
            "efficiency": self.efficiency,
            "resource_allocation": self.resource_allocation,
            "total_tasks": self.task_count,
            "total_yield": self.total_yield,
            "total_credits": self.total_credits,
            "average_yield_per_task": round(avg_yield, 2)
        }


def create_bot_fleet(num_bots: int) -> list[MockBot]:
    """
    Create a fleet of mock bots with varied parameters for simulation.
    
    Args:
        num_bots: Number of bots to create
        
    Returns:
        List of configured MockBot instances
    """
    bots = []
    bot_types = ["worker", "indexer", "processor"]
    
    for i in range(num_bots):
        bot_id = f"bot_{i+1:03d}"
        
        # Generate varied parameters for realistic simulation
        efficiency = random.uniform(0.6, 1.8)
        resource_allocation = random.uniform(0.7, 2.5)
        bot_type = random.choice(bot_types)
        
        bot = MockBot(bot_id, efficiency, resource_allocation, bot_type)
        bots.append(bot)
    
    return bots