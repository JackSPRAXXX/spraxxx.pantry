"""
SPRAXXX Pantry – Main Simulation
Purpose: Demonstrate module interaction safely with visual outputs
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from greeter import Greeter
from kitchen import Kitchen
from yield_queue import YieldQueue
from credit_ledger import CreditLedger
from governance import Governance

# Optional: Import visualization module if available
try:
    from visualization import SPRAXXXVisualizer
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

def main():
    """Main simulation function with optional visual outputs."""
    print("🚀 SPRAXXX Pantry Simulation Starting...")
    
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
    print("\nYield Queue Contents:")
    print(yield_queue.get_yield())

    print("\nCredit Ledger Entries:")
    print(ledger.get_ledger())

    print("\nSimulation complete. All outputs are nonprofit-only and ethically processed.")
    
    # Generate visual outputs if visualization module is available
    if VISUALIZATION_AVAILABLE:
        print("\n🎨 Generating visual analytics...")
        try:
            visualizer = SPRAXXXVisualizer()
            visual_report = visualizer.generate_batch_simulation_report(
                yield_queue.get_yield(),
                ledger.get_ledger(),
                incoming_bots
            )
            
            if visual_report:
                print("\n📊 Visual reports generated successfully!")
                print("📁 Check the 'visualizations/' directory for charts and graphs.")
        except Exception as e:
            print(f"\n⚠ Could not generate visualizations: {e}")
    else:
        print("\n💡 To generate visual charts, install matplotlib: pip install matplotlib")

if __name__ == "__main__":
    main()
