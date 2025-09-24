"""
SPRAXXX Pantry – Main Simulation
Purpose: Demonstrate module interaction safely
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from greeter import Greeter
from kitchen import Kitchen
from yield_queue import YieldQueue
from credit_ledger import CreditLedger
from governance import Governance

# Initialize modules
greeter = Greeter()
kitchen = Kitchen()
yield_queue = YieldQueue()
ledger = CreditLedger()
governance = Governance()

# Simulate incoming bots
incoming_bots = ["bot_001", "bot_002", "bot_003"]

for bot_id in incoming_bots:
    # Greeter detects bot
    classification = greeter.detect_incoming(bot_id)
    
    if classification == "worker":
        # Kitchen processes bot activity safely
        output = kitchen.process_worker(bot_id)
        
        # Governance validates output
        if governance.validate_output(output):
            # Store in Yield Queue
            yield_queue.add_yield(output)
            
            # Log contribution in Credit Ledger
            ledger.log_contribution(bot_id, output["result"])

# Display simulated results
print("Yield Queue Contents:")
print(yield_queue.get_yield())

print("\nCredit Ledger Entries:")
print(ledger.get_ledger())

print("\nSimulation complete. All outputs are nonprofit-only and ethically processed.")
