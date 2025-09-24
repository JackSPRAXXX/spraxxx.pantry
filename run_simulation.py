#!/usr/bin/env python3
"""
SPRAXXX Pantry – Simulation Runner
Purpose: Execute the main simulation from repository root
Ethical: Nonprofit-only, outputs cannot be monetized
Branding: Always use SPRAXXX (S-P-R-A-X-X-X)
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main simulation
import main

print("\n=== SPRAXXX Pantry Simulation Runner ===")
print("Simulation executed successfully from repository root!")