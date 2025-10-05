#!/usr/bin/env python3
"""
Verification script to check if the LLM Maps Assistant is properly configured.
Run this before starting the application to verify all requirements are met.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10 or higher"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.10+")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔍 Checking .env file...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Create it from .env.example: cp .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check if API key is set
    with open(env_path) as f:
        content = f.read()
        if "YOUR_RESTRICTED_SERVER_KEY" in content:
            print("⚠️  API key not configured (still has placeholder)")
            print("   Edit .env and set your Google Maps API key")
            return False
        elif "GOOGLE_MAPS_API_KEY=" in content:
            # Extract key (basic check)
            for line in content.split('\n'):
                if line.startswith('GOOGLE_MAPS_API_KEY='):
                    key = line.split('=', 1)[1].strip()
                    if len(key) > 10:
                        print(f"✅ API key configured ({len(key)} characters)")
                        return True
                    else:
                        print("⚠️  API key seems too short")
                        return False
    
    print("❌ GOOGLE_MAPS_API_KEY not found in .env")
    return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    required = [
        'fastapi',
        'uvicorn',
        'httpx',
        'pydantic',
        'slowapi',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages: pip install -r requirements.txt")
        return False
    
    return True

def check_backend_structure():
    """Check if backend files exist"""
    print("\n🔍 Checking backend structure...")
    required_files = [
        'backend/app/__init__.py',
        'backend/app/main.py',
        'backend/app/config.py',
        'backend/app/routes.py',
        'backend/app/schemas.py',
        'backend/app/google_maps.py',
        'backend/app/rate_limit.py',
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - missing")
            all_exist = False
    
    return all_exist

def check_frontend():
    """Check if frontend exists"""
    print("\n🔍 Checking frontend...")
    frontend_path = Path("frontend/public/index.html")
    
    if frontend_path.exists():
        print(f"✅ {frontend_path}")
        return True
    else:
        print(f"❌ {frontend_path} - missing")
        return False

def check_documentation():
    """Check if documentation exists"""
    print("\n🔍 Checking documentation...")
    docs = ['README.md', 'TESTING.md', 'ASSUMPTIONS.md']
    
    all_exist = True
    for doc in docs:
        path = Path(doc)
        if path.exists():
            print(f"✅ {doc}")
        else:
            print(f"❌ {doc} - missing")
            all_exist = False
    
    return all_exist

def check_port_available():
    """Check if port 8000 is available"""
    print("\n🔍 Checking if port 8000 is available...")
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', 8000))
        sock.close()
        print("✅ Port 8000 is available")
        return True
    except OSError:
        print("⚠️  Port 8000 is already in use")
        print("   Stop the service using port 8000 or use a different port")
        return False

def print_next_steps(all_checks_passed):
    """Print next steps based on verification results"""
    print("\n" + "="*60)
    
    if all_checks_passed:
        print("🎉 All checks passed! You're ready to start.")
        print("\n📋 Next steps:")
        print("1. Start the backend:")
        print("   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n2. Open the frontend:")
        print("   Open frontend/public/index.html in your browser")
        print("\n3. (Optional) Set up Open WebUI:")
        print("   See README.md for Open WebUI integration instructions")
        print("\n4. Test the API:")
        print("   Visit http://localhost:8000/docs for interactive API docs")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n📋 Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp .env.example .env")
        print("3. Set API key in .env file")
        print("4. Ensure all files are present")
    
    print("="*60)

def main():
    """Run all verification checks"""
    print("="*60)
    print("🗺️  LLM Maps Assistant - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python version", check_python_version),
        (".env configuration", check_env_file),
        ("Python dependencies", check_dependencies),
        ("Backend structure", check_backend_structure),
        ("Frontend", check_frontend),
        ("Documentation", check_documentation),
        ("Port availability", check_port_available),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    all_passed = all(results)
    print_next_steps(all_passed)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
