#!/usr/bin/env python3
"""
Quick start script for the AI HR Assistant Streamlit app
"""

import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'google.generativeai', 'PyPDF2', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('.', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your GOOGLE_API_KEY")
        print("Example:")
        print("GOOGLE_API_KEY=your_gemini_api_key_here")
        return False
    
    # Check if GOOGLE_API_KEY is set
    load_dotenv()
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY not found in .env file")
        print("Please add your Gemini API key to the .env file")
        return False
    
    print("✅ Environment variables are configured")
    return True

def main():
    print("🚀 AI HR Assistant - Quick Start")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    try:
        from dotenv import load_dotenv
        if not check_env_file():
            sys.exit(1)
    except ImportError:
        print("❌ python-dotenv not installed")
        print("Please install it using: pip install python-dotenv")
        sys.exit(1)
    
    print("\n🎯 Starting Streamlit app...")
    print("The app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the app")
    print("=" * 40)
    
    try:
        # Start Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 