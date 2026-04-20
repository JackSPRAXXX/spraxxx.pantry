#!/usr/bin/env python3
"""
SPRAXXX Pantry – Divine Court CLI Interface
Purpose: Command-line interface for Divine Court incident tracking
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import argparse
import sys
import json
from datetime import datetime, date
from divine_court import IncidentController, IncidentSeverity, UserRole

def print_header():
    """Print SPRAXXX Pantry Divine Court header"""
    print("=" * 60)
    print("SPRAXXX PANTRY - DIVINE COURT INCIDENT TRACKER")
    print("Nonprofit-only tool for institutional accountability")
    print("=" * 60)
    print()

def print_incident_summary(incident_data):
    """Print formatted incident summary"""
    print(f"Incident ID: {incident_data['id']}")
    print(f"Institution: {incident_data['institution']}")
    print(f"Severity: {incident_data['severity'].upper()}")
    print(f"FSI Impact: {incident_data['fsi_impact']}")
    print(f"Date: {incident_data['date']}")
    print(f"Submitted by: {incident_data['submitted_by']} ({incident_data['user_role']})")
    print(f"Approved: {'Yes' if incident_data['approved'] else 'No'}")
    if incident_data.get('prayer_support_requested'):
        print("🙏 Prayer support requested")
    if incident_data.get('emotional_support_requested'):
        print("💚 Emotional support requested")
    print("-" * 40)

def print_fsi_summary(fsi_data):
    """Print formatted FSI summary"""
    print(f"Institution: {fsi_data['institution']}")
    print(f"FSI Score: {fsi_data['fsi_score']}")
    print(f"Risk Level: {fsi_data['risk_level'].upper()}")
    print(f"Total Incidents: {fsi_data['incident_count']}")
    
    breakdown = fsi_data['breakdown']
    print(f"  Red Incidents: {breakdown['red_incidents']}")
    print(f"  Yellow Incidents: {breakdown['yellow_incidents']}")
    print(f"  Green Incidents: {breakdown['green_incidents']}")
    print("-" * 40)

def log_incident(args):
    """Log a new incident"""
    controller = IncidentController()
    
    # Parse user role
    try:
        user_role = UserRole(args.user_role.lower())
    except ValueError:
        print(f"Error: Invalid user role '{args.user_role}'. Use 'archangel' or 'watcher'")
        return False
    
    # Parse date if provided
    incident_date = None
    if args.date:
        try:
            incident_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD")
            return False
    
    # Log the incident
    result = controller.log_incident(
        institution=args.institution,
        act_violated=args.violation,
        witness=args.witness or "",
        comments=args.comments or "",
        submitted_by=args.submitted_by,
        user_role=user_role,
        date=incident_date
    )
    
    if result['success']:
        print("✅ Incident logged successfully!")
        print(f"Incident ID: {result['incident_id']}")
        print(f"Severity: {result['severity'].upper()}")
        print(f"FSI Impact: {result['fsi_impact']}")
        
        if result['severity'] == 'red':
            print("🚨 RED ALERT: Critical incident notification sent!")
        
        return True
    else:
        print(f"❌ Failed to log incident: {result['message']}")
        return False

def list_incidents(args):
    """List incidents with optional filtering"""
    controller = IncidentController()
    
    # Parse severity filter
    severity_filter = None
    if args.severity:
        try:
            severity_filter = IncidentSeverity(args.severity.lower())
        except ValueError:
            print(f"Error: Invalid severity '{args.severity}'. Use 'red', 'yellow', or 'green'")
            return False
    
    # Get incidents
    incidents = controller.get_incidents(
        institution=args.institution,
        severity=severity_filter,
        approved_only=not args.include_pending,
        limit=args.limit
    )
    
    if not incidents:
        print("No incidents found matching the criteria.")
        return True
    
    print(f"Found {len(incidents)} incident(s):")
    print()
    
    for incident in incidents:
        print_incident_summary(incident)
    
    return True

def show_dashboard(args):
    """Show dashboard summary"""
    controller = IncidentController()
    
    result = controller.get_dashboard_data()
    
    if not result['success']:
        print(f"❌ Failed to load dashboard: {result['message']}")
        return False
    
    dashboard = result['dashboard']
    
    print("📊 DIVINE COURT DASHBOARD")
    print("=" * 40)
    
    # Severity counts
    severity = dashboard['severity_counts']
    print(f"Total Incidents: {dashboard['total_incidents']}")
    print(f"  🔴 Red: {severity['red']}")
    print(f"  🟡 Yellow: {severity['yellow']}")
    print(f"  🟢 Green: {severity['green']}")
    print()
    
    # Pending approvals
    pending = len(dashboard['pending_approvals'])
    if pending > 0:
        print(f"⏳ Pending Approvals: {pending}")
        print()
    
    # Risk categories
    risk_cats = dashboard['risk_categories']
    print("🎯 INSTITUTION RISK LEVELS:")
    print(f"  🔴 High Risk: {len(risk_cats['red'])} institutions")
    print(f"  🟡 Medium Risk: {len(risk_cats['yellow'])} institutions")
    print(f"  🟢 Low Risk: {len(risk_cats['green'])} institutions")
    print()
    
    # Show top risk institutions
    if risk_cats['red']:
        print("🚨 HIGH RISK INSTITUTIONS:")
        for inst in risk_cats['red'][:5]:  # Top 5
            print(f"  • {inst['institution']}: FSI {inst['fsi_score']} ({inst['incident_count']} incidents)")
        print()
    
    # Recent incidents
    if dashboard['recent_incidents']:
        print("📋 RECENT INCIDENTS:")
        for incident in dashboard['recent_incidents'][:3]:  # Last 3
            print(f"  • {incident['institution']}: {incident['severity'].upper()} - {incident['date']}")
        print()
    
    print(f"Last updated: {dashboard['last_updated']}")
    return True

def show_institution_report(args):
    """Show detailed report for an institution"""
    controller = IncidentController()
    
    result = controller.get_institution_report(args.institution)
    
    if not result['success']:
        print(f"❌ Failed to generate report: {result['message']}")
        return False
    
    report = result['report']
    
    print(f"📋 INSTITUTION REPORT: {args.institution}")
    print("=" * 50)
    
    # FSI Data
    print("📊 FSI ANALYSIS:")
    print_fsi_summary(report['fsi_data'])
    print()
    
    # Trend Analysis
    trend = report['trend_analysis']
    print(f"📈 TREND ANALYSIS ({trend['analysis_period']}):")
    print(f"Current FSI: {trend['current_fsi']}")
    print(f"Trend Direction: {trend['trend_direction'].upper()}")
    print()
    
    # Recent incidents
    incidents = report['incidents']
    if incidents:
        print(f"📋 INCIDENTS ({len(incidents)} total):")
        for incident in incidents[:5]:  # Show last 5
            print(f"  • {incident['date']}: {incident['severity'].upper()} - {incident['act_violated'][:50]}...")
        if len(incidents) > 5:
            print(f"  ... and {len(incidents) - 5} more incidents")
        print()
    
    # Support requests
    support_reqs = report['support_requests']
    if support_reqs:
        print(f"🙏 SUPPORT REQUESTS ({len(support_reqs)} active):")
        for req in support_reqs:
            types = []
            if req.get('prayer_support_requested'):
                types.append('Prayer')
            if req.get('emotional_support_requested'):
                types.append('Emotional')
            print(f"  • {req['date']}: {', '.join(types)} support")
        print()
    
    return True

def approve_incident(args):
    """Approve an incident (Archangel only)"""
    controller = IncidentController()
    
    # Parse user role
    try:
        user_role = UserRole(args.user_role.lower())
    except ValueError:
        print(f"Error: Invalid user role '{args.user_role}'. Use 'archangel' or 'watcher'")
        return False
    
    result = controller.approve_incident(
        incident_id=args.incident_id,
        approver_id=args.approver_id,
        user_role=user_role
    )
    
    if result['success']:
        print(f"✅ {result['message']}")
        return True
    else:
        print(f"❌ {result['message']}")
        return False

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="SPRAXXX Pantry Divine Court Incident Tracker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s log --institution "State Prison" --violation "Policy violation" --submitted-by "watcher_01" --user-role watcher
  %(prog)s list --institution "State Prison" --severity red
  %(prog)s dashboard
  %(prog)s report --institution "State Prison"
  %(prog)s approve --incident-id DC_INCIDENT_20241201_143022 --approver-id michael --user-role archangel
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Log incident command
    log_parser = subparsers.add_parser('log', help='Log a new incident')
    log_parser.add_argument('--institution', required=True, help='Institution name')
    log_parser.add_argument('--violation', required=True, help='Act or policy violated')
    log_parser.add_argument('--submitted-by', required=True, help='Username of submitter')
    log_parser.add_argument('--user-role', required=True, choices=['archangel', 'watcher'], 
                           help='Role of submitter')
    log_parser.add_argument('--witness', help='Witness information')
    log_parser.add_argument('--comments', help='Additional comments')
    log_parser.add_argument('--date', help='Incident date (YYYY-MM-DD)')
    
    # List incidents command
    list_parser = subparsers.add_parser('list', help='List incidents')
    list_parser.add_argument('--institution', help='Filter by institution')
    list_parser.add_argument('--severity', choices=['red', 'yellow', 'green'], 
                            help='Filter by severity')
    list_parser.add_argument('--include-pending', action='store_true', 
                            help='Include pending (unapproved) incidents')
    list_parser.add_argument('--limit', type=int, default=20, help='Maximum incidents to show')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Show dashboard summary')
    
    # Institution report command
    report_parser = subparsers.add_parser('report', help='Show institution report')
    report_parser.add_argument('--institution', required=True, help='Institution name')
    
    # Approve incident command
    approve_parser = subparsers.add_parser('approve', help='Approve an incident')
    approve_parser.add_argument('--incident-id', required=True, help='Incident ID to approve')
    approve_parser.add_argument('--approver-id', required=True, help='Username of approver')
    approve_parser.add_argument('--user-role', required=True, choices=['archangel', 'watcher'],
                               help='Role of approver (must be archangel)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    print_header()
    
    # Route to appropriate command handler
    success = False
    if args.command == 'log':
        success = log_incident(args)
    elif args.command == 'list':
        success = list_incidents(args)
    elif args.command == 'dashboard':
        success = show_dashboard(args)
    elif args.command == 'report':
        success = show_institution_report(args)
    elif args.command == 'approve':
        success = approve_incident(args)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())