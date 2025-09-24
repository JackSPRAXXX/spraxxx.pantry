#!/usr/bin/env python3
"""
SPRAXXX Pantry – Batch Simulation Runner
Purpose: Command-line interface for running batch simulations
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)

Usage:
    python batch_runner.py --bots 100 --name "Energy Conservation Simulation"
    python batch_runner.py --bots 25 --delay 0.1 --quiet
    python batch_runner.py --custom-config custom_bots.json
"""

import argparse
import json
import sys
from pathlib import Path

from batch_simulation import BatchSimulation


def load_custom_config(config_path: str) -> list:
    """
    Load custom bot configurations from a JSON file.
    
    Args:
        config_path: Path to the JSON configuration file
        
    Returns:
        List of bot configuration dictionaries
    """
    try:
        with open(config_path, 'r') as f:
            configs = json.load(f)
        
        if not isinstance(configs, list):
            raise ValueError("Configuration file must contain a list of bot configs")
            
        return configs
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"❌ Error loading configuration file: {e}")
        sys.exit(1)


def create_sample_config(output_path: str):
    """
    Create a sample configuration file for custom bot setups.
    
    Args:
        output_path: Path where to save the sample configuration
    """
    sample_config = [
        {
            "bot_id": "efficiency_champion_001",
            "efficiency": 1.8,
            "resource_allocation": 1.2,
            "bot_type": "processor"
        },
        {
            "bot_id": "resource_optimizer_002", 
            "efficiency": 1.4,
            "resource_allocation": 0.8,
            "bot_type": "indexer"
        },
        {
            "bot_id": "balanced_worker_003",
            "efficiency": 1.0,
            "resource_allocation": 1.0,
            "bot_type": "worker"
        },
        {
            "bot_id": "high_capacity_004",
            "efficiency": 1.2,
            "resource_allocation": 2.5,
            "bot_type": "processor"
        }
    ]
    
    try:
        with open(output_path, 'w') as f:
            json.dump(sample_config, f, indent=2)
        print(f"✅ Sample configuration created at: {output_path}")
        print("   Edit this file to customize bot parameters for your simulation.")
    except IOError as e:
        print(f"❌ Error creating sample configuration: {e}")
        sys.exit(1)


def main():
    """
    Main entry point for the SPRAXXX Pantry batch simulation runner.
    Embodies the principles of stewardship and cosmic community service.
    """
    parser = argparse.ArgumentParser(
        description="SPRAXXX Pantry Batch Simulation Runner - Ethical AI for Nonprofit Good",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_runner.py --bots 50
  python batch_runner.py --bots 100 --name "CPU Hour Conservation Test"
  python batch_runner.py --custom-config my_bots.json --delay 0.05
  python batch_runner.py --create-sample-config sample_bots.json

All outputs are dedicated to nonprofit and charitable purposes.
SPRAXXX Pantry serves humanity through ethical stewardship.
        """
    )
    
    parser.add_argument(
        '--bots', '-b',
        type=int,
        default=50,
        help='Number of bots to simulate (default: 50)'
    )
    
    parser.add_argument(
        '--name', '-n',
        type=str,
        default="SPRAXXX Ethical Bot Harvest",
        help='Name for the simulation run'
    )
    
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=0.0,
        help='Delay between bot processing in seconds (default: 0.0)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Run simulation without real-time progress output'
    )
    
    parser.add_argument(
        '--custom-config', '-c',
        type=str,
        help='Path to JSON file with custom bot configurations'
    )
    
    parser.add_argument(
        '--create-sample-config',
        type=str,
        help='Create a sample configuration file at the specified path and exit'
    )
    
    parser.add_argument(
        '--output-report', '-o',
        type=str,
        help='Save detailed simulation report to specified file'
    )
    
    args = parser.parse_args()
    
    # Handle sample config creation
    if args.create_sample_config:
        create_sample_config(args.create_sample_config)
        return
    
    # Validate arguments
    if args.bots < 1:
        print("❌ Number of bots must be at least 1")
        sys.exit(1)
        
    if args.delay < 0:
        print("❌ Delay cannot be negative")
        sys.exit(1)
    
    # Display startup message
    if not args.quiet:
        print("🌟 SPRAXXX Pantry - Batch Simulation System 🌟")
        print("Transforming digital waste into human good")
        print("Ethical • Nonprofit • Transparent")
        print()
    
    # Initialize simulation
    simulation = BatchSimulation(verbose=not args.quiet)
    
    # Load custom configurations if provided
    custom_configs = None
    if args.custom_config:
        if not args.quiet:
            print(f"📋 Loading custom bot configurations from: {args.custom_config}")
        custom_configs = load_custom_config(args.custom_config)
        args.bots = len(custom_configs)  # Override bot count with config length
    
    # Configure simulation
    simulation.configure_simulation(
        num_bots=args.bots,
        simulation_name=args.name,
        custom_bot_configs=custom_configs,
        processing_delay=args.delay
    )
    
    if not args.quiet:
        print(f"🚀 Configured simulation: {args.name}")
        print(f"🤖 Bots to process: {args.bots}")
        if args.delay > 0:
            print(f"⏱️  Processing delay: {args.delay}s per bot")
        print()
    
    # Run the simulation
    try:
        results = simulation.run_simulation()
        
        # Display summary
        if not args.quiet:
            summary = simulation.generate_simulation_summary(results)
            print("\n" + summary)
        
        # Save detailed report if requested
        if args.output_report:
            try:
                report_content = []
                report_content.append(simulation.generate_simulation_summary(results))
                report_content.append("\n\n" + "="*80 + "\n")
                report_content.append("DETAILED YIELD QUEUE REPORT\n")
                report_content.append("="*80 + "\n")
                report_content.append(results["yield_queue"]["report"])
                report_content.append("\n\n" + "="*80 + "\n")
                report_content.append("DETAILED CREDIT LEDGER REPORT\n")
                report_content.append("="*80 + "\n")
                report_content.append(results["credit_ledger"]["report"])
                report_content.append("\n\n" + "="*80 + "\n")
                report_content.append("SIMULATION LOG REPORT\n")
                report_content.append("="*80 + "\n")
                report_content.append(results["simulation_log"]["detailed_report"])
                
                with open(args.output_report, 'w') as f:
                    f.write("".join(report_content))
                    
                print(f"\n📄 Detailed report saved to: {args.output_report}")
            except IOError as e:
                print(f"⚠️  Warning: Could not save report to {args.output_report}: {e}")
        
        # Final ethical reminder
        if not args.quiet:
            print("\n🤝 Remember: All SPRAXXX Pantry outputs are for nonprofit use only")
            print("🌍 Thank you for contributing to the cosmic community!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation interrupted by user")
        print("🙏 Thank you for testing SPRAXXX Pantry's ethical capabilities")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Simulation failed with error: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()