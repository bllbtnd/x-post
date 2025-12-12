#!/usr/bin/env python3
"""Run all tests from the project root"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run tests
from tests.test_scrapers import test_all_scrapers

if __name__ == "__main__":
    success = test_all_scrapers()
    sys.exit(0 if success else 1)
