#!/usr/bin/env python3
"""
Credit and Symbolic Acknowledgment Projections for SPRAXXX Pantry

Simulates the accumulation and distribution of symbolic credits
across the ecosystem to project community engagement and impact.
"""

import time
import json
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

class CreditType(Enum):
    """Types of symbolic credits (matching credit_ledger.py)"""
    COMPUTATIONAL = "computational"
    CHARITABLE = "charitable"
    EFFICIENCY = "efficiency"
    TRANSPARENCY = "transparency"
    COMMUNITY = "community"

@dataclass
class CreditProjection:
    """Projected credit accumulation over time"""
    scenario_name: str
    time_period_days: int
    total_credits_awarded: Dict[str, float]
    credits_per_day: Dict[str, float]
    top_contributors: List[Dict[str, Any]]
    distribution_metrics: Dict[str, float]
    community_health_score: float

class CreditProjectionSimulator:
    """Simulates symbolic credit accumulation and community dynamics"""
    
    def __init__(self):
        self.scenarios = []
        self.bot_profiles = self._create_bot_profiles()
        self.consumer_profiles = self._create_consumer_profiles()
        
    def _create_bot_profiles(self) -> List[Dict[str, Any]]:
        """Create diverse bot profiles for simulation"""
        return [
            {
                'id': 'charitable_analyzer',
                'type': 'charitable',
                'activity_level': 0.8,
                'efficiency': 0.9,
                'task_preference': ['data_analysis', 'research_task'],
                'credit_multiplier': 1.2
            },
            {
                'id': 'education_helper',
                'type': 'educational',
                'activity_level': 0.7,
                'efficiency': 0.8,
                'task_preference': ['text_processing', 'community_service'],
                'credit_multiplier': 1.1
            },
            {
                'id': 'research_bot',
                'type': 'research',
                'activity_level': 0.6,
                'efficiency': 0.85,
                'task_preference': ['research_task', 'calculation'],
                'credit_multiplier': 1.0
            },
            {
                'id': 'community_supporter',
                'type': 'charitable',
                'activity_level': 0.9,
                'efficiency': 0.7,
                'task_preference': ['community_service', 'text_processing'],
                'credit_multiplier': 1.3
            },
            {
                'id': 'efficiency_optimizer',
                'type': 'research',
                'activity_level': 0.5,
                'efficiency': 0.95,
                'task_preference': ['calculation', 'data_analysis'],
                'credit_multiplier': 0.9
            }
        ]
    
    def _create_consumer_profiles(self) -> List[Dict[str, Any]]:
        """Create charitable consumer profiles"""
        return [
            {
                'id': 'local_food_bank',
                'type': 'food_security',
                'consumption_rate': 0.8,
                'impact_multiplier': 1.4,
                'preferred_outputs': ['data_analysis', 'community_service']
            },
            {
                'id': 'education_nonprofit',
                'type': 'education',
                'consumption_rate': 0.6,
                'impact_multiplier': 1.2,
                'preferred_outputs': ['text_processing', 'research_task']
            },
            {
                'id': 'healthcare_charity',
                'type': 'healthcare',
                'consumption_rate': 0.9,
                'impact_multiplier': 1.5,
                'preferred_outputs': ['data_analysis', 'research_task']
            },
            {
                'id': 'environmental_org',
                'type': 'environment',
                'consumption_rate': 0.7,
                'impact_multiplier': 1.3,
                'preferred_outputs': ['research_task', 'calculation']
            }
        ]
    
    def simulate_daily_activity(self, day: int, scenario_params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate one day of credit-generating activity"""
        daily_credits = {credit_type.value: 0.0 for credit_type in CreditType}
        daily_activities = []
        
        # Simulate bot activities
        active_bots = random.sample(
            self.bot_profiles, 
            min(len(self.bot_profiles), scenario_params.get('active_bots_per_day', 3))
        )
        
        for bot in active_bots:
            # Determine if bot is active today
            if random.random() < bot['activity_level']:
                # Simulate tasks
                num_tasks = random.randint(1, scenario_params.get('max_tasks_per_bot', 5))
                
                for _ in range(num_tasks):
                    task_credits = self._simulate_task_completion(bot, scenario_params)
                    
                    for credit_type, amount in task_credits.items():
                        daily_credits[credit_type] += amount
                    
                    daily_activities.append({
                        'type': 'task_completion',
                        'bot_id': bot['id'],
                        'credits_awarded': task_credits,
                        'day': day
                    })
        
        # Simulate consumer activities
        active_consumers = random.sample(
            self.consumer_profiles,
            min(len(self.consumer_profiles), scenario_params.get('active_consumers_per_day', 2))
        )
        
        for consumer in active_consumers:
            if random.random() < consumer['consumption_rate']:
                consumption_credits = self._simulate_output_consumption(consumer, scenario_params)
                
                for credit_type, amount in consumption_credits.items():
                    daily_credits[credit_type] += amount
                
                daily_activities.append({
                    'type': 'output_consumption',
                    'consumer_id': consumer['id'],
                    'credits_awarded': consumption_credits,
                    'day': day
                })
        
        # Simulate governance activities
        if random.random() < 0.1:  # 10% chance of governance activity
            governance_credits = self._simulate_governance_activity(scenario_params)
            for credit_type, amount in governance_credits.items():
                daily_credits[credit_type] += amount
            
            daily_activities.append({
                'type': 'governance_activity',
                'credits_awarded': governance_credits,
                'day': day
            })
        
        return {
            'day': day,
            'daily_credits': daily_credits,
            'activities': daily_activities,
            'total_daily_credits': sum(daily_credits.values())
        }
    
    def _simulate_task_completion(self, bot: Dict[str, Any], scenario_params: Dict[str, Any]) -> Dict[str, float]:
        """Simulate credits for a completed task"""
        base_credits = {
            CreditType.COMPUTATIONAL.value: 2.0,
            CreditType.CHARITABLE.value: 1.5 if bot['type'] == 'charitable' else 1.0,
            CreditType.EFFICIENCY.value: bot['efficiency'] * 2.0,
            CreditType.TRANSPARENCY.value: 1.0,
            CreditType.COMMUNITY.value: 0.5
        }
        
        # Apply bot multiplier
        multiplier = bot['credit_multiplier']
        
        # Apply scenario scaling
        scenario_multiplier = scenario_params.get('credit_multiplier', 1.0)
        
        return {
            credit_type: amount * multiplier * scenario_multiplier
            for credit_type, amount in base_credits.items()
        }
    
    def _simulate_output_consumption(self, consumer: Dict[str, Any], scenario_params: Dict[str, Any]) -> Dict[str, float]:
        """Simulate credits for output consumption"""
        base_credits = {
            CreditType.CHARITABLE.value: 3.0 * consumer['impact_multiplier'],
            CreditType.COMMUNITY.value: 2.0,
            CreditType.TRANSPARENCY.value: 1.0
        }
        
        scenario_multiplier = scenario_params.get('credit_multiplier', 1.0)
        
        return {
            credit_type: amount * scenario_multiplier
            for credit_type, amount in base_credits.items()
        }
    
    def _simulate_governance_activity(self, scenario_params: Dict[str, Any]) -> Dict[str, float]:
        """Simulate credits for governance activities"""
        activity_types = [
            {'type': 'rule_enforcement', 'credits': {CreditType.TRANSPARENCY.value: 2.0, CreditType.COMMUNITY.value: 1.0}},
            {'type': 'violation_resolution', 'credits': {CreditType.TRANSPARENCY.value: 3.0, CreditType.COMMUNITY.value: 2.0}},
            {'type': 'policy_update', 'credits': {CreditType.TRANSPARENCY.value: 4.0, CreditType.COMMUNITY.value: 3.0}}
        ]
        
        activity = random.choice(activity_types)
        scenario_multiplier = scenario_params.get('credit_multiplier', 1.0)
        
        return {
            credit_type: amount * scenario_multiplier
            for credit_type, amount in activity['credits'].items()
        }
    
    def run_projection(self, scenario_name: str, days: int, scenario_params: Dict[str, Any]) -> CreditProjection:
        """Run credit projection for a given scenario"""
        print(f"Running credit projection: {scenario_name} ({days} days)")
        
        total_credits = {credit_type.value: 0.0 for credit_type in CreditType}
        daily_data = []
        contributor_credits = {}
        
        for day in range(days):
            daily_result = self.simulate_daily_activity(day, scenario_params)
            daily_data.append(daily_result)
            
            # Accumulate total credits
            for credit_type, amount in daily_result['daily_credits'].items():
                total_credits[credit_type] += amount
            
            # Track contributors
            for activity in daily_result['activities']:
                contributor_id = activity.get('bot_id') or activity.get('consumer_id') or 'system'
                
                if contributor_id not in contributor_credits:
                    contributor_credits[contributor_id] = {credit_type.value: 0.0 for credit_type in CreditType}
                
                for credit_type, amount in activity['credits_awarded'].items():
                    contributor_credits[contributor_id][credit_type] += amount
        
        # Calculate daily averages
        credits_per_day = {
            credit_type: total / days
            for credit_type, total in total_credits.items()
        }
        
        # Generate top contributors
        top_contributors = []
        for contributor_id, credits in contributor_credits.items():
            total_contributor_credits = sum(credits.values())
            top_contributors.append({
                'contributor_id': contributor_id,
                'total_credits': total_contributor_credits,
                'credit_breakdown': credits
            })
        
        top_contributors.sort(key=lambda x: x['total_credits'], reverse=True)
        top_contributors = top_contributors[:10]  # Top 10
        
        # Calculate distribution metrics
        distribution_metrics = self._calculate_distribution_metrics(daily_data, total_credits)
        
        # Calculate community health score
        community_health_score = self._calculate_community_health_score(
            total_credits, distribution_metrics, len(contributor_credits)
        )
        
        return CreditProjection(
            scenario_name=scenario_name,
            time_period_days=days,
            total_credits_awarded=total_credits,
            credits_per_day=credits_per_day,
            top_contributors=top_contributors,
            distribution_metrics=distribution_metrics,
            community_health_score=community_health_score
        )
    
    def _calculate_distribution_metrics(self, daily_data: List[Dict], total_credits: Dict[str, float]) -> Dict[str, float]:
        """Calculate credit distribution metrics"""
        # Credit diversity (how evenly distributed across types)
        credit_values = list(total_credits.values())
        total = sum(credit_values)
        
        if total == 0:
            return {'diversity_index': 0.0, 'stability_score': 0.0, 'growth_rate': 0.0}
        
        # Calculate diversity using Simpson's diversity index
        diversity_index = 1 - sum((value / total) ** 2 for value in credit_values)
        
        # Calculate stability (variation in daily totals)
        daily_totals = [day['total_daily_credits'] for day in daily_data]
        if len(daily_totals) > 1:
            avg_daily = sum(daily_totals) / len(daily_totals)
            variance = sum((total - avg_daily) ** 2 for total in daily_totals) / len(daily_totals)
            stability_score = max(0, 1 - (variance ** 0.5) / max(1, avg_daily))
        else:
            stability_score = 1.0
        
        # Calculate growth rate (simple linear trend)
        if len(daily_totals) > 1:
            first_half = daily_totals[:len(daily_totals)//2]
            second_half = daily_totals[len(daily_totals)//2:]
            
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)
            
            growth_rate = (avg_second - avg_first) / max(1, avg_first) if avg_first > 0 else 0
        else:
            growth_rate = 0.0
        
        return {
            'diversity_index': diversity_index,
            'stability_score': stability_score,
            'growth_rate': growth_rate
        }
    
    def _calculate_community_health_score(self, total_credits: Dict[str, float], 
                                        distribution_metrics: Dict[str, float], 
                                        num_contributors: int) -> float:
        """Calculate overall community health score (0-100)"""
        # Components of community health
        
        # 1. Credit volume (scaled to 0-1)
        total_volume = sum(total_credits.values())
        volume_score = min(1.0, total_volume / 1000)  # Normalize to reasonable scale
        
        # 2. Diversity of credit types
        diversity_score = distribution_metrics['diversity_index']
        
        # 3. Stability of daily activity
        stability_score = distribution_metrics['stability_score']
        
        # 4. Contributor participation
        participation_score = min(1.0, num_contributors / 20)  # 20+ contributors = max score
        
        # 5. Balance between different credit types
        charitable_ratio = total_credits.get(CreditType.CHARITABLE.value, 0) / max(1, total_volume)
        balance_score = 1.0 - abs(charitable_ratio - 0.3)  # Target 30% charitable credits
        balance_score = max(0, balance_score)
        
        # Weighted combination
        health_score = (
            volume_score * 0.25 +
            diversity_score * 0.2 +
            stability_score * 0.2 +
            participation_score * 0.2 +
            balance_score * 0.15
        ) * 100
        
        return min(100, max(0, health_score))
    
    def run_multiple_scenarios(self) -> Dict[str, Any]:
        """Run multiple credit projection scenarios"""
        scenarios = [
            {
                'name': 'Conservative Growth',
                'days': 30,
                'params': {
                    'active_bots_per_day': 2,
                    'max_tasks_per_bot': 3,
                    'active_consumers_per_day': 1,
                    'credit_multiplier': 0.8
                }
            },
            {
                'name': 'Moderate Expansion',
                'days': 90,
                'params': {
                    'active_bots_per_day': 4,
                    'max_tasks_per_bot': 5,
                    'active_consumers_per_day': 2,
                    'credit_multiplier': 1.0
                }
            },
            {
                'name': 'Rapid Growth',
                'days': 180,
                'params': {
                    'active_bots_per_day': 6,
                    'max_tasks_per_bot': 8,
                    'active_consumers_per_day': 4,
                    'credit_multiplier': 1.3
                }
            },
            {
                'name': 'Sustained Operation',
                'days': 365,
                'params': {
                    'active_bots_per_day': 5,
                    'max_tasks_per_bot': 6,
                    'active_consumers_per_day': 3,
                    'credit_multiplier': 1.1
                }
            }
        ]
        
        results = {}
        
        for scenario in scenarios:
            projection = self.run_projection(
                scenario['name'],
                scenario['days'],
                scenario['params']
            )
            results[scenario['name']] = asdict(projection)
        
        # Generate comparative analysis
        comparative_analysis = self._generate_comparative_analysis(results)
        
        return {
            'individual_projections': results,
            'comparative_analysis': comparative_analysis,
            'generated_at': time.time()
        }
    
    def _generate_comparative_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparative analysis across scenarios"""
        scenario_summaries = []
        
        for name, result in results.items():
            total_credits = sum(result['total_credits_awarded'].values())
            daily_avg = sum(result['credits_per_day'].values())
            
            scenario_summaries.append({
                'name': name,
                'total_credits': total_credits,
                'daily_average': daily_avg,
                'community_health': result['community_health_score'],
                'diversity_index': result['distribution_metrics']['diversity_index'],
                'stability_score': result['distribution_metrics']['stability_score'],
                'num_contributors': len(result['top_contributors'])
            })
        
        # Find best performers
        best_health = max(scenario_summaries, key=lambda x: x['community_health'])
        most_credits = max(scenario_summaries, key=lambda x: x['total_credits'])
        most_stable = max(scenario_summaries, key=lambda x: x['stability_score'])
        
        return {
            'best_community_health': best_health['name'],
            'highest_total_credits': most_credits['name'],
            'most_stable_scenario': most_stable['name'],
            'average_health_score': sum(s['community_health'] for s in scenario_summaries) / len(scenario_summaries),
            'total_projected_credits': sum(s['total_credits'] for s in scenario_summaries),
            'recommendations': [
                f"For maximum community health, consider parameters similar to '{best_health['name']}'",
                f"For highest credit generation, use '{most_credits['name']}' scenario approach",
                f"For operational stability, follow '{most_stable['name']}' patterns",
                "Balance credit diversity to maintain healthy ecosystem dynamics",
                "Monitor contributor participation to ensure community engagement"
            ]
        }
    
    def save_projections(self, filename: str = None) -> str:
        """Save credit projections to file"""
        if not filename:
            filename = f"/home/runner/work/spraxxx.pantry/spraxxx.pantry/simulations/credit_projections_{int(time.time())}.json"
        
        results = self.run_multiple_scenarios()
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Credit projections saved to {filename}")
        return filename

def main():
    """Run credit projection simulations"""
    print("SPRAXXX Pantry - Symbolic Credit Projections")
    print("=" * 60)
    
    simulator = CreditProjectionSimulator()
    results_file = simulator.save_projections()
    
    print("\nCredit Projection Summary:")
    print(f"Results saved to: {results_file}")
    print("\nKey Insights:")
    print("- Community health improves with balanced participation")
    print("- Credit diversity indicates healthy ecosystem dynamics")
    print("- Stability scores reflect sustainable operation patterns")
    print("- Contributor engagement drives long-term success")
    
    return results_file

if __name__ == "__main__":
    main()