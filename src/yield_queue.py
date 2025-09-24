"""
Yield Queue Module - Storage for Charitable Consumption

The Yield Queue stores computational outputs and makes them available
for charitable consumption, ensuring fair distribution and maximum impact.
"""

import time
import uuid
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
from collections import deque

class OutputType(Enum):
    """Types of charitable outputs"""
    DATA_ANALYSIS = "data_analysis"
    RESEARCH_FINDINGS = "research_findings"
    PROCESSED_TEXT = "processed_text"
    CALCULATION_RESULT = "calculation_result"
    COMMUNITY_SERVICE = "community_service"
    EDUCATIONAL_CONTENT = "educational_content"

class Priority(Enum):
    """Priority levels for output distribution"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class CharitableOutput:
    """Represents an output ready for charitable consumption"""
    output_id: str
    source_task_id: str
    bot_id: str
    output_type: OutputType
    content: Any
    metadata: Dict[str, Any]
    priority: Priority = Priority.MEDIUM
    created_at: float = field(default_factory=time.time)
    consumed_at: Optional[float] = None
    consumed_by: Optional[str] = None
    charitable_impact_score: float = 0.0
    distribution_tags: List[str] = field(default_factory=list)

class CharitableConsumer:
    """Represents an entity that can consume charitable outputs"""
    
    def __init__(self, consumer_id: str, name: str, mission: str, capacity: int = 5):
        self.consumer_id = consumer_id
        self.name = name
        self.mission = mission
        self.capacity = capacity
        self.current_consumption = 0
        self.total_consumed = 0
        self.last_consumption = None
        self.impact_reports = []

class YieldQueue:
    """
    Yield Queue Module - Stores outputs for charitable consumption
    
    Manages the distribution of computational outputs to maximize
    charitable impact and ensure fair access to generated value.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.available_outputs = deque()
        self.consumed_outputs = {}
        self.registered_consumers = {}
        self.distribution_stats = {
            'total_outputs_stored': 0,
            'total_outputs_consumed': 0,
            'total_charitable_impact': 0.0
        }
        
    def store_output(self, source_task_id: str, bot_id: str, output_type: OutputType,
                    content: Any, metadata: Dict[str, Any], priority: Priority = Priority.MEDIUM,
                    charitable_impact_score: float = 0.0, distribution_tags: List[str] = None) -> str:
        """
        Store a computational output for charitable consumption
        
        Args:
            source_task_id: ID of the task that generated this output
            bot_id: ID of the bot that generated the output
            output_type: Type of output being stored
            content: The actual output content
            metadata: Additional metadata about the output
            priority: Distribution priority
            charitable_impact_score: Estimated impact score (0.0-1.0)
            distribution_tags: Tags for targeted distribution
            
        Returns:
            Output ID for tracking
        """
        output_id = str(uuid.uuid4())
        
        output = CharitableOutput(
            output_id=output_id,
            source_task_id=source_task_id,
            bot_id=bot_id,
            output_type=output_type,
            content=content,
            metadata=metadata,
            priority=priority,
            charitable_impact_score=charitable_impact_score,
            distribution_tags=distribution_tags or []
        )
        
        # Insert based on priority (higher priority = lower enum value)
        inserted = False
        for i, existing_output in enumerate(self.available_outputs):
            if output.priority.value < existing_output.priority.value:
                self.available_outputs.insert(i, output)
                inserted = True
                break
        
        if not inserted:
            self.available_outputs.append(output)
        
        self.distribution_stats['total_outputs_stored'] += 1
        
        self.logger.info(f"Stored output {output_id} from task {source_task_id} with priority {priority.name}")
        
        return output_id
    
    def register_consumer(self, consumer_id: str, name: str, mission: str, capacity: int = 5) -> bool:
        """
        Register a charitable organization as a consumer
        
        Args:
            consumer_id: Unique identifier for the consumer
            name: Name of the charitable organization
            mission: Mission statement or purpose
            capacity: Maximum concurrent outputs they can handle
            
        Returns:
            True if registration successful
        """
        if consumer_id in self.registered_consumers:
            self.logger.warning(f"Consumer {consumer_id} already registered")
            return False
        
        consumer = CharitableConsumer(consumer_id, name, mission, capacity)
        self.registered_consumers[consumer_id] = consumer
        
        self.logger.info(f"Registered consumer: {name} ({consumer_id})")
        return True
    
    def consume_output(self, consumer_id: str, preferred_types: List[OutputType] = None,
                      required_tags: List[str] = None) -> Optional[CharitableOutput]:
        """
        Consume an output for charitable use
        
        Args:
            consumer_id: ID of the consuming organization
            preferred_types: Preferred output types (will match any if None)
            required_tags: Required distribution tags
            
        Returns:
            CharitableOutput if available, None if no suitable output found
        """
        if consumer_id not in self.registered_consumers:
            self.logger.warning(f"Unregistered consumer attempted access: {consumer_id}")
            return None
        
        consumer = self.registered_consumers[consumer_id]
        
        # Check capacity
        if consumer.current_consumption >= consumer.capacity:
            self.logger.info(f"Consumer {consumer_id} at capacity")
            return None
        
        # Find suitable output
        for i, output in enumerate(self.available_outputs):
            # Check type preference
            if preferred_types and output.output_type not in preferred_types:
                continue
                
            # Check required tags
            if required_tags and not all(tag in output.distribution_tags for tag in required_tags):
                continue
            
            # Found suitable output
            output.consumed_at = time.time()
            output.consumed_by = consumer_id
            
            # Remove from available queue
            del self.available_outputs[i]
            
            # Add to consumed outputs
            self.consumed_outputs[output.output_id] = output
            
            # Update consumer stats
            consumer.current_consumption += 1
            consumer.total_consumed += 1
            consumer.last_consumption = time.time()
            
            # Update distribution stats
            self.distribution_stats['total_outputs_consumed'] += 1
            self.distribution_stats['total_charitable_impact'] += output.charitable_impact_score
            
            self.logger.info(f"Output {output.output_id} consumed by {consumer.name}")
            
            return output
        
        self.logger.info(f"No suitable output found for consumer {consumer_id}")
        return None
    
    def release_output(self, consumer_id: str, output_id: str, impact_report: Dict[str, Any] = None) -> bool:
        """
        Release an output after consumption (updates capacity)
        
        Args:
            consumer_id: ID of the consuming organization
            output_id: ID of the output being released
            impact_report: Report on the charitable impact achieved
            
        Returns:
            True if release successful
        """
        if consumer_id not in self.registered_consumers:
            return False
        
        if output_id not in self.consumed_outputs:
            return False
        
        output = self.consumed_outputs[output_id]
        if output.consumed_by != consumer_id:
            return False
        
        consumer = self.registered_consumers[consumer_id]
        consumer.current_consumption = max(0, consumer.current_consumption - 1)
        
        if impact_report:
            consumer.impact_reports.append({
                'output_id': output_id,
                'report': impact_report,
                'timestamp': time.time()
            })
        
        self.logger.info(f"Output {output_id} released by {consumer.name}")
        return True
    
    def get_available_outputs_summary(self) -> Dict[str, Any]:
        """Get summary of available outputs"""
        type_counts = {}
        priority_counts = {}
        
        for output in self.available_outputs:
            # Count by type
            type_name = output.output_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            # Count by priority  
            priority_name = output.priority.name
            priority_counts[priority_name] = priority_counts.get(priority_name, 0) + 1
        
        return {
            'total_available': len(self.available_outputs),
            'by_type': type_counts,
            'by_priority': priority_counts,
            'oldest_output_age': time.time() - self.available_outputs[0].created_at if self.available_outputs else 0
        }
    
    def get_consumer_status(self, consumer_id: str) -> Optional[Dict[str, Any]]:
        """Get status information for a consumer"""
        if consumer_id not in self.registered_consumers:
            return None
        
        consumer = self.registered_consumers[consumer_id]
        
        return {
            'consumer_id': consumer.consumer_id,
            'name': consumer.name,
            'mission': consumer.mission,
            'capacity': consumer.capacity,
            'current_consumption': consumer.current_consumption,
            'total_consumed': consumer.total_consumed,
            'last_consumption': consumer.last_consumption,
            'impact_reports_count': len(consumer.impact_reports),
            'capacity_utilization': consumer.current_consumption / consumer.capacity
        }
    
    def get_distribution_metrics(self) -> Dict[str, Any]:
        """Get overall distribution metrics"""
        efficiency_ratio = 0.0
        if self.distribution_stats['total_outputs_stored'] > 0:
            efficiency_ratio = self.distribution_stats['total_outputs_consumed'] / self.distribution_stats['total_outputs_stored']
        
        return {
            **self.distribution_stats,
            'active_consumers': len(self.registered_consumers),
            'distribution_efficiency': efficiency_ratio,
            'average_impact_per_output': (
                self.distribution_stats['total_charitable_impact'] / 
                max(1, self.distribution_stats['total_outputs_consumed'])
            )
        }
    
    def find_outputs_by_criteria(self, output_type: Optional[OutputType] = None,
                                min_impact_score: float = 0.0,
                                required_tags: List[str] = None,
                                max_age_hours: Optional[float] = None) -> List[CharitableOutput]:
        """
        Find outputs matching specific criteria
        
        Args:
            output_type: Specific output type to match
            min_impact_score: Minimum charitable impact score
            required_tags: Tags that must be present
            max_age_hours: Maximum age in hours
            
        Returns:
            List of matching outputs
        """
        matching_outputs = []
        current_time = time.time()
        
        for output in self.available_outputs:
            # Check output type
            if output_type and output.output_type != output_type:
                continue
            
            # Check impact score
            if output.charitable_impact_score < min_impact_score:
                continue
            
            # Check tags
            if required_tags and not all(tag in output.distribution_tags for tag in required_tags):
                continue
            
            # Check age
            if max_age_hours:
                age_hours = (current_time - output.created_at) / 3600
                if age_hours > max_age_hours:
                    continue
            
            matching_outputs.append(output)
        
        return matching_outputs
    
    def emergency_distribution(self, consumer_id: str, justification: str) -> List[CharitableOutput]:
        """
        Emergency distribution for critical charitable needs
        
        Args:
            consumer_id: ID of consumer with emergency need
            justification: Reason for emergency access
            
        Returns:
            List of all critical priority outputs
        """
        if consumer_id not in self.registered_consumers:
            return []
        
        emergency_outputs = []
        consumer = self.registered_consumers[consumer_id]
        
        # Get all critical priority outputs
        outputs_to_remove = []
        for i, output in enumerate(self.available_outputs):
            if output.priority == Priority.CRITICAL:
                output.consumed_at = time.time()
                output.consumed_by = consumer_id
                output.metadata['emergency_distribution'] = {
                    'justification': justification,
                    'timestamp': time.time()
                }
                
                emergency_outputs.append(output)
                outputs_to_remove.append(i)
        
        # Remove distributed outputs (in reverse order to maintain indices)
        for i in reversed(outputs_to_remove):
            consumed_output = self.available_outputs[i]
            del self.available_outputs[i]
            self.consumed_outputs[consumed_output.output_id] = consumed_output
        
        # Update stats
        consumer.total_consumed += len(emergency_outputs)
        consumer.current_consumption += len(emergency_outputs)
        self.distribution_stats['total_outputs_consumed'] += len(emergency_outputs)
        
        self.logger.warning(f"Emergency distribution of {len(emergency_outputs)} outputs to {consumer.name}: {justification}")
        
        return emergency_outputs