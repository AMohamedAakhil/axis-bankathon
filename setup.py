#!/usr/bin/env python3
"""
Setup script for AI HR Assistant Streamlit app
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 AI HR Assistant - Setup Script")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("\n🔧 Creating .env file...")
    
    env_content = """# Google Gemini API Key
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your actual Gemini API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_env_setup():
    """Check if environment is properly configured"""
    print("\n🔍 Checking environment setup...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("❌ GOOGLE_API_KEY not configured in .env file")
            print("Please edit .env file and add your actual Gemini API key")
            return False
        
        print("✅ Environment variables configured")
        return True
        
    except ImportError:
        print("❌ python-dotenv not installed")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing imports...")
    
    import_tests = [
        ("streamlit", "import streamlit"),
        ("google.generativeai", "import google.generativeai as genai"),
        ("PyPDF2", "import PyPDF2"),
        ("pandas", "import pandas"),
        ("dotenv", "from dotenv import load_dotenv")
    ]
    
    failed_imports = []
    
    for package_name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"✅ {package_name}")
        except ImportError as e:
            print(f"❌ {package_name}: {e}")
            failed_imports.append(package_name)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All imports successful")
    return True

def run_demo():
    """Run the demo script to test functionality"""
    print("\n🎯 Running demo to test functionality...")
    
    try:
        subprocess.check_call([sys.executable, "demo_cv_analysis.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Check environment setup
    if not check_env_setup():
        print("\n⚠️  Setup incomplete. Please configure your .env file and run setup again.")
        print("Or run the app manually with: streamlit run streamlit_app.py")
        sys.exit(1)
    
    # Run demo
    if run_demo():
        print("\n🎉 Setup complete! Your AI HR Assistant is ready to use.")
        print("\n🚀 To start the app, run:")
        print("   streamlit run streamlit_app.py")
        print("\n📖 For more information, see README_STREAMLIT.md")
    else:
        print("\n⚠️  Setup completed but demo failed. Please check your API key.")

if __name__ == "__main__":
    main() 