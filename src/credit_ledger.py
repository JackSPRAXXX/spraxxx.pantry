"""
SPRAXXX Pantry – Credit Ledger Module
Purpose: Log symbolic acknowledgments of contributions
Ethical: Nonprofit-only, no monetization
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

class CreditLedger:
    def __init__(self):
        self.ledger = []

    def log_contribution(self, worker_id, contribution):
        """Log a symbolic credit for a worker."""
        self.ledger.append({"worker": worker_id, "contribution": contribution})

    def get_ledger(self):
        """Retrieve all logged contributions."""
        return self.ledger
