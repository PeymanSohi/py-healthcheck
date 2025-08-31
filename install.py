#!/usr/bin/env python3
"""
Installation script for py-healthcheck.

This script helps install the package and its dependencies.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def main():
    """Main installation function."""
    print("=== py-healthcheck Installation Script ===\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install the package in development mode
    if not run_command("pip install -e .", "Installing py-healthcheck in development mode"):
        print("Failed to install py-healthcheck")
        sys.exit(1)
    
    # Install basic dependencies
    if not run_command("pip install click httpx", "Installing basic dependencies"):
        print("Failed to install basic dependencies")
        sys.exit(1)
    
    # Install development dependencies
    if not run_command("pip install pytest pytest-asyncio", "Installing test dependencies"):
        print("Failed to install test dependencies")
        sys.exit(1)
    
    print("\n=== Installation Complete ===")
    print("You can now:")
    print("1. Run tests: pytest")
    print("2. Use the CLI: py-healthcheck --help")
    print("3. Import the package: import py_healthcheck")
    print("\nFor additional features, install optional dependencies:")
    print("- Database support: pip install py-healthcheck[postgres,mysql,redis,mongodb,elasticsearch]")
    print("- Framework support: pip install py-healthcheck[flask,fastapi,django]")
    print("- CLI enhancements: pip install py-healthcheck[cli]")
    print("- All features: pip install py-healthcheck[all]")


if __name__ == "__main__":
    main()
