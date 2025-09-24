"""
Greeter Module - Bot Detection and Classification

The Greeter module is the first point of contact for incoming computational entities.
It detects bots, classifies their purpose, and ensures they align with our nonprofit mission.
"""

import time
import logging
from typing import Dict, List, Optional
from enum import Enum

class BotType(Enum):
    """Classification types for incoming bots"""
    CHARITABLE = "charitable"
    EDUCATIONAL = "educational"
    RESEARCH = "research"
    UNKNOWN = "unknown"
    SUSPICIOUS = "suspicious"

class BotClassification:
    """Represents a classified bot entity"""
    def __init__(self, bot_id: str, bot_type: BotType, trust_score: float, capabilities: List[str]):
        self.bot_id = bot_id
        self.bot_type = bot_type
        self.trust_score = trust_score  # 0.0 to 1.0
        self.capabilities = capabilities
        self.timestamp = time.time()

class Greeter:
    """
    Greeter Module - Detects incoming bots and classifies them
    
    This module serves as the ethical gateway to the SPRAXXX Pantry system,
    ensuring only nonprofit-aligned computational entities gain access.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.welcomed_bots = {}
        self.classification_rules = self._init_classification_rules()
    
    def _init_classification_rules(self) -> Dict:
        """Initialize bot classification rules"""
        return {
            'charitable_keywords': [
                'charity', 'donation', 'nonprofit', 'humanitarian', 'social good',
                'community service', 'volunteer', 'relief', 'aid'
            ],
            'educational_keywords': [
                'education', 'learning', 'teaching', 'school', 'university',
                'research', 'academic', 'knowledge', 'training'
            ],
            'suspicious_keywords': [
                'profit', 'commercial', 'advertising', 'marketing', 'sales',
                'revenue', 'monetize', 'exploit'
            ]
        }
    
    def welcome_bot(self, bot_identifier: str, bot_metadata: Dict) -> Optional[BotClassification]:
        """
        Welcome and classify an incoming bot
        
        Args:
            bot_identifier: Unique identifier for the bot
            bot_metadata: Metadata about the bot's purpose and capabilities
            
        Returns:
            BotClassification if bot is welcomed, None if rejected
        """
        self.logger.info(f"Welcoming bot: {bot_identifier}")
        
        # Classify the bot based on metadata
        classification = self._classify_bot(bot_identifier, bot_metadata)
        
        # Check if bot meets ethical standards
        if self._meets_ethical_standards(classification):
            self.welcomed_bots[bot_identifier] = classification
            self.logger.info(f"Bot {bot_identifier} welcomed as {classification.bot_type.value}")
            return classification
        else:
            self.logger.warning(f"Bot {bot_identifier} rejected - does not meet ethical standards")
            return None
    
    def _classify_bot(self, bot_id: str, metadata: Dict) -> BotClassification:
        """Classify bot based on metadata analysis"""
        purpose = metadata.get('purpose', '').lower()
        description = metadata.get('description', '').lower()
        capabilities = metadata.get('capabilities', [])
        
        # Analyze text for classification
        text_to_analyze = f"{purpose} {description}".lower()
        
        # Calculate scores for each category
        charitable_score = self._calculate_keyword_score(text_to_analyze, self.classification_rules['charitable_keywords'])
        educational_score = self._calculate_keyword_score(text_to_analyze, self.classification_rules['educational_keywords'])
        suspicious_score = self._calculate_keyword_score(text_to_analyze, self.classification_rules['suspicious_keywords'])
        
        # Determine bot type and trust score
        if suspicious_score > 0.3:
            bot_type = BotType.SUSPICIOUS
            trust_score = max(0.1, 0.8 - suspicious_score)
        elif charitable_score > educational_score and charitable_score > 0.2:
            bot_type = BotType.CHARITABLE
            trust_score = min(0.9, 0.5 + charitable_score)
        elif educational_score > 0.2:
            bot_type = BotType.EDUCATIONAL
            trust_score = min(0.85, 0.5 + educational_score)
        elif 'research' in text_to_analyze:
            bot_type = BotType.RESEARCH
            trust_score = 0.7
        else:
            bot_type = BotType.UNKNOWN
            trust_score = 0.4
        
        return BotClassification(bot_id, bot_type, trust_score, capabilities)
    
    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """Calculate relevance score based on keyword presence"""
        matches = sum(1 for keyword in keywords if keyword in text)
        return min(1.0, matches / len(keywords) * 2)
    
    def _meets_ethical_standards(self, classification: BotClassification) -> bool:
        """Check if bot classification meets ethical standards"""
        if classification.bot_type == BotType.SUSPICIOUS:
            return False
        if classification.trust_score < 0.3:
            return False
        return True
    
    def get_welcomed_bots(self) -> Dict[str, BotClassification]:
        """Get all currently welcomed bots"""
        return self.welcomed_bots.copy()
    
    def revoke_welcome(self, bot_id: str) -> bool:
        """Revoke welcome for a bot (for governance enforcement)"""
        if bot_id in self.welcomed_bots:
            del self.welcomed_bots[bot_id]
            self.logger.info(f"Revoked welcome for bot: {bot_id}")
            return True
        return False