#!/usr/bin/env python3
"""
Energy and Resource Projections for SPRAXXX Pantry

Simulates energy usage, efficiency metrics, and charitable impact
projections for the SPRAXXX Pantry system.
"""

import time
import json
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class EnergyMetrics:
    """Energy usage and efficiency metrics"""
    total_energy_consumed: float
    energy_per_task: float
    efficiency_ratio: float
    waste_percentage: float
    renewable_percentage: float
    charitable_impact_per_unit: float

@dataclass
class ProjectionScenario:
    """Projection scenario parameters"""
    name: str
    bot_count: int
    tasks_per_hour: int
    task_complexity_avg: float
    efficiency_target: float
    charitable_orgs: int
    simulation_hours: int

class EnergyProjectionSimulator:
    """Simulates energy usage and charitable impact projections"""
    
    def __init__(self):
        self.scenarios = []
        self.results = {}
        
        # Energy constants (arbitrary units for demonstration)
        self.base_energy_per_task = 1.0
        self.complexity_multiplier = 1.5
        self.efficiency_bonus = 0.2
        self.overhead_energy = 0.1
        
    def add_scenario(self, scenario: ProjectionScenario):
        """Add a projection scenario"""
        self.scenarios.append(scenario)
    
    def run_simulation(self, scenario: ProjectionScenario) -> Dict[str, Any]:
        """Run energy projection simulation for a scenario"""
        print(f"Running simulation: {scenario.name}")
        
        # Initialize metrics
        hourly_data = []
        cumulative_energy = 0.0
        cumulative_tasks = 0
        cumulative_impact = 0.0
        
        for hour in range(scenario.simulation_hours):
            # Simulate tasks for this hour
            tasks_this_hour = self._simulate_hourly_tasks(scenario, hour)
            
            # Calculate energy usage
            energy_this_hour = self._calculate_energy_usage(tasks_this_hour, scenario)
            
            # Calculate charitable impact
            impact_this_hour = self._calculate_charitable_impact(tasks_this_hour, energy_this_hour)
            
            # Update cumulatives
            cumulative_energy += energy_this_hour
            cumulative_tasks += len(tasks_this_hour)
            cumulative_impact += impact_this_hour
            
            # Calculate efficiency metrics
            efficiency = self._calculate_efficiency(energy_this_hour, len(tasks_this_hour), scenario)
            
            # Store hourly data
            hourly_data.append({
                'hour': hour,
                'tasks_processed': len(tasks_this_hour),
                'energy_consumed': energy_this_hour,
                'charitable_impact': impact_this_hour,
                'efficiency_ratio': efficiency,
                'cumulative_energy': cumulative_energy,
                'cumulative_tasks': cumulative_tasks,
                'cumulative_impact': cumulative_impact
            })
        
        # Calculate final metrics
        final_metrics = EnergyMetrics(
            total_energy_consumed=cumulative_energy,
            energy_per_task=cumulative_energy / max(1, cumulative_tasks),
            efficiency_ratio=cumulative_impact / max(0.1, cumulative_energy),
            waste_percentage=max(0, (cumulative_energy - cumulative_impact) / cumulative_energy * 100),
            renewable_percentage=85.0,  # Assumed renewable energy usage
            charitable_impact_per_unit=cumulative_impact / max(0.1, cumulative_energy)
        )
        
        return {
            'scenario': asdict(scenario),
            'metrics': asdict(final_metrics),
            'hourly_data': hourly_data,
            'summary': self._generate_summary(scenario, final_metrics, hourly_data)
        }
    
    def _simulate_hourly_tasks(self, scenario: ProjectionScenario, hour: int) -> List[Dict[str, Any]]:
        """Simulate tasks for a specific hour"""
        # Add some randomness and patterns
        base_tasks = scenario.tasks_per_hour
        
        # Peak hours simulation (more tasks during business hours)
        hour_of_day = hour % 24
        if 9 <= hour_of_day <= 17:  # Business hours
            multiplier = 1.5
        elif 18 <= hour_of_day <= 22:  # Evening peak
            multiplier = 1.2
        else:  # Off hours
            multiplier = 0.7
        
        # Add random variation
        variation = random.uniform(0.8, 1.2)
        actual_tasks = int(base_tasks * multiplier * variation)
        
        tasks = []
        for i in range(actual_tasks):
            task_complexity = random.gauss(scenario.task_complexity_avg, 0.3)
            task_complexity = max(0.1, min(3.0, task_complexity))  # Clamp between 0.1 and 3.0
            
            task_type = random.choice(['data_analysis', 'text_processing', 'calculation', 'research_task', 'community_service'])
            
            tasks.append({
                'id': f"task_{hour}_{i}",
                'type': task_type,
                'complexity': task_complexity,
                'charitable_priority': random.uniform(0.3, 1.0)
            })
        
        return tasks
    
    def _calculate_energy_usage(self, tasks: List[Dict[str, Any]], scenario: ProjectionScenario) -> float:
        """Calculate energy usage for tasks"""
        total_energy = 0.0
        
        for task in tasks:
            # Base energy calculation
            base_energy = self.base_energy_per_task * task['complexity']
            
            # Task type modifiers
            type_modifiers = {
                'data_analysis': 1.5,
                'text_processing': 1.0,
                'calculation': 0.8,
                'research_task': 2.0,
                'community_service': 1.2
            }
            
            type_modifier = type_modifiers.get(task['type'], 1.0)
            task_energy = base_energy * type_modifier
            
            # Efficiency improvements
            efficiency_factor = min(1.0, scenario.efficiency_target)
            task_energy *= (2.0 - efficiency_factor)  # Better efficiency reduces energy
            
            total_energy += task_energy
        
        # Add system overhead
        total_energy += self.overhead_energy * len(tasks)
        
        return total_energy
    
    def _calculate_charitable_impact(self, tasks: List[Dict[str, Any]], energy_consumed: float) -> float:
        """Calculate charitable impact for tasks"""
        impact = 0.0
        
        for task in tasks:
            # Impact based on charitable priority and energy efficiency
            task_impact = task['charitable_priority'] * task['complexity'] * 0.8
            impact += task_impact
        
        # Bonus for energy efficiency
        if energy_consumed > 0:
            efficiency_bonus = min(1.0, impact / energy_consumed) * 0.1
            impact += efficiency_bonus
        
        return impact
    
    def _calculate_efficiency(self, energy_consumed: float, tasks_processed: int, scenario: ProjectionScenario) -> float:
        """Calculate efficiency ratio for the hour"""
        if energy_consumed <= 0:
            return 0.0
        
        # Efficiency = useful work / energy consumed
        # Target efficiency should be achievable with good practices
        theoretical_min_energy = tasks_processed * self.base_energy_per_task * 0.8
        efficiency = min(1.0, theoretical_min_energy / energy_consumed)
        
        return efficiency
    
    def _generate_summary(self, scenario: ProjectionScenario, metrics: EnergyMetrics, hourly_data: List[Dict]) -> Dict[str, Any]:
        """Generate summary insights for the simulation"""
        peak_hour = max(hourly_data, key=lambda x: x['tasks_processed'])
        min_hour = min(hourly_data, key=lambda x: x['tasks_processed'])
        
        return {
            'simulation_completed_at': time.time(),
            'efficiency_rating': 'Excellent' if metrics.efficiency_ratio > 0.8 else 
                               'Good' if metrics.efficiency_ratio > 0.6 else
                               'Fair' if metrics.efficiency_ratio > 0.4 else 'Poor',
            'peak_utilization': {
                'hour': peak_hour['hour'],
                'tasks': peak_hour['tasks_processed'],
                'energy': peak_hour['energy_consumed']
            },
            'lowest_utilization': {
                'hour': min_hour['hour'],
                'tasks': min_hour['tasks_processed'],
                'energy': min_hour['energy_consumed']
            },
            'sustainability_score': (metrics.renewable_percentage + (100 - metrics.waste_percentage)) / 2,
            'charitable_effectiveness': metrics.charitable_impact_per_unit,
            'recommendations': self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: EnergyMetrics) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if metrics.efficiency_ratio < 0.6:
            recommendations.append("Consider optimizing task processing algorithms to improve energy efficiency")
        
        if metrics.waste_percentage > 20:
            recommendations.append("Implement better resource allocation to reduce energy waste")
        
        if metrics.charitable_impact_per_unit < 0.5:
            recommendations.append("Focus on higher-impact charitable tasks to maximize benefit per energy unit")
        
        if metrics.energy_per_task > 2.0:
            recommendations.append("Review task complexity and processing methods to reduce per-task energy consumption")
        
        if not recommendations:
            recommendations.append("System is performing well - maintain current practices")
        
        return recommendations
    
    def run_all_scenarios(self) -> Dict[str, Any]:
        """Run all scenarios and compile results"""
        all_results = {}
        
        for scenario in self.scenarios:
            results = self.run_simulation(scenario)
            all_results[scenario.name] = results
        
        # Generate comparative analysis
        comparative_analysis = self._generate_comparative_analysis(all_results)
        
        return {
            'individual_results': all_results,
            'comparative_analysis': comparative_analysis,
            'generated_at': time.time()
        }
    
    def _generate_comparative_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparative analysis across scenarios"""
        if not results:
            return {}
        
        scenarios_data = []
        for name, result in results.items():
            scenarios_data.append({
                'name': name,
                'efficiency': result['metrics']['efficiency_ratio'],
                'impact_per_unit': result['metrics']['charitable_impact_per_unit'],
                'total_energy': result['metrics']['total_energy_consumed'],
                'waste_percentage': result['metrics']['waste_percentage']
            })
        
        # Find best and worst performers
        best_efficiency = max(scenarios_data, key=lambda x: x['efficiency'])
        best_impact = max(scenarios_data, key=lambda x: x['impact_per_unit'])
        lowest_waste = min(scenarios_data, key=lambda x: x['waste_percentage'])
        
        return {
            'best_efficiency_scenario': best_efficiency['name'],
            'highest_impact_scenario': best_impact['name'],
            'lowest_waste_scenario': lowest_waste['name'],
            'average_efficiency': sum(s['efficiency'] for s in scenarios_data) / len(scenarios_data),
            'total_projected_energy': sum(s['total_energy'] for s in scenarios_data),
            'recommendations_summary': [
                "Choose scenarios with efficiency ratio > 0.7 for optimal resource utilization",
                "Prioritize scenarios with high charitable impact per energy unit",
                "Minimize waste percentage through better task matching and processing optimization"
            ]
        }
    
    def save_results(self, filename: str = None):
        """Save simulation results to file"""
        if not filename:
            filename = f"/home/runner/work/spraxxx.pantry/spraxxx.pantry/simulations/energy_projections_{int(time.time())}.json"
        
        results = self.run_all_scenarios()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {filename}")
        return filename

def main():
    """Run energy projection simulations"""
    print("SPRAXXX Pantry - Energy & Charitable Impact Projections")
    print("=" * 60)
    
    simulator = EnergyProjectionSimulator()
    
    # Define scenarios
    scenarios = [
        ProjectionScenario(
            name="Small Community Deployment",
            bot_count=5,
            tasks_per_hour=10,
            task_complexity_avg=1.0,
            efficiency_target=0.8,
            charitable_orgs=3,
            simulation_hours=168  # 1 week
        ),
        ProjectionScenario(
            name="Medium Scale Operations",
            bot_count=25,
            tasks_per_hour=50,
            task_complexity_avg=1.2,
            efficiency_target=0.75,
            charitable_orgs=15,
            simulation_hours=720  # 1 month
        ),
        ProjectionScenario(
            name="Large Scale Deployment",
            bot_count=100,
            tasks_per_hour=200,
            task_complexity_avg=1.5,
            efficiency_target=0.7,
            charitable_orgs=50,
            simulation_hours=8760  # 1 year
        ),
        ProjectionScenario(
            name="Optimized High Efficiency",
            bot_count=50,
            tasks_per_hour=100,
            task_complexity_avg=1.1,
            efficiency_target=0.9,
            charitable_orgs=25,
            simulation_hours=2160  # 3 months
        )
    ]
    
    for scenario in scenarios:
        simulator.add_scenario(scenario)
    
    # Run simulations
    results_file = simulator.save_results()
    
    print("\nSimulation Summary:")
    print(f"Results saved to: {results_file}")
    print("\nKey Insights:")
    print("- Energy efficiency improves with optimized processing")
    print("- Charitable impact scales with proper resource allocation")
    print("- Waste reduction is crucial for sustainability")
    print("- Peak hour management affects overall efficiency")
    
    return results_file

if __name__ == "__main__":
    main()