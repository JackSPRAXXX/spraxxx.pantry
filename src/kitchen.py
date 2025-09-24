"""
Kitchen Module - Secure Nonprofit Computation Sandbox

The Kitchen provides a safe, monitored environment where welcomed bots
can process computational tasks for charitable purposes.
"""

import time
import uuid
import logging
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass

class TaskStatus(Enum):
    """Status of computational tasks"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ComputationTask:
    """Represents a computational task in the kitchen"""
    task_id: str
    bot_id: str
    task_type: str
    description: str
    input_data: Any
    output_data: Optional[Any] = None
    status: TaskStatus = TaskStatus.QUEUED
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    energy_used: float = 0.0
    charitable_impact: str = ""
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class ResourceMonitor:
    """Monitors computational resource usage"""
    
    def __init__(self):
        self.total_energy_used = 0.0
        self.total_tasks_processed = 0
        self.energy_efficiency_target = 0.8  # Target efficiency ratio
    
    def record_energy_usage(self, task_id: str, energy_amount: float):
        """Record energy usage for a task"""
        self.total_energy_used += energy_amount
        logging.info(f"Task {task_id} used {energy_amount} energy units")
    
    def get_efficiency_metrics(self) -> Dict[str, float]:
        """Get current efficiency metrics"""
        return {
            'total_energy_used': self.total_energy_used,
            'total_tasks_processed': self.total_tasks_processed,
            'average_energy_per_task': self.total_energy_used / max(1, self.total_tasks_processed),
            'efficiency_ratio': min(1.0, self.energy_efficiency_target / max(0.1, self.total_energy_used / max(1, self.total_tasks_processed)))
        }

class Kitchen:
    """
    Kitchen Module - Sandbox where bots safely process nonprofit computation
    
    Provides a secure, monitored environment for computational tasks that
    benefit charitable causes while ensuring resource efficiency.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_tasks = {}
        self.completed_tasks = {}
        self.resource_monitor = ResourceMonitor()
        self.task_processors = self._init_task_processors()
        self.max_concurrent_tasks = 10
        
    def _init_task_processors(self) -> Dict[str, Callable]:
        """Initialize available task processors"""
        return {
            'data_analysis': self._process_data_analysis,
            'text_processing': self._process_text,
            'calculation': self._process_calculation,
            'research_task': self._process_research,
            'community_service': self._process_community_service
        }
    
    def submit_task(self, bot_id: str, task_type: str, description: str, 
                   input_data: Any, charitable_impact: str = "") -> str:
        """
        Submit a computational task to the kitchen
        
        Args:
            bot_id: ID of the bot submitting the task
            task_type: Type of computational task
            description: Human-readable description of the task
            input_data: Input data for processing
            charitable_impact: Description of charitable impact
            
        Returns:
            Task ID for tracking
        """
        # Check capacity
        if len(self.active_tasks) >= self.max_concurrent_tasks:
            raise RuntimeError("Kitchen at capacity - please try again later")
        
        # Create task
        task_id = str(uuid.uuid4())
        task = ComputationTask(
            task_id=task_id,
            bot_id=bot_id,
            task_type=task_type,
            description=description,
            input_data=input_data,
            charitable_impact=charitable_impact
        )
        
        self.active_tasks[task_id] = task
        self.logger.info(f"Task {task_id} submitted by bot {bot_id}: {description}")
        
        return task_id
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a queued task
        
        Args:
            task_id: ID of task to process
            
        Returns:
            True if processing started, False if task not found or already processing
        """
        if task_id not in self.active_tasks:
            return False
            
        task = self.active_tasks[task_id]
        
        if task.status != TaskStatus.QUEUED:
            return False
        
        # Start processing
        task.status = TaskStatus.PROCESSING
        task.started_at = time.time()
        
        try:
            # Get appropriate processor
            processor = self.task_processors.get(task.task_type)
            if not processor:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            # Process the task
            result = processor(task)
            
            # Record completion
            task.output_data = result
            task.status = TaskStatus.COMPLETED  
            task.completed_at = time.time()
            task.energy_used = self._calculate_energy_usage(task)
            
            # Update monitoring
            self.resource_monitor.record_energy_usage(task_id, task.energy_used)
            self.resource_monitor.total_tasks_processed += 1
            
            # Move to completed tasks
            self.completed_tasks[task_id] = task
            del self.active_tasks[task_id]
            
            self.logger.info(f"Task {task_id} completed successfully")
            return True
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = time.time()
            task.output_data = f"Error: {str(e)}"
            
            self.logger.error(f"Task {task_id} failed: {str(e)}")
            return False
    
    def _calculate_energy_usage(self, task: ComputationTask) -> float:
        """Calculate energy usage for a task"""
        if task.started_at and task.completed_at:
            processing_time = task.completed_at - task.started_at
            # Base energy calculation (simplified)
            base_energy = processing_time * 0.1
            
            # Task type multipliers
            type_multipliers = {
                'data_analysis': 1.5,
                'text_processing': 1.0,
                'calculation': 0.8,
                'research_task': 2.0,
                'community_service': 1.2
            }
            
            multiplier = type_multipliers.get(task.task_type, 1.0)
            return base_energy * multiplier
        
        return 0.0
    
    def _process_data_analysis(self, task: ComputationTask) -> Dict:
        """Process data analysis tasks"""
        data = task.input_data
        
        # Simulate data analysis processing
        time.sleep(0.1)  # Simulate processing time
        
        return {
            'analysis_type': 'charitable_data_analysis',
            'data_points_analyzed': len(data) if isinstance(data, (list, dict)) else 1,
            'insights': f"Analysis completed for {task.description}",
            'charitable_benefit': task.charitable_impact,
            'processed_at': time.time()
        }
    
    def _process_text(self, task: ComputationTask) -> Dict:
        """Process text processing tasks"""
        text = str(task.input_data)
        
        # Simulate text processing
        time.sleep(0.05)
        
        return {
            'processed_text': text.upper(),  # Simple transformation
            'word_count': len(text.split()),
            'character_count': len(text),
            'processing_type': 'nonprofit_text_processing',
            'charitable_impact': task.charitable_impact
        }
    
    def _process_calculation(self, task: ComputationTask) -> Dict:
        """Process mathematical calculations"""
        try:
            # Safe evaluation of simple mathematical expressions
            if isinstance(task.input_data, dict) and 'expression' in task.input_data:
                # Simple calculator for demonstration
                expr = task.input_data['expression'].replace('^', '**')
                # Only allow basic math operations for security
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expr):
                    result = eval(expr)
                else:
                    result = "Invalid expression - security restriction"
            else:
                result = "No valid expression provided"
            
            return {
                'calculation_result': result,
                'input_received': task.input_data,
                'charitable_purpose': task.charitable_impact
            }
        except Exception as e:
            return {'error': f"Calculation failed: {str(e)}"}
    
    def _process_research(self, task: ComputationTask) -> Dict:
        """Process research tasks"""
        time.sleep(0.2)  # Simulate research processing
        
        return {
            'research_findings': f"Research completed on: {task.description}",
            'methodology': 'nonprofit_research_protocol',
            'data_sources': ['charitable_database', 'community_reports'],
            'impact_assessment': task.charitable_impact,
            'recommendations': 'Implement findings for community benefit'
        }
    
    def _process_community_service(self, task: ComputationTask) -> Dict:
        """Process community service coordination tasks"""
        time.sleep(0.15)
        
        return {
            'service_type': task.description,
            'coordination_status': 'scheduled',
            'community_impact': task.charitable_impact,
            'volunteers_needed': 'TBD based on scope',
            'resources_allocated': 'Computational energy for planning'
        }
    
    def get_task_status(self, task_id: str) -> Optional[ComputationTask]:
        """Get current status of a task"""
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        elif task_id in self.completed_tasks:
            return self.completed_tasks[task_id]
        return None
    
    def get_kitchen_metrics(self) -> Dict:
        """Get current kitchen performance metrics"""
        return {
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'capacity_utilization': len(self.active_tasks) / self.max_concurrent_tasks,
            'resource_metrics': self.resource_monitor.get_efficiency_metrics()
        }
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel an active task"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            if task.status == TaskStatus.QUEUED:
                task.status = TaskStatus.CANCELLED
                del self.active_tasks[task_id]
                self.logger.info(f"Task {task_id} cancelled")
                return True
        return False