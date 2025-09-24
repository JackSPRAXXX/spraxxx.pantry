#!/usr/bin/env python3
"""
SPRAXXX Pantry - Main Entry Point

Initialize and demonstrate the SPRAXXX Pantry system for transforming
computational energy into charitable abundance.
"""

import logging
import time
from typing import Dict, Any

from greeter import Greeter, BotType
from kitchen import Kitchen
from yield_queue import YieldQueue, OutputType, Priority
from credit_ledger import CreditLedger, TransactionType, CreditType
from governance import GovernanceLayer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SPRAXXXPantry:
    """
    Main SPRAXXX Pantry System
    
    Orchestrates all modules to transform computational energy
    for charitable purposes.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize modules
        self.credit_ledger = CreditLedger()
        self.greeter = Greeter()
        self.kitchen = Kitchen()
        self.yield_queue = YieldQueue()
        self.governance = GovernanceLayer(self.credit_ledger)
        
        self.logger.info("SPRAXXX Pantry system initialized")
        
        # Record system initialization
        self.credit_ledger.record_transaction(
            TransactionType.GOVERNANCE_ACTION,
            "system",
            "SPRAXXX Pantry system initialized",
            {CreditType.TRANSPARENCY: 5.0},
            {'initialization_time': time.time()}
        )
    
    def welcome_bot(self, bot_id: str, bot_metadata: Dict[str, Any]) -> bool:
        """
        Welcome a new bot to the system
        
        Args:
            bot_id: Unique identifier for the bot
            bot_metadata: Metadata about the bot's purpose and capabilities
            
        Returns:
            True if bot was welcomed, False if rejected
        """
        # Check governance compliance
        if not self.governance.evaluate_action(bot_id, "bot_welcome", bot_metadata):
            self.logger.warning(f"Bot {bot_id} rejected by governance layer")
            return False
        
        # Welcome the bot
        classification = self.greeter.welcome_bot(bot_id, bot_metadata)
        
        if classification:
            # Record welcome in ledger
            credits = {CreditType.COMMUNITY: 2.0}
            if classification.trust_score > 0.8:
                credits[CreditType.CHARITABLE] = 1.0
            
            self.credit_ledger.record_transaction(
                TransactionType.BOT_WELCOME,
                bot_id,
                f"Bot welcomed: {classification.bot_type.value} (trust: {classification.trust_score:.2f})",
                credits,
                {
                    'bot_type': classification.bot_type.value,
                    'trust_score': classification.trust_score,
                    'capabilities': classification.capabilities
                }
            )
            
            self.logger.info(f"Bot {bot_id} successfully welcomed")
            return True
        
        return False
    
    def submit_charitable_task(self, bot_id: str, task_type: str, description: str,
                             input_data: Any, charitable_impact: str) -> str:
        """
        Submit a task for charitable computation
        
        Args:
            bot_id: ID of the bot submitting the task
            task_type: Type of computational task
            description: Description of the task
            input_data: Input data for processing
            charitable_impact: Description of charitable impact
            
        Returns:
            Task ID if successful, empty string if rejected
        """
        # Check if bot is welcomed
        welcomed_bots = self.greeter.get_welcomed_bots()
        if bot_id not in welcomed_bots:
            self.logger.warning(f"Unwelcomed bot {bot_id} attempted task submission")
            return ""
        
        # Check governance compliance
        task_data = {
            'description': description,
            'task_type': task_type,
            'charitable_impact': charitable_impact
        }
        
        if not self.governance.evaluate_action(bot_id, "task_submission", task_data):
            self.logger.warning(f"Task submission by {bot_id} rejected by governance")
            return ""
        
        # Submit task to kitchen
        try:
            task_id = self.kitchen.submit_task(bot_id, task_type, description, input_data, charitable_impact)
            
            # Record in ledger
            self.credit_ledger.record_transaction(
                TransactionType.TASK_SUBMISSION,
                bot_id,
                f"Task submitted: {description}",
                {CreditType.COMPUTATIONAL: 1.0},
                {
                    'task_id': task_id,
                    'task_type': task_type,
                    'charitable_impact': charitable_impact
                }
            )
            
            self.logger.info(f"Task {task_id} submitted by {bot_id}")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to submit task: {str(e)}")
            return ""
    
    def process_task(self, task_id: str) -> bool:
        """Process a submitted task"""
        success = self.kitchen.process_task(task_id)
        
        if success:
            # Get task details
            task = self.kitchen.get_task_status(task_id)
            if task and task.status.value == "completed":
                # Store output in yield queue
                output_type = self._map_task_to_output_type(task.task_type)
                priority = Priority.HIGH if task.charitable_impact else Priority.MEDIUM
                
                output_id = self.yield_queue.store_output(
                    task_id,
                    task.bot_id,
                    output_type,
                    task.output_data,
                    {
                        'task_description': task.description,
                        'processing_time': task.completed_at - task.started_at if task.started_at else 0,
                        'energy_used': task.energy_used
                    },
                    priority,
                    0.8,  # High charitable impact score
                    ['charitable', 'community']
                )
                
                # Record completion in ledger
                credits = {
                    CreditType.COMPUTATIONAL: 2.0,
                    CreditType.CHARITABLE: 3.0 if task.charitable_impact else 1.0,
                    CreditType.EFFICIENCY: min(2.0, 2.0 / max(0.1, task.energy_used))
                }
                
                self.credit_ledger.record_transaction(
                    TransactionType.TASK_COMPLETION,
                    task.bot_id,
                    f"Task completed: {task.description}",
                    credits,
                    {
                        'task_id': task_id,
                        'output_id': output_id,
                        'energy_used': task.energy_used,
                        'charitable_impact': task.charitable_impact
                    }
                )
                
                self.logger.info(f"Task {task_id} completed and output stored as {output_id}")
        
        return success
    
    def _map_task_to_output_type(self, task_type: str) -> OutputType:
        """Map task type to output type"""
        mapping = {
            'data_analysis': OutputType.DATA_ANALYSIS,
            'text_processing': OutputType.PROCESSED_TEXT,
            'calculation': OutputType.CALCULATION_RESULT,
            'research_task': OutputType.RESEARCH_FINDINGS,
            'community_service': OutputType.COMMUNITY_SERVICE
        }
        return mapping.get(task_type, OutputType.DATA_ANALYSIS)
    
    def register_charitable_consumer(self, consumer_id: str, name: str, mission: str) -> bool:
        """Register a charitable organization as a consumer"""
        success = self.yield_queue.register_consumer(consumer_id, name, mission)
        
        if success:
            # Record in ledger
            self.credit_ledger.record_transaction(
                TransactionType.GOVERNANCE_ACTION,
                consumer_id,
                f"Charitable consumer registered: {name}",
                {CreditType.COMMUNITY: 3.0, CreditType.TRANSPARENCY: 2.0},
                {
                    'consumer_name': name,
                    'mission': mission,
                    'registration_time': time.time()
                }
            )
        
        return success
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'greeted_bots': len(self.greeter.get_welcomed_bots()),
            'kitchen_metrics': self.kitchen.get_kitchen_metrics(),
            'yield_queue_summary': self.yield_queue.get_available_outputs_summary(),
            'distribution_metrics': self.yield_queue.get_distribution_metrics(),
            'governance_metrics': self.governance.governance_metrics,
            'ledger_stats': self.credit_ledger.get_ledger_statistics(),
            'system_uptime': time.time()
        }
    
    def generate_transparency_report(self) -> Dict[str, Any]:
        """Generate comprehensive transparency report"""
        return {
            'pantry_status': self.get_system_status(),
            'ledger_transparency': self.credit_ledger.generate_transparency_report(),
            'governance_compliance': self.governance.get_compliance_report(),
            'manifesto_compliance': {
                'shepherding_bot_energy': len(self.greeter.get_welcomed_bots()) > 0,
                'teaching_purpose': self.kitchen.get_kitchen_metrics()['completed_tasks'] > 0,
                'extracting_clarity': self.yield_queue.get_distribution_metrics()['total_outputs_consumed'] > 0,
                'growing_abundance': self.credit_ledger.get_ledger_statistics()['total_credits_awarded']
            }
        }

def demonstrate_pantry_system():
    """Demonstrate the SPRAXXX Pantry system with example usage"""
    print("=" * 60)
    print("SPRAXXX PANTRY - Computational Energy for Charitable Abundance")
    print("=" * 60)
    print()
    
    # Initialize the system
    pantry = SPRAXXXPantry()
    print("✓ System initialized")
    
    # Welcome some bots
    print("\n--- Welcoming Bots ---")
    
    bots = [
        {
            'id': 'bot_charitable_helper',
            'metadata': {
                'purpose': 'Help charitable organizations with data analysis',
                'description': 'A bot dedicated to supporting nonprofit missions',
                'capabilities': ['data_analysis', 'research', 'reporting']
            }
        },
        {
            'id': 'bot_education_assistant', 
            'metadata': {
                'purpose': 'Assist with educational content creation',
                'description': 'Educational support bot for community learning',
                'capabilities': ['text_processing', 'curriculum_development']
            }
        }
    ]
    
    for bot in bots:
        success = pantry.welcome_bot(bot['id'], bot['metadata'])
        print(f"{'✓' if success else '✗'} Bot {bot['id']}: {'Welcomed' if success else 'Rejected'}")
    
    # Submit some tasks
    print("\n--- Submitting Charitable Tasks ---")
    
    tasks = [
        {
            'bot_id': 'bot_charitable_helper',
            'task_type': 'data_analysis',
            'description': 'Analyze donation patterns for food bank optimization',
            'input_data': {'donations': [100, 150, 200, 180, 220], 'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May']},
            'charitable_impact': 'Help food banks distribute resources more efficiently'
        },
        {
            'bot_id': 'bot_education_assistant',
            'task_type': 'text_processing',
            'description': 'Create educational materials about environmental conservation',
            'input_data': 'Environmental conservation is crucial for sustainable development and community wellbeing.',
            'charitable_impact': 'Educate communities about environmental responsibility'
        }
    ]
    
    task_ids = []
    for task in tasks:
        task_id = pantry.submit_charitable_task(
            task['bot_id'],
            task['task_type'],
            task['description'],
            task['input_data'],
            task['charitable_impact']
        )
        if task_id:
            task_ids.append(task_id)
            print(f"✓ Task submitted: {task_id[:8]}... - {task['description']}")
        else:
            print(f"✗ Task rejected: {task['description']}")
    
    # Process tasks
    print("\n--- Processing Tasks ---")
    for task_id in task_ids:
        success = pantry.process_task(task_id)
        print(f"{'✓' if success else '✗'} Task {task_id[:8]}... {'processed' if success else 'failed'}")
    
    # Register charitable consumers
    print("\n--- Registering Charitable Consumers ---")
    
    consumers = [
        {
            'id': 'consumer_local_food_bank',
            'name': 'Local Community Food Bank',
            'mission': 'Provide food assistance to families in need in our community'
        },
        {
            'id': 'consumer_education_nonprofit',
            'name': 'Community Education Initiative',
            'mission': 'Provide free educational resources and programs to underserved communities'
        }
    ]
    
    for consumer in consumers:
        success = pantry.register_charitable_consumer(
            consumer['id'],
            consumer['name'],
            consumer['mission']
        )
        print(f"{'✓' if success else '✗'} Consumer registered: {consumer['name']}")
    
    # Generate reports
    print("\n--- System Status ---")
    status = pantry.get_system_status()
    print(f"Welcomed bots: {status['greeted_bots']}")
    print(f"Completed tasks: {status['kitchen_metrics']['completed_tasks']}")
    print(f"Available outputs: {status['yield_queue_summary']['total_available']}")
    print(f"Total ledger entries: {status['ledger_stats']['total_entries']}")
    
    print("\n--- Transparency Report ---")
    transparency = pantry.generate_transparency_report()
    manifesto_compliance = transparency['manifesto_compliance']
    
    print("Manifesto Compliance:")
    print(f"  ✓ Shepherding bot energy: {manifesto_compliance['shepherding_bot_energy']}")
    print(f"  ✓ Teaching purpose: {manifesto_compliance['teaching_purpose']}")
    print(f"  ✓ Extracting clarity: {manifesto_compliance['extracting_clarity']}")
    print(f"  ✓ Growing abundance: {manifesto_compliance['growing_abundance'] is not None}")
    
    print("\n" + "=" * 60)
    print("SPRAXXX Pantry demonstration completed successfully!")
    print("From chaos, we extract clarity. From waste, we grow abundance.")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_pantry_system()