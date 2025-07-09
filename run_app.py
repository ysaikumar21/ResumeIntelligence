#!/usr/bin/env python3
"""
Launch script for ATS Resume Analyzer
Built for Saikumar Yaramala - B.Tech Electronics and Data Science
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit ATS Resume Analyzer application"""
    
    print("🎯 Starting ATS Resume Analyzer...")
    print("📊 Built for Data Science Portfolio by Saikumar Yaramala")
    print("🚀 Technologies: Python, Streamlit, SQLite, HTML/CSS")
    print("-" * 60)
    
    try:
        # Change to the directory containing the app
        app_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(app_dir)
        
        # Launch Streamlit app
        cmd = [
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        
        print("🌐 Starting application on http://localhost:8501")
        print("📱 The app will open in your default browser")
        print("⌨️  Press Ctrl+C to stop the application")
        print("-" * 60)
        
        # Run the application
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()