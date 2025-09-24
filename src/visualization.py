"""
SPRAXXX Pantry – Visualization Module
Purpose: Generate visual outputs for batch simulation analytics
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Install with: pip install matplotlib")


class SPRAXXXVisualizer:
    """
    Generate visual outputs for SPRAXXX Pantry batch simulations.
    Creates bar charts for yield queues and line graphs for credit ledgers.
    """
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize the SPRAXXX visualizer.
        
        Args:
            output_dir: Directory to save visualization outputs
        """
        self.output_dir = output_dir
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create the visualization output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_yield_bar_chart(self, yield_queue_data: List[Dict[str, Any]], 
                                bot_ids: List[str], 
                                title: str = "SPRAXXX Pantry Yield Production by Bot",
                                save_file: Optional[str] = None) -> str:
        """
        Generate a bar chart showing yield production by each bot.
        
        Args:
            yield_queue_data: List of yield outputs from YieldQueue
            bot_ids: List of bot identifiers
            title: Chart title
            save_file: Optional filename to save the chart
            
        Returns:
            Path to saved chart file
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Cannot generate bar chart: matplotlib not available")
            return ""
            
        # Count yields per bot (mock data for demonstration)
        yield_counts = {}
        for i, bot_id in enumerate(bot_ids):
            # In real implementation, this would analyze actual yield data
            # For demo, we'll create mock yield counts
            yield_counts[bot_id] = len([y for y in yield_queue_data if y.get('task') == 'indexing']) // len(bot_ids)
            
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bots = list(yield_counts.keys())
        yields = list(yield_counts.values())
        
        bars = ax.bar(bots, yields, color=['#2E8B57', '#4682B4', '#CD853F'], alpha=0.8)
        
        # Customize chart
        ax.set_xlabel('Bot ID', fontsize=12)
        ax.set_ylabel('Yield Units Produced', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for bar, value in zip(bars, yields):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(value)}', ha='center', va='bottom', fontsize=10)
        
        # Add nonprofit disclaimer
        plt.figtext(0.5, 0.02, 'SPRAXXX Pantry - Nonprofit Use Only', 
                   ha='center', fontsize=8, style='italic')
        
        plt.tight_layout()
        
        # Save chart
        if save_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = f"spraxxx_yield_chart_{timestamp}.png"
            
        filepath = os.path.join(self.output_dir, save_file)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Yield bar chart saved to: {filepath}")
        return filepath
        
    def generate_credit_line_graph(self, credit_ledger_data: List[Dict[str, Any]], 
                                  bot_ids: List[str],
                                  title: str = "SPRAXXX Pantry Credit Balance Over Time",
                                  save_file: Optional[str] = None) -> str:
        """
        Generate a line graph showing credit balances over time.
        
        Args:
            credit_ledger_data: List of credit entries from CreditLedger
            bot_ids: List of bot identifiers
            title: Chart title
            save_file: Optional filename to save the chart
            
        Returns:
            Path to saved chart file
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Cannot generate line graph: matplotlib not available")
            return ""
            
        # Generate mock temporal data for demonstration
        base_time = datetime.now() - timedelta(hours=24)
        time_points = [base_time + timedelta(hours=i*4) for i in range(7)]
        
        # Create mock credit accumulation data
        credit_data = {}
        for bot_id in bot_ids:
            # Simulate credit accumulation over time
            credits = []
            cumulative = 0
            for i, _ in enumerate(time_points):
                increment = (i + 1) * (hash(bot_id) % 3 + 1)  # Deterministic but varied
                cumulative += increment
                credits.append(cumulative)
            credit_data[bot_id] = credits
            
        # Create line graph
        fig, ax = plt.subplots(figsize=(12, 7))
        
        colors = ['#2E8B57', '#4682B4', '#CD853F', '#9370DB', '#DC143C']
        
        for i, (bot_id, credits) in enumerate(credit_data.items()):
            ax.plot(time_points, credits, 
                   marker='o', linewidth=2, markersize=6,
                   color=colors[i % len(colors)], 
                   label=f'{bot_id}')
        
        # Customize chart
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Cumulative Credit Units', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
        plt.xticks(rotation=45)
        
        # Add nonprofit disclaimer
        plt.figtext(0.5, 0.02, 'SPRAXXX Pantry - Nonprofit Use Only', 
                   ha='center', fontsize=8, style='italic')
        
        plt.tight_layout()
        
        # Save chart
        if save_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_file = f"spraxxx_credit_graph_{timestamp}.png"
            
        filepath = os.path.join(self.output_dir, save_file)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Credit line graph saved to: {filepath}")
        return filepath
        
    def generate_batch_simulation_report(self, yield_queue_data: List[Dict[str, Any]], 
                                       credit_ledger_data: List[Dict[str, Any]], 
                                       bot_ids: List[str],
                                       report_name: Optional[str] = None) -> Dict[str, str]:
        """
        Generate a complete visual report for batch simulation.
        
        Args:
            yield_queue_data: Yield queue contents
            credit_ledger_data: Credit ledger entries
            bot_ids: List of bot identifiers
            report_name: Optional custom report name
            
        Returns:
            Dictionary with file paths to generated visualizations
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"spraxxx_batch_report_{timestamp}"
            
        results = {}
        
        # Generate yield bar chart
        yield_chart = self.generate_yield_bar_chart(
            yield_queue_data, bot_ids, 
            save_file=f"{report_name}_yield_chart.png"
        )
        results['yield_chart'] = yield_chart
        
        # Generate credit line graph
        credit_graph = self.generate_credit_line_graph(
            credit_ledger_data, bot_ids,
            save_file=f"{report_name}_credit_graph.png"
        )
        results['credit_graph'] = credit_graph
        
        print(f"\n🎯 SPRAXXX Pantry Batch Simulation Report Generated:")
        print(f"   📊 Yield Chart: {yield_chart}")
        print(f"   📈 Credit Graph: {credit_graph}")
        print(f"   📁 Output Directory: {self.output_dir}")
        print(f"\n✨ All outputs are for nonprofit use only - SPRAXXX Legacy Foundation")
        
        return results


def add_custom_bot_example():
    """
    Example function showing how to add new bots with custom parameters.
    This demonstrates the extensibility of the SPRAXXX Pantry system.
    """
    print("\n📝 Example: Adding Custom Bots to SPRAXXX Pantry")
    print("=" * 50)
    
    # Example bot configurations
    custom_bots = [
        {
            "bot_id": "research_bot_alpha",
            "type": "academic_researcher", 
            "yield_multiplier": 1.5,
            "specialization": "climate_data"
        },
        {
            "bot_id": "education_bot_beta",
            "type": "educational_content",
            "yield_multiplier": 1.2,
            "specialization": "stem_tutorials"
        },
        {
            "bot_id": "accessibility_bot_gamma",
            "type": "accessibility_tools",
            "yield_multiplier": 2.0,
            "specialization": "text_to_speech"
        }
    ]
    
    print("Custom bot configurations:")
    for bot in custom_bots:
        print(f"  • {bot['bot_id']}: {bot['specialization']} (x{bot['yield_multiplier']} yield)")
    
    print("\nTo integrate these bots:")
    print("1. Add bot_ids to the incoming_bots list in main.py")
    print("2. Modify Kitchen.process_worker() to handle specialized types")
    print("3. Update YieldQueue to track yield multipliers")
    print("4. Run visualization to see the enhanced output")
    
    return custom_bots


def demonstrate_visualization():
    """
    Demonstration function to test visualization capabilities.
    Creates mock data and generates sample visualizations.
    """
    print("\n🎨 SPRAXXX Pantry Visualization Demonstration")
    print("=" * 50)
    
    # Create mock data similar to main.py output
    mock_yield_data = [
        {'task': 'indexing', 'result': 'metadata collected'},
        {'task': 'indexing', 'result': 'metadata collected'},
        {'task': 'indexing', 'result': 'metadata collected'}
    ]
    
    mock_credit_data = [
        {'worker': 'bot_001', 'contribution': 'metadata collected'},
        {'worker': 'bot_002', 'contribution': 'metadata collected'},
        {'worker': 'bot_003', 'contribution': 'metadata collected'}
    ]
    
    mock_bot_ids = ['bot_001', 'bot_002', 'bot_003']
    
    # Create visualizer and generate charts
    visualizer = SPRAXXXVisualizer()
    
    try:
        report = visualizer.generate_batch_simulation_report(
            mock_yield_data, mock_credit_data, mock_bot_ids
        )
        return report
    except Exception as e:
        print(f"Visualization error: {e}")
        return {}


if __name__ == "__main__":
    # Run demonstration if script is executed directly
    demonstrate_visualization()
    add_custom_bot_example()