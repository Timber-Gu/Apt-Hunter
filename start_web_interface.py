#!/usr/bin/env python3
"""
Apt-Hunter Web Interface Launcher

This script checks for dependencies and launches the web interface.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'flask', 'selenium', 'beautifulsoup4', 'pandas', 
        'webdriver-manager', 'openai', 'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    return missing_packages

def install_dependencies(packages):
    """Install missing packages."""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade'
        ] + packages)
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_chrome():
    """Check if Chrome is available."""
    try:
        # Try to import webdriver manager to check Chrome
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ Chrome WebDriver support available")
        return True
    except Exception:
        print("⚠️  Chrome WebDriver check failed - will attempt auto-download")
        return True  # Still return True as webdriver-manager handles this

def launch_app():
    """Launch the Flask application."""
    print("\n🚀 Starting Apt-Hunter Web Interface...")
    print("📍 The application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Apt-Hunter Web Interface. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running 'python app.py' directly for more details.")

def main():
    """Main function to check everything and launch the app."""
    print("🏠 Apt-Hunter Web Interface Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📋 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} required packages.")
        response = input("Would you like to install them automatically? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_dependencies(missing):
                sys.exit(1)
        else:
            print("❌ Cannot proceed without required packages.")
            print("💡 Install manually with: pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n🌐 Checking Chrome browser support...")
    check_chrome()
    
    # Check if app.py exists
    if not Path('app.py').exists():
        print("❌ app.py not found in current directory.")
        print("💡 Make sure you're running this from the Apt-Hunter directory.")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    launch_app()

if __name__ == "__main__":
    main() 