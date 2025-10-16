#!/usr/bin/env python
"""
Setup script to create sample events for the D.O.L ministry backend.
Run this script from the backend directory.
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🎉 Setting up sample events for D.O.L Ministry...")
    
    try:
        # Create sample events
        call_command('create_sample_events')
        print("✅ Sample events created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating sample events: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
