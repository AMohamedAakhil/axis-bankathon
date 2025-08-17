#!/usr/bin/env python3
"""
Conda-specific fix script for dependency conflicts in AI HR Assistant
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🔧 Fixing Dependency Conflicts (Conda Environment)")
    print("=" * 60)
    
    # Check if we're in a conda environment
    if 'CONDA_DEFAULT_ENV' not in os.environ:
        print("⚠️  Not in a conda environment. Using pip instead...")
        print("Run: python fix_dependencies.py")
        return False
    
    print(f"📦 Current conda environment: {os.environ.get('CONDA_DEFAULT_ENV', 'base')}")
    
    # Step 1: Remove conflicting packages using conda
    print("\n📦 Step 1: Removing conflicting packages with conda...")
    
    packages_to_remove = [
        "protobuf",
        "google-generativeai",
        "google-ai-generativelanguage",
        "google-api-core",
        "google-api-python-client"
    ]
    
    for package in packages_to_remove:
        run_command(f"conda remove -y {package}", f"Removing {package}")
    
    # Step 2: Install correct protobuf version with conda
    print("\n📦 Step 2: Installing correct protobuf version with conda...")
    if not run_command("conda install -y 'protobuf>=4.25.3,<5.0.0'", "Installing protobuf"):
        print("⚠️  Conda install failed, trying pip...")
        if not run_command("pip install 'protobuf>=4.25.3,<5.0.0'", "Installing protobuf with pip"):
            print("❌ Failed to install protobuf.")
            return False
    
    # Step 3: Install google-generativeai
    print("\n📦 Step 3: Installing Google Generative AI...")
    if not run_command("pip install google-generativeai>=0.8.0", "Installing google-generativeai"):
        print("❌ Failed to install google-generativeai.")
        return False
    
    # Step 4: Install other required packages
    print("\n📦 Step 4: Installing other required packages...")
    packages_to_install = ["PyPDF2", "pandas", "python-dotenv"]
    
    for package in packages_to_install:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package} with pip, trying conda...")
            if not run_command(f"conda install -y {package}", f"Installing {package} with conda"):
                print(f"❌ Failed to install {package} with both pip and conda.")
                return False
    
    # Step 5: Test imports
    print("\n🧪 Step 5: Testing imports...")
    
    import_tests = [
        ("streamlit", "import streamlit"),
        ("google.generativeai", "import google.generativeai as genai"),
        ("PyPDF2", "import PyPDF2"),
        ("pandas", "import pandas"),
        ("dotenv", "from dotenv import load_dotenv")
    ]
    
    all_imports_working = True
    
    for package_name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"✅ {package_name}")
        except ImportError as e:
            print(f"❌ {package_name}: {e}")
            all_imports_working = False
    
    if all_imports_working:
        print("\n🎉 All dependencies are now working correctly!")
        print("\n🚀 You can now run the app with:")
        print("   streamlit run streamlit_app.py")
        
        # Additional conda-specific recommendations
        print("\n💡 Conda Environment Tips:")
        print("   - If you encounter issues, consider creating a fresh environment:")
        print("     conda create -n ai-hr python=3.11")
        print("     conda activate ai-hr")
        print("     python fix_dependencies.py")
        
    else:
        print("\n⚠️  Some dependencies still have issues. Please check the errors above.")
        print("\n💡 Try creating a fresh conda environment:")
        print("   conda create -n ai-hr python=3.11")
        print("   conda activate ai-hr")
        print("   python fix_dependencies.py")
    
    return all_imports_working

if __name__ == "__main__":
    main() 