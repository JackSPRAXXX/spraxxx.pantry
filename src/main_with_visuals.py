"""
SPRAXXX Pantry – Enhanced Main Simulation with Visual Outputs
Purpose: Demonstrate module interaction safely with visual analytics
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from greeter import Greeter
from kitchen import Kitchen
from yield_queue import YieldQueue
from credit_ledger import CreditLedger
from governance import Governance
from visualization import SPRAXXXVisualizer, add_custom_bot_example


def run_enhanced_simulation(include_custom_bots=False, generate_visuals=True):
    """
    Run the SPRAXXX Pantry simulation with optional visual outputs.
    
    Args:
        include_custom_bots: Whether to include additional custom bot examples
        generate_visuals: Whether to generate visual charts and graphs
    """
    print("🚀 SPRAXXX Pantry Enhanced Simulation Starting...")
    print("=" * 60)
    
    # Initialize modules
    greeter = Greeter()
    kitchen = Kitchen()
    yield_queue = YieldQueue()
    ledger = CreditLedger()
    governance = Governance()
    
    # Base simulation bots
    incoming_bots = ["bot_001", "bot_002", "bot_003"]
    
    # Optionally add custom bots for demonstration
    if include_custom_bots:
        custom_bots = ["research_bot_alpha", "education_bot_beta", "accessibility_bot_gamma"]
        incoming_bots.extend(custom_bots)
        print(f"📋 Processing {len(incoming_bots)} bots (including {len(custom_bots)} custom bots)")
    else:
        print(f"📋 Processing {len(incoming_bots)} standard bots")
    
    print("\n⚡ Bot Processing Pipeline:")
    
    # Simulate incoming bots
    for i, bot_id in enumerate(incoming_bots, 1):
        print(f"  {i}. Processing {bot_id}...")
        
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
                print(f"     ✓ {bot_id} contributed: {output['result']}")
            else:
                print(f"     ✗ {bot_id} output failed governance validation")
        else:
            print(f"     ⚠ {bot_id} classified as: {classification}")
    
    # Display simulation results
    print(f"\n📊 Simulation Results:")
    print(f"   • Yield Queue Entries: {len(yield_queue.get_yield())}")
    print(f"   • Credit Ledger Entries: {len(ledger.get_ledger())}")
    
    print("\n📋 Yield Queue Contents:")
    for i, yield_item in enumerate(yield_queue.get_yield(), 1):
        print(f"   {i}. Task: {yield_item['task']} | Result: {yield_item['result']}")
    
    print("\n💳 Credit Ledger Entries:")
    for i, credit_entry in enumerate(ledger.get_ledger(), 1):
        print(f"   {i}. Worker: {credit_entry['worker']} | Contribution: {credit_entry['contribution']}")
    
    # Generate visual outputs if requested
    if generate_visuals:
        print(f"\n🎨 Generating Visual Analytics...")
        
        try:
            visualizer = SPRAXXXVisualizer()
            
            # Generate comprehensive visual report
            visual_report = visualizer.generate_batch_simulation_report(
                yield_queue.get_yield(),
                ledger.get_ledger(),
                incoming_bots
            )
            
            if visual_report:
                print(f"\n📈 Visual Reports Generated Successfully!")
                return visual_report
            else:
                print(f"\n⚠ Visual generation skipped (matplotlib not available)")
                
        except Exception as e:
            print(f"\n❌ Error generating visuals: {e}")
            print("   Install matplotlib with: pip install matplotlib")
    
    print(f"\n✅ Simulation complete. All outputs are nonprofit-only and ethically processed.")
    print(f"🏛️ SPRAXXX Legacy Foundation - Serving Humanity Through Technology")
    
    return None


def demonstrate_bot_customization():
    """
    Demonstrate how to add and customize new bots in SPRAXXX Pantry.
    """
    print(f"\n🔧 Bot Customization Examples")
    print("=" * 40)
    
    # Show custom bot examples
    add_custom_bot_example()
    
    print(f"\n📚 Implementation Guide:")
    print("1. Define bot characteristics in a configuration dictionary")
    print("2. Extend Kitchen.process_worker() to handle specialized bot types")
    print("3. Update YieldQueue to track additional metadata")
    print("4. Modify CreditLedger to record specialized contributions")
    print("5. Run enhanced simulation to see customized outputs")
    
    print(f"\n🎯 Example Integration:")
    print("   incoming_bots = ['bot_001', 'research_bot_alpha', 'education_bot_beta']")
    print("   # Each bot type can have different yield multipliers and specializations")


def main():
    """
    Main execution function with options for different simulation modes.
    """
    print("🌟 SPRAXXX Pantry - Enhanced Batch Simulation")
    print("   Nonprofit Digital Infrastructure for the Public Good")
    print("   Founded by Jacquot Maple Monster Periard Raymond")
    print()
    
    # Run basic simulation with visuals
    print("🔄 Running Enhanced Simulation (Standard Mode)")
    visual_files = run_enhanced_simulation(
        include_custom_bots=False, 
        generate_visuals=True
    )
    
    # Demonstrate customization capabilities
    demonstrate_bot_customization()
    
    # Optional: Run with custom bots
    print(f"\n" + "="*60)
    print("🔄 Running Enhanced Simulation (Custom Bot Mode)")
    run_enhanced_simulation(
        include_custom_bots=True, 
        generate_visuals=False  # Skip visuals for second run
    )
    
    if visual_files:
        print(f"\n📁 Generated Files:")
        for chart_type, filepath in visual_files.items():
            print(f"   • {chart_type}: {filepath}")


if __name__ == "__main__":
    main()