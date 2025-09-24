"""
SPRAXXX Pantry – Batch Simulation Module
Purpose: Run configurable batch simulations with mock bots
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import random
import time
from typing import Dict, List, Any, Optional

from greeter import Greeter
from kitchen import Kitchen
from yield_queue import YieldQueue
from credit_ledger import CreditLedger
from governance import Governance
from mock_bot import MockBot, create_bot_fleet
from simulation_logger import SimulationLogger


class BatchSimulation:
    """
    Orchestrates batch simulations of the SPRAXXX Pantry system.
    Emphasizes stewardship and cosmic community through ethical bot processing.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the batch simulation system.
        
        Args:
            verbose: Whether to display real-time progress
        """
        # Initialize core SPRAXXX Pantry modules
        self.greeter = Greeter()
        self.kitchen = Kitchen()
        self.yield_queue = YieldQueue()
        self.ledger = CreditLedger()
        self.governance = Governance()
        
        # Initialize simulation-specific components
        self.logger = SimulationLogger(verbose=verbose)
        self.bots = []
        self.simulation_config = {}
        
    def configure_simulation(self, 
                           num_bots: int = 50,
                           simulation_name: str = "SPRAXXX Ethical Bot Harvest",
                           custom_bot_configs: Optional[List[Dict[str, Any]]] = None,
                           processing_delay: float = 0.0) -> Dict[str, Any]:
        """
        Configure the batch simulation parameters.
        
        Args:
            num_bots: Number of bots to simulate
            simulation_name: Name for this simulation run
            custom_bot_configs: Custom configurations for specific bots
            processing_delay: Delay between bot processing (for demonstration)
            
        Returns:
            Configuration dictionary
        """
        self.simulation_config = {
            "num_bots": num_bots,
            "simulation_name": simulation_name,
            "processing_delay": processing_delay,
            "custom_configs": custom_bot_configs or []
        }
        
        # Create the bot fleet
        if custom_bot_configs:
            self.bots = self._create_custom_bot_fleet(custom_bot_configs)
        else:
            self.bots = create_bot_fleet(num_bots)
            
        return self.simulation_config
    
    def _create_custom_bot_fleet(self, configs: List[Dict[str, Any]]) -> List[MockBot]:
        """Create bots with custom configurations."""
        bots = []
        for i, config in enumerate(configs):
            bot_id = config.get("bot_id", f"custom_bot_{i+1:03d}")
            efficiency = config.get("efficiency", 1.0)
            resource_allocation = config.get("resource_allocation", 1.0)
            bot_type = config.get("bot_type", "worker")
            
            bot = MockBot(bot_id, efficiency, resource_allocation, bot_type)
            bots.append(bot)
            
        return bots
    
    def run_simulation(self) -> Dict[str, Any]:
        """
        Execute the complete batch simulation.
        
        Returns:
            Comprehensive simulation results
        """
        if not self.bots:
            raise ValueError("No bots configured. Call configure_simulation() first.")
        
        # Start logging
        self.logger.start_simulation(
            len(self.bots), 
            self.simulation_config["simulation_name"]
        )
        
        # Process each bot through the SPRAXXX Pantry system
        for bot in self.bots:
            try:
                self._process_single_bot(bot)
                
                # Optional delay for demonstration purposes
                if self.simulation_config["processing_delay"] > 0:
                    time.sleep(self.simulation_config["processing_delay"])
                    
            except Exception as e:
                self.logger.log_error("bot_processing_error", {
                    "bot_id": bot.bot_id,
                    "error": str(e)
                })
        
        # End logging and compile results
        self.logger.end_simulation()
        
        return self._compile_results()
    
    def _process_single_bot(self, bot: MockBot):
        """
        Process a single bot through the complete SPRAXXX Pantry pipeline.
        
        Args:
            bot: MockBot instance to process
        """
        # Step 1: Greeter detects and classifies the bot
        classification = self.greeter.detect_incoming(bot.bot_id)
        
        if classification == "worker":
            # Step 2: Generate work output from the bot
            bot_output = bot.generate_work_output()
            
            # Step 3: Kitchen processes the bot activity safely
            kitchen_output = self.kitchen.process_worker(bot.bot_id)
            
            # Merge bot output with kitchen processing
            combined_output = {**kitchen_output, **bot_output}
            
            # Step 4: Governance validates the output
            if self.governance.validate_output(combined_output):
                # Step 5: Store in Yield Queue
                self.yield_queue.add_yield(combined_output)
                
                # Step 6: Calculate and log credits in Credit Ledger
                credit_amount = self._calculate_credits(combined_output)
                self.ledger.log_contribution(
                    bot.bot_id, 
                    combined_output["result"], 
                    credit_amount,
                    combined_output
                )
                
                # Update bot's credit total
                bot.total_credits += credit_amount
                
                # Log the processing
                self.logger.log_bot_processed(bot.bot_id, combined_output, credit_amount)
            else:
                self.logger.log_error("governance_validation_failed", {
                    "bot_id": bot.bot_id,
                    "output": combined_output
                })
        else:
            self.logger.log_error("bot_classification_failed", {
                "bot_id": bot.bot_id,
                "classification": classification
            })
    
    def _calculate_credits(self, output: Dict[str, Any]) -> int:
        """
        Calculate credit amount based on output quality and yield.
        Emphasizes fair acknowledgment of contributions.
        """
        base_credits = 1
        
        # Bonus for high quality work
        if output.get("quality_score", 0) > 0.8:
            base_credits += 2
        elif output.get("quality_score", 0) > 0.5:
            base_credits += 1
            
        # Bonus based on yield amount
        yield_bonus = max(0, int(output.get("yield_amount", 0) * 0.05))
        
        return base_credits + yield_bonus
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile comprehensive simulation results."""
        # Get statistics from all modules
        yield_stats = self.yield_queue.get_statistics()
        ledger_stats = self.ledger.get_statistics()
        logger_stats = self.logger.get_statistics()
        
        # Compile bot statistics
        bot_stats = [bot.get_statistics() for bot in self.bots]
        
        # Calculate aggregate metrics
        total_efficiency = sum(bot.efficiency for bot in self.bots) / len(self.bots)
        total_resource_allocation = sum(bot.resource_allocation for bot in self.bots) / len(self.bots)
        
        results = {
            "simulation_config": self.simulation_config,
            "summary": {
                "total_bots": len(self.bots),
                "average_efficiency": round(total_efficiency, 3),
                "average_resource_allocation": round(total_resource_allocation, 3),
                "simulation_duration": logger_stats.get("end_time", 0) - logger_stats.get("start_time", 0)
            },
            "yield_queue": {
                "statistics": yield_stats,
                "report": self.yield_queue.generate_yield_report()
            },
            "credit_ledger": {
                "statistics": ledger_stats,
                "balances": self.ledger.get_all_balances(),
                "top_contributors": self.ledger.get_top_contributors(),
                "report": self.ledger.generate_ledger_report()
            },
            "bot_statistics": bot_stats,
            "simulation_log": {
                "statistics": logger_stats,
                "detailed_report": self.logger.generate_detailed_report()
            }
        }
        
        return results
    
    def generate_simulation_summary(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of simulation results.
        
        Args:
            results: Results from run_simulation()
            
        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("🌟 SPRAXXX Pantry Batch Simulation Summary 🌟")
        lines.append("=" * 60)
        
        summary = results["summary"]
        lines.append(f"🤖 Total Bots: {summary['total_bots']}")
        lines.append(f"⚡ Average Efficiency: {summary['average_efficiency']}")
        lines.append(f"📊 Average Resource Allocation: {summary['average_resource_allocation']}")
        lines.append(f"⏱️  Duration: {summary['simulation_duration']:.2f} seconds")
        
        lines.append("\n📈 Yield Queue Results:")
        yield_stats = results["yield_queue"]["statistics"]
        lines.append(f"  • Total Items: {yield_stats['total_items']}")
        lines.append(f"  • Total Yield: {yield_stats['total_yield']}")
        lines.append(f"  • Resources Used: {yield_stats['total_resources_used']:.2f}")
        
        lines.append("\n💰 Credit Ledger Results:")
        ledger_stats = results["credit_ledger"]["statistics"]
        lines.append(f"  • Total Contributions: {ledger_stats['total_contributions']}")
        lines.append(f"  • Total Credits Issued: {ledger_stats['total_credits_issued']}")
        lines.append(f"  • Unique Contributors: {ledger_stats['unique_contributors']}")
        
        lines.append("\n🏆 Top Performers:")
        for contributor in results["credit_ledger"]["top_contributors"][:3]:
            lines.append(f"  • {contributor['worker_id']}: {contributor['credits']} credits")
        
        lines.append("\n🌍 Ethical Impact:")
        lines.append("  • All outputs dedicated to nonprofit purposes")
        lines.append("  • Transparent and auditable contribution tracking")
        lines.append("  • Serving the cosmic community through stewardship")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)