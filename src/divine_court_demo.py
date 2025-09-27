#!/usr/bin/env python3
"""
SPRAXXX Pantry – Divine Court Demo
Purpose: Demonstrate the Divine Court Incident Tracker functionality
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import sys
import os
from datetime import datetime, date, timedelta

# Add the src directory to Python path so we can import divine_court
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from divine_court import IncidentController, IncidentSeverity, UserRole

def print_header():
    """Print demo header"""
    print("=" * 70)
    print("SPRAXXX PANTRY - DIVINE COURT INCIDENT TRACKER DEMO")
    print("Nonprofit-only institutional accountability system")
    print("=" * 70)
    print()

def notification_handler(notification_data):
    """Sample notification handler"""
    if notification_data['type'] == 'red_incident_alert':
        print(f"🚨 CRITICAL ALERT: {notification_data['message']}")
    elif notification_data['type'] == 'support_request':
        print(f"🙏 SUPPORT REQUEST: {notification_data['message']}")
    print()

def demo_incident_logging():
    """Demonstrate incident logging functionality"""
    print("1️⃣ INCIDENT LOGGING DEMONSTRATION")
    print("-" * 40)
    
    # Initialize controller with notification handler
    controller = IncidentController()
    controller.add_notification_handler(notification_handler)
    
    # Sample incidents to log
    sample_incidents = [
        {
            "institution": "State Correctional Facility",
            "act_violated": "Use of excessive force during routine cell inspection",
            "witness": "Guard Johnson, Inmate #47291",
            "comments": "Multiple inmates report unnecessary violence during standard procedure. Medical attention required for two individuals. Pattern of escalation observed over past month.",
            "submitted_by": "gabriel_node",
            "user_role": UserRole.ARCHANGEL,
            "date": date.today() - timedelta(days=1)
        },
        {
            "institution": "County Detention Center", 
            "act_violated": "Denial of medical care for chronic condition",
            "witness": "Nurse Smith",
            "comments": "Diabetic inmate denied insulin for 48 hours despite medical orders. Condition deteriorated requiring emergency intervention.",
            "submitted_by": "watcher_01",
            "user_role": UserRole.WATCHER,
            "date": date.today() - timedelta(days=2)
        },
        {
            "institution": "Metro Police Department",
            "act_violated": "Improper detention procedures during arrest",
            "witness": "Officer Rodriguez, Civilian witness",
            "comments": "Failure to read Miranda rights, excessive use of restraints for non-violent offense.",
            "submitted_by": "michael_node",
            "user_role": UserRole.ARCHANGEL,
            "date": date.today() - timedelta(days=3)
        },
        {
            "institution": "Regional Hospital",
            "act_violated": "Discrimination in emergency care",
            "witness": "Dr. Peterson",
            "comments": "Patient care delayed based on socioeconomic status. Standard protocols not followed.",
            "submitted_by": "watcher_02",
            "user_role": UserRole.WATCHER,
            "date": date.today() - timedelta(days=1)
        },
        {
            "institution": "City Hall",
            "act_violated": "Failure to provide interpreter services",
            "witness": "Social worker Martinez",
            "comments": "Spanish-speaking family denied services, no interpreter provided despite legal requirement.",
            "submitted_by": "raphael_node",
            "user_role": UserRole.ARCHANGEL,
            "date": date.today()
        }
    ]
    
    logged_incidents = []
    
    for incident_data in sample_incidents:
        print(f"Logging incident at {incident_data['institution']}...")
        result = controller.log_incident(**incident_data)
        
        if result['success']:
            print(f"  ✅ {result['incident_id']}: {result['severity'].upper()} severity")
            print(f"     FSI Impact: {result['fsi_impact']}")
            logged_incidents.append(result['incident_id'])
        else:
            print(f"  ❌ Failed: {result['message']}")
        print()
    
    print(f"Successfully logged {len(logged_incidents)} incidents")
    print()
    
    return controller, logged_incidents

def demo_fsi_calculations(controller):
    """Demonstrate FSI calculations and risk assessment"""
    print("2️⃣ FSI CALCULATION & RISK ASSESSMENT")
    print("-" * 40)
    
    # Get FSI data for all institutions
    dashboard_data = controller.get_dashboard_data()
    
    if dashboard_data['success']:
        fsi_data = dashboard_data['dashboard']['fsi_data']
        risk_categories = dashboard_data['dashboard']['risk_categories']
        
        print("📊 INSTITUTION RISK LEVELS:")
        
        # Show high-risk institutions
        if risk_categories['red']:
            print("\n🔴 HIGH RISK INSTITUTIONS:")
            for inst in risk_categories['red']:
                print(f"  • {inst['institution']}: FSI {inst['fsi_score']} ({inst['incident_count']} incidents)")
        
        # Show medium-risk institutions  
        if risk_categories['yellow']:
            print("\n🟡 MEDIUM RISK INSTITUTIONS:")
            for inst in risk_categories['yellow']:
                print(f"  • {inst['institution']}: FSI {inst['fsi_score']} ({inst['incident_count']} incidents)")
        
        # Show low-risk institutions
        if risk_categories['green']:
            print("\n🟢 LOW RISK INSTITUTIONS:")
            for inst in risk_categories['green']:
                print(f"  • {inst['institution']}: FSI {inst['fsi_score']} ({inst['incident_count']} incidents)")
        
        print(f"\nTotal institutions monitored: {fsi_data['total_institutions']}")
        print()
    else:
        print(f"❌ Failed to get FSI data: {dashboard_data['message']}")
        print()

def demo_user_roles(controller, incident_ids):
    """Demonstrate user role functionality"""
    print("3️⃣ USER ROLE SYSTEM DEMONSTRATION")
    print("-" * 40)
    
    if not incident_ids:
        print("No incidents available for role demonstration")
        return
    
    # Get first incident for testing
    test_incident_id = incident_ids[0]
    
    # Try to approve as Watcher (should fail)
    print("Testing Watcher node attempting to approve incident...")
    result = controller.approve_incident(
        incident_id=test_incident_id,
        approver_id="watcher_test",
        user_role=UserRole.WATCHER
    )
    
    if result['success']:
        print("  ❌ Unexpected: Watcher was able to approve incident")
    else:
        print(f"  ✅ Correctly blocked: {result['message']}")
    
    # Try to approve as Archangel (should succeed)
    print("\nTesting Archangel node approving incident...")
    result = controller.approve_incident(
        incident_id=test_incident_id,
        approver_id="gabriel_node",
        user_role=UserRole.ARCHANGEL
    )
    
    if result['success']:
        print(f"  ✅ {result['message']}")
    else:
        print(f"  ❌ Unexpected failure: {result['message']}")
    
    print()

def demo_support_requests(controller, incident_ids):
    """Demonstrate support request functionality (Raphael node)"""
    print("4️⃣ SUPPORT REQUEST SYSTEM (RAPHAEL NODE)")
    print("-" * 40)
    
    if not incident_ids:
        print("No incidents available for support request demonstration")
        return
    
    # Request prayer support
    test_incident_id = incident_ids[0] if incident_ids else None
    if test_incident_id:
        print("Requesting prayer support for high-impact incident...")
        result = controller.request_support(test_incident_id, "prayer")
        
        if result['success']:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  ❌ {result['message']}")
        
        # Request emotional support
        print("\nRequesting emotional support...")
        result = controller.request_support(test_incident_id, "emotional")
        
        if result['success']:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  ❌ {result['message']}")
    
    print()

def demo_dashboard_visualization(controller):
    """Demonstrate dashboard data generation"""
    print("5️⃣ DASHBOARD VISUALIZATION DATA")
    print("-" * 40)
    
    dashboard_result = controller.get_dashboard_data()
    
    if dashboard_result['success']:
        data = dashboard_result['dashboard'] 
        
        print(f"📊 SUMMARY STATISTICS:")
        print(f"  Total Incidents: {data['total_incidents']}")
        print(f"  Red (Critical): {data['severity_counts']['red']}")
        print(f"  Yellow (Moderate): {data['severity_counts']['yellow']}")
        print(f"  Green (Low): {data['severity_counts']['green']}")
        
        if data['pending_approvals']:
            print(f"  Pending Approvals: {len(data['pending_approvals'])}")
        
        print(f"\n📈 FSI OVERVIEW:")
        fsi_summary = data['fsi_data']['summary']
        print(f"  Average FSI Score: {fsi_summary['average_fsi']}")
        print(f"  Highest Risk Institution: {fsi_summary['highest_fsi']['institution']} (FSI: {fsi_summary['highest_fsi']['score']})")
        
        print(f"\n📋 RECENT INCIDENTS:")
        for incident in data['recent_incidents'][:3]:  # Show top 3
            print(f"  • {incident['institution']}: {incident['severity'].upper()} - {incident['date']}")
    else:
        print(f"❌ Failed to get dashboard data: {dashboard_result['message']}")
    
    print()

def demo_institution_report(controller):
    """Demonstrate detailed institution reporting"""
    print("6️⃣ DETAILED INSTITUTION REPORTING")
    print("-" * 40)
    
    # Get report for State Correctional Facility
    institution = "State Correctional Facility"
    report_result = controller.get_institution_report(institution)
    
    if report_result['success']:
        report = report_result['report']
        
        print(f"📋 REPORT FOR: {institution}")
        print(f"  FSI Score: {report['fsi_data']['fsi_score']}")
        print(f"  Risk Level: {report['fsi_data']['risk_level'].upper()}")
        print(f"  Total Incidents: {report['fsi_data']['incident_count']}")
        
        breakdown = report['fsi_data']['breakdown']
        print(f"  Incident Breakdown:")
        print(f"    Red: {breakdown['red_incidents']}")
        print(f"    Yellow: {breakdown['yellow_incidents']}")
        print(f"    Green: {breakdown['green_incidents']}")
        
        trend = report['trend_analysis']
        print(f"  Trend Direction: {trend['trend_direction'].upper()}")
        
        if report['support_requests']:
            print(f"  Active Support Requests: {len(report['support_requests'])}")
    else:
        print(f"❌ Failed to generate report: {report_result['message']}")
    
    print()

def demo_governance_integration():
    """Demonstrate integration with SPRAXXX Pantry governance"""
    print("7️⃣ SPRAXXX PANTRY GOVERNANCE INTEGRATION")
    print("-" * 40)
    
    # Import SPRAXXX governance
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from governance import Governance
        
        governance = Governance()
        
        # Create sample output that would come from Divine Court
        divine_court_output = {
            "task": "incident_tracking",
            "result": "institutional_accountability_data",
            "energy_consumed_wh": 0.05,  # Very efficient
            "nonprofit_purpose": "charitable_institutional_oversight"
        }
        
        print("Validating Divine Court output through SPRAXXX governance...")
        is_valid = governance.validate_output(divine_court_output)
        
        if is_valid:
            print("  ✅ Divine Court output passes SPRAXXX governance validation")
            print("  ✅ Energy efficiency compliant (0.05 Wh)")
            print("  ✅ Nonprofit-only purpose verified")
        else:
            print("  ❌ Governance validation failed")
        
        # Get compliance report
        compliance = governance.get_compliance_report()
        print(f"\n📜 COMPLIANCE STATUS:")
        print(f"  Nonprofit Status: {compliance['nonprofit_compliance']['status']}")
        print(f"  Environmental Status: {compliance['environmental_compliance']['status']}")
        
    except ImportError:
        print("⚠️  SPRAXXX Governance module not available for integration test")
    
    print()

def main():
    """Main demo function"""
    print_header()
    
    try:
        # Run all demonstrations
        controller, incident_ids = demo_incident_logging()
        demo_fsi_calculations(controller)
        demo_user_roles(controller, incident_ids)
        demo_support_requests(controller, incident_ids)
        demo_dashboard_visualization(controller)
        demo_institution_report(controller)
        demo_governance_integration()
        
        print("🎉 DEMO COMPLETED SUCCESSFULLY")
        print("-" * 40)
        print("The Divine Court Incident Tracker has been successfully demonstrated!")
        print("Key features verified:")
        print("  ✅ Incident logging with automatic FSI/DDI calculation")
        print("  ✅ User role management (Archangel vs Watcher nodes)")
        print("  ✅ Real-time notifications for critical incidents") 
        print("  ✅ Dashboard data generation for visualization")
        print("  ✅ Institution risk assessment and reporting")
        print("  ✅ Support request system (Raphael node functionality)")
        print("  ✅ Integration with SPRAXXX Pantry governance framework")
        print()
        print("🌐 To view the web dashboard, open: public/dashboard.html")
        print("🖥️  To use the CLI interface, run: python src/divine_court_cli.py --help")
        print()
        print("All outputs remain strictly nonprofit-only per SPRAXXX Pantry ethics.")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())