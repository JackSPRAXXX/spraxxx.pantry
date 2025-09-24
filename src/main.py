"""
SPRAXXX Pantry – Main Simulation
Purpose: Demonstrate module interaction safely with environmental impact tracking
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

from greeter import Greeter
from kitchen import Kitchen
from yield_queue import YieldQueue
from credit_ledger import CreditLedger
from governance import Governance
from environmental_impact import EnvironmentalImpact

# Initialize modules
greeter = Greeter()
kitchen = Kitchen()
yield_queue = YieldQueue()
ledger = CreditLedger()
governance = Governance()
env_impact = EnvironmentalImpact()

# Simulate incoming bots
incoming_bots = ["bot_001", "bot_002", "bot_003", "bot_004", "bot_005"]

processed_count = 0
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
            
            processed_count += 1

# Calculate environmental impact
energy_savings = env_impact.calculate_energy_savings(processed_count, kitchen.energy_per_task)
comparative_analysis = env_impact.get_comparative_analysis()
policy_recommendation = env_impact.generate_policy_recommendation()

# Display simulated results
print("=== SPRAXXX PANTRY SIMULATION RESULTS ===")
print("\nYield Queue Contents:")
for i, yield_item in enumerate(yield_queue.get_yield(), 1):
    print(f"  {i}. Task: {yield_item['task']}, Energy: {yield_item['energy_consumed_wh']:.3f} Wh")

print("\nCredit Ledger Entries:")
for entry in ledger.get_ledger():
    print(f"  Worker: {entry['worker']}, Contribution: {entry['contribution']}")

print("\n=== ENVIRONMENTAL IMPACT ANALYSIS ===")
print(f"Bots Processed: {energy_savings['bots_processed']}")
print(f"Energy Waste Avoided: {energy_savings['waste_avoided_wh']:.3f} Wh")
print(f"Productive Energy Used: {energy_savings['productive_energy_used_wh']:.3f} Wh")
print(f"Net Energy Saved: {energy_savings['net_energy_saved_kwh']:.6f} kWh")
print(f"Efficiency Ratio: {energy_savings['efficiency_ratio']:.1f}%")

print("\n=== KITCHEN ENERGY METRICS ===")
kitchen_metrics = kitchen.get_energy_metrics()
print(f"Total Energy Used: {kitchen_metrics['total_energy_used_kwh']:.6f} kWh")
print(f"Average Energy per Task: {kitchen_metrics['average_energy_per_task_wh']:.3f} Wh")
print(f"Energy Efficiency Rating: {kitchen_metrics['energy_efficiency_rating']}")

print("\n=== COMPARATIVE ANALYSIS ===")
global_consumption = comparative_analysis['global_annual_consumption_twh']
print(f"Global Bot Traffic (estimated): {global_consumption['bot_traffic_estimated']} TWh/year")
print(f"ChatGPT Annual Consumption: {global_consumption['chatgpt']} TWh/year")
print(f"Total AI Bot Consumption: {global_consumption['total_ai_bots']} TWh/year")

print("\n=== CANADIAN LEGAL FRAMEWORK (CEPA) ===")
legal_data = env_impact.get_canadian_legal_framework_data()
print(f"Act: {legal_data['cepa_compliance']['act_name']}")
print("Key Applications:")
for key, value in legal_data['cepa_compliance']['application_to_bot_traffic'].items():
    print(f"  - {key.replace('_', ' ').title()}: {value}")

print("\nSimulation complete. All outputs are nonprofit-only and ethically processed.")
print("Environmental impact quantification demonstrates significant potential for energy savings.")
