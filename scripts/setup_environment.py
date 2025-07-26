#!/usr/bin/env python3
"""
Environment setup script for GoChurch development
"""

import subprocess
import sys
import os
import shutil

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔧 {description}")
    print(f"{'='*50}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode == 0:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.11 or higher")
        return False

def check_poetry():
    """Check if Poetry is available"""
    return shutil.which("poetry") is not None

def setup_with_poetry():
    """Setup environment using Poetry"""
    print("🎯 Setting up environment with Poetry...")
    
    if not check_poetry():
        print("❌ Poetry not found. Installing Poetry...")
        if not run_command("curl -sSL https://install.python-poetry.org | python3 -", "Installing Poetry"):
            return False
        
        # Add Poetry to PATH for current session
        home = os.path.expanduser("~")
        poetry_bin = f"{home}/.local/bin"
        if poetry_bin not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{poetry_bin}:{os.environ.get('PATH', '')}"
    
    # Install dependencies
    if not run_command("poetry install", "Installing dependencies with Poetry"):
        return False
    
    print("✅ Poetry setup completed!")
    print("\n🎯 To activate the environment:")
    print("   poetry shell")
    print("\n🎯 To run tests:")
    print("   poetry run python scripts/run_tests.py")
    
    return True

def setup_with_pip():
    """Setup environment using pip and venv"""
    print("🎯 Setting up environment with pip and venv...")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_script = "source venv/bin/activate"
        pip_command = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_command} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Install additional testing dependencies
    additional_deps = ["requests", "pytest-cov", "pytest-xdist"]
    for dep in additional_deps:
        run_command(f"{pip_command} install {dep}", f"Installing {dep}", check=False)
    
    print("✅ pip setup completed!")
    print(f"\n🎯 To activate the environment:")
    print(f"   {activate_script}")
    print("\n🎯 To run tests:")
    print("   python scripts/run_tests.py")
    
    return True

def check_database_config():
    """Check if database configuration exists"""
    if os.path.exists(".env"):
        print("✅ .env file exists")
        return True
    elif os.path.exists(".env.example"):
        print("⚠️  .env file not found, but .env.example exists")
        print("Please copy .env.example to .env and configure your database settings")
        return False
    else:
        print("❌ No .env or .env.example file found")
        return False

def main():
    """Main setup function"""
    print("🚀 GoChurch Environment Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check database configuration
    check_database_config()
    
    # Choose setup method
    print("\n🔧 Choose setup method:")
    print("1. Poetry (Recommended)")
    print("2. pip + venv")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    success = False
    if choice == "1":
        success = setup_with_poetry()
    elif choice == "2":
        success = setup_with_pip()
    else:
        print("❌ Invalid choice. Please run the script again.")
        sys.exit(1)
    
    if success:
        print("\n🎉 Environment setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Configure your .env file with database settings")
        print("2. Start your PostgreSQL database")
        print("3. Run tests: python scripts/run_tests.py")
        print("4. Start the server: ./start.sh")
    else:
        print("\n❌ Environment setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
