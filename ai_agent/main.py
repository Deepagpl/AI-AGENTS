import os
import subprocess
from pathlib import Path

def setup_environment():
    """Ensure all required packages are installed"""
    requirements_file = Path(__file__).parent.parent / 'requirements.txt'
    if requirements_file.exists():
        subprocess.check_call(['pip', 'install', '-r', str(requirements_file)])

def main():
    """Main entry point for the AI Agent Chatbot"""
    # Ensure dependencies are installed
    setup_environment()
    
    # Start the Streamlit app
    streamlit_file = Path(__file__).parent / 'src' / 'frontend' / 'app.py'
    print("Starting AI Agent Chatbot...")
    print("You can access the chat interface in your browser once it starts.")
    subprocess.run(['streamlit', 'run', str(streamlit_file)])

if __name__ == "__main__":
    main()
