"""
Credit Ledger Module - Symbolic Acknowledgments Logging

The Credit Ledger maintains transparent records of all computational
activities and their charitable contributions for accountability.
"""

import time
import json
import logging
import hashlib
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field, asdict
from pathlib import Path

class TransactionType(Enum):
    """Types of ledger transactions"""
    BOT_WELCOME = "bot_welcome"
    TASK_SUBMISSION = "task_submission"
    TASK_COMPLETION = "task_completion"
    OUTPUT_STORAGE = "output_storage"
    OUTPUT_CONSUMPTION = "output_consumption"
    ENERGY_USAGE = "energy_usage"
    CHARITABLE_IMPACT = "charitable_impact"
    GOVERNANCE_ACTION = "governance_action"

class CreditType(Enum):
    """Types of symbolic credits"""
    COMPUTATIONAL = "computational"
    CHARITABLE = "charitable"
    EFFICIENCY = "efficiency"
    TRANSPARENCY = "transparency"
    COMMUNITY = "community"

@dataclass
class LedgerEntry:
    """Represents a single entry in the credit ledger"""
    entry_id: str
    timestamp: float
    transaction_type: TransactionType
    actor_id: str  # Bot ID, Consumer ID, or System ID
    action_description: str
    credits_awarded: Dict[CreditType, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    hash_previous: Optional[str] = None
    hash_current: Optional[str] = None
    verified: bool = False

class CreditAccount:
    """Represents a credit account for tracking symbolic acknowledgments"""
    
    def __init__(self, account_id: str, account_type: str, name: str):
        self.account_id = account_id
        self.account_type = account_type  # 'bot', 'consumer', 'system'
        self.name = name
        self.credit_balances = {credit_type: 0.0 for credit_type in CreditType}
        self.total_earned = {credit_type: 0.0 for credit_type in CreditType}
        self.transaction_count = 0
        self.created_at = time.time()
        self.last_activity = time.time()

class CreditLedger:
    """
    Credit Ledger Module - Logs symbolic acknowledgments
    
    Maintains a transparent, tamperproof record of all activities
    and their charitable contributions within the SPRAXXX Pantry ecosystem.
    """
    
    def __init__(self, ledger_file_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.ledger_entries = []
        self.credit_accounts = {}
        self.ledger_file_path = ledger_file_path or "/home/runner/work/spraxxx.pantry/spraxxx.pantry/ledger/credit_ledger.json"
        self.activity_log_path = "/home/runner/work/spraxxx.pantry/spraxxx.pantry/ledger/activity.log"
        
        # Ensure ledger directory exists
        Path(self.ledger_file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.activity_log_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing ledger if available
        self._load_ledger()
        
        # Initialize logging
        self._setup_activity_logging()
    
    def _setup_activity_logging(self):
        """Setup activity logging to file"""
        activity_logger = logging.getLogger('pantry_activity')
        activity_logger.setLevel(logging.INFO)
        
        # Create file handler if not exists
        if not activity_logger.handlers:
            handler = logging.FileHandler(self.activity_log_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            activity_logger.addHandler(handler)
    
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        timestamp = str(time.time())
        entry_count = str(len(self.ledger_entries))
        return hashlib.sha256(f"{timestamp}_{entry_count}".encode()).hexdigest()[:16]
    
    def _calculate_hash(self, entry: LedgerEntry) -> str:
        """Calculate hash for ledger entry"""
        entry_data = {
            'entry_id': entry.entry_id,
            'timestamp': entry.timestamp,
            'transaction_type': entry.transaction_type.value,
            'actor_id': entry.actor_id,
            'action_description': entry.action_description,
            'credits_awarded': {k.value: v for k, v in entry.credits_awarded.items()},
            'metadata': entry.metadata,
            'hash_previous': entry.hash_previous
        }
        
        data_string = json.dumps(entry_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def record_transaction(self, transaction_type: TransactionType, actor_id: str,
                          action_description: str, credits_awarded: Dict[CreditType, float] = None,
                          metadata: Dict[str, Any] = None) -> str:
        """
        Record a transaction in the ledger
        
        Args:
            transaction_type: Type of transaction being recorded
            actor_id: ID of the entity performing the action
            action_description: Human-readable description of the action
            credits_awarded: Credits to award for this transaction
            metadata: Additional metadata about the transaction
            
        Returns:
            Entry ID for the recorded transaction
        """
        entry_id = self._generate_entry_id()
        
        # Get previous hash for chain integrity
        previous_hash = None
        if self.ledger_entries:
            previous_hash = self.ledger_entries[-1].hash_current
        
        # Create ledger entry
        entry = LedgerEntry(
            entry_id=entry_id,
            timestamp=time.time(),
            transaction_type=transaction_type,
            actor_id=actor_id,
            action_description=action_description,
            credits_awarded=credits_awarded or {},
            metadata=metadata or {},
            hash_previous=previous_hash
        )
        
        # Calculate hash for this entry
        entry.hash_current = self._calculate_hash(entry)
        entry.verified = True
        
        # Add to ledger
        self.ledger_entries.append(entry)
        
        # Update credit accounts
        self._update_credit_account(actor_id, credits_awarded or {})
        
        # Log activity
        activity_logger = logging.getLogger('pantry_activity')
        activity_logger.info(f"TRANSACTION: {transaction_type.value} | {actor_id} | {action_description}")
        
        self.logger.info(f"Recorded transaction {entry_id}: {action_description}")
        
        # Save ledger
        self._save_ledger()
        
        return entry_id
    
    def _update_credit_account(self, actor_id: str, credits_awarded: Dict[CreditType, float]):
        """Update credit account balances"""
        if actor_id not in self.credit_accounts:
            # Create new account
            account_type = 'system'
            if actor_id.startswith('bot_'):
                account_type = 'bot'
            elif actor_id.startswith('consumer_'):
                account_type = 'consumer'
            
            self.credit_accounts[actor_id] = CreditAccount(
                actor_id, account_type, actor_id
            )
        
        account = self.credit_accounts[actor_id]
        
        # Update balances and totals
        for credit_type, amount in credits_awarded.items():
            account.credit_balances[credit_type] += amount
            account.total_earned[credit_type] += amount
        
        account.transaction_count += 1
        account.last_activity = time.time()
    
    def award_credits(self, actor_id: str, credit_type: CreditType, amount: float, reason: str) -> str:
        """
        Award credits to an actor
        
        Args:
            actor_id: ID of the actor receiving credits
            credit_type: Type of credit being awarded
            amount: Amount of credits to award
            reason: Reason for the credit award
            
        Returns:
            Entry ID for the credit award transaction
        """
        return self.record_transaction(
            TransactionType.CHARITABLE_IMPACT,
            actor_id,
            f"Credit award: {reason}",
            {credit_type: amount},
            {'award_reason': reason, 'credit_type': credit_type.value}
        )
    
    def get_credit_balance(self, actor_id: str, credit_type: CreditType = None) -> Dict[CreditType, float]:
        """
        Get credit balance for an actor
        
        Args:
            actor_id: ID of the actor
            credit_type: Specific credit type (returns all if None)
            
        Returns:
            Dictionary of credit balances
        """
        if actor_id not in self.credit_accounts:
            return {credit_type: 0.0} if credit_type else {ct: 0.0 for ct in CreditType}
        
        account = self.credit_accounts[actor_id]
        
        if credit_type:
            return {credit_type: account.credit_balances[credit_type]}
        else:
            return account.credit_balances.copy()
    
    def get_account_summary(self, actor_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive account summary"""
        if actor_id not in self.credit_accounts:
            return None
        
        account = self.credit_accounts[actor_id]
        
        return {
            'account_id': account.account_id,
            'account_type': account.account_type,
            'name': account.name,
            'credit_balances': {ct.value: balance for ct, balance in account.credit_balances.items()},
            'total_earned': {ct.value: total for ct, total in account.total_earned.items()},
            'transaction_count': account.transaction_count,
            'created_at': account.created_at,
            'last_activity': account.last_activity,
            'account_age_days': (time.time() - account.created_at) / 86400
        }
    
    def get_ledger_statistics(self) -> Dict[str, Any]:
        """Get comprehensive ledger statistics"""
        transaction_counts = {}
        total_credits_by_type = {ct: 0.0 for ct in CreditType}
        
        for entry in self.ledger_entries:
            # Count transactions by type
            tx_type = entry.transaction_type.value
            transaction_counts[tx_type] = transaction_counts.get(tx_type, 0) + 1
            
            # Sum credits by type
            for credit_type, amount in entry.credits_awarded.items():
                total_credits_by_type[credit_type] += amount
        
        return {
            'total_entries': len(self.ledger_entries),
            'total_accounts': len(self.credit_accounts),
            'transaction_counts': transaction_counts,
            'total_credits_awarded': {ct.value: total for ct, total in total_credits_by_type.items()},
            'ledger_integrity': self._verify_ledger_integrity(),
            'oldest_entry_age_hours': (
                (time.time() - self.ledger_entries[0].timestamp) / 3600 
                if self.ledger_entries else 0
            )
        }
    
    def _verify_ledger_integrity(self) -> bool:
        """Verify the integrity of the ledger chain"""
        if not self.ledger_entries:
            return True
        
        for i, entry in enumerate(self.ledger_entries):
            # Verify hash
            calculated_hash = self._calculate_hash(entry)
            if calculated_hash != entry.hash_current:
                self.logger.error(f"Hash mismatch in entry {entry.entry_id}")
                return False
            
            # Verify chain
            if i > 0:
                previous_entry = self.ledger_entries[i-1]
                if entry.hash_previous != previous_entry.hash_current:
                    self.logger.error(f"Chain break at entry {entry.entry_id}")
                    return False
        
        return True
    
    def get_transactions_by_actor(self, actor_id: str, limit: int = 50) -> List[LedgerEntry]:
        """Get recent transactions for a specific actor"""
        actor_transactions = [
            entry for entry in self.ledger_entries 
            if entry.actor_id == actor_id
        ]
        
        # Return most recent first
        return sorted(actor_transactions, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_transactions_by_type(self, transaction_type: TransactionType, limit: int = 50) -> List[LedgerEntry]:
        """Get recent transactions of a specific type"""
        type_transactions = [
            entry for entry in self.ledger_entries
            if entry.transaction_type == transaction_type
        ]
        
        return sorted(type_transactions, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def generate_transparency_report(self) -> Dict[str, Any]:
        """Generate comprehensive transparency report"""
        stats = self.get_ledger_statistics()
        
        # Top contributors by credit type
        top_contributors = {}
        for credit_type in CreditType:
            contributors = []
            for account_id, account in self.credit_accounts.items():
                total_earned = account.total_earned[credit_type]
                if total_earned > 0:
                    contributors.append({
                        'account_id': account_id,
                        'name': account.name,
                        'total_earned': total_earned
                    })
            
            top_contributors[credit_type.value] = sorted(
                contributors, 
                key=lambda x: x['total_earned'], 
                reverse=True
            )[:10]
        
        return {
            'report_generated_at': time.time(),
            'ledger_statistics': stats,
            'top_contributors_by_credit_type': top_contributors,
            'integrity_verified': self._verify_ledger_integrity(),
            'total_charitable_impact': sum(
                entry.credits_awarded.get(CreditType.CHARITABLE, 0.0)
                for entry in self.ledger_entries
            )
        }
    
    def _save_ledger(self):
        """Save ledger to file"""
        try:
            # Convert entries to dict format
            entries_data = []
            for entry in self.ledger_entries:
                entry_dict = {
                    'entry_id': entry.entry_id,
                    'timestamp': entry.timestamp,
                    'transaction_type': entry.transaction_type.value,
                    'actor_id': entry.actor_id,
                    'action_description': entry.action_description,
                    'credits_awarded': {k.value: v for k, v in entry.credits_awarded.items()},
                    'metadata': entry.metadata,
                    'hash_previous': entry.hash_previous,
                    'hash_current': entry.hash_current,
                    'verified': entry.verified
                }
                entries_data.append(entry_dict)
            
            # Convert accounts to dict format
            accounts_data = {}
            for account_id, account in self.credit_accounts.items():
                accounts_data[account_id] = {
                    'account_id': account.account_id,
                    'account_type': account.account_type,
                    'name': account.name,
                    'credit_balances': {k.value: v for k, v in account.credit_balances.items()},
                    'total_earned': {k.value: v for k, v in account.total_earned.items()},
                    'transaction_count': account.transaction_count,
                    'created_at': account.created_at,
                    'last_activity': account.last_activity
                }
            
            ledger_data = {
                'entries': entries_data,
                'accounts': accounts_data
            }
            
            with open(self.ledger_file_path, 'w') as f:
                json.dump(ledger_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save ledger: {str(e)}")
    
    def _load_ledger(self):
        """Load ledger from file if it exists"""
        try:
            if Path(self.ledger_file_path).exists():
                with open(self.ledger_file_path, 'r') as f:
                    ledger_data = json.load(f)
                
                # Load entries
                for entry_data in ledger_data.get('entries', []):
                    entry = LedgerEntry(
                        entry_id=entry_data['entry_id'],
                        timestamp=entry_data['timestamp'],
                        transaction_type=TransactionType(entry_data['transaction_type']),
                        actor_id=entry_data['actor_id'],
                        action_description=entry_data['action_description'],
                        credits_awarded={
                            CreditType(k): v for k, v in entry_data['credits_awarded'].items()
                        },
                        metadata=entry_data['metadata'],
                        hash_previous=entry_data['hash_previous'],
                        hash_current=entry_data['hash_current'],
                        verified=entry_data['verified']
                    )
                    self.ledger_entries.append(entry)
                
                # Load accounts
                for account_id, account_data in ledger_data.get('accounts', {}).items():
                    account = CreditAccount(
                        account_data['account_id'],
                        account_data['account_type'],
                        account_data['name']
                    )
                    account.credit_balances = {
                        CreditType(k): v for k, v in account_data['credit_balances'].items()
                    }
                    account.total_earned = {
                        CreditType(k): v for k, v in account_data['total_earned'].items()
                    }
                    account.transaction_count = account_data['transaction_count']
                    account.created_at = account_data['created_at']
                    account.last_activity = account_data['last_activity']
                    
                    self.credit_accounts[account_id] = account
                
                self.logger.info(f"Loaded ledger with {len(self.ledger_entries)} entries")
                
        except Exception as e:
            self.logger.warning(f"Failed to load existing ledger: {str(e)}")
            # Start with empty ledger