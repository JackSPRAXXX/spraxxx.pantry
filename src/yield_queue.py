"""
SPRAXXX Pantry – Yield Queue Module
Purpose: Store outputs from Kitchen for nonprofit consumption
Ethical: Nonprofit-only
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

class YieldQueue:
    def __init__(self):
        self.queue = []

    def add_yield(self, yield_output):
        """Add a Kitchen output to the queue."""
        self.queue.append(yield_output)

    def get_yield(self):
        """Retrieve all queued outputs for nonprofit consumption."""
        return self.queue
