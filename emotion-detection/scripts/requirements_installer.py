import subprocess
import sys
import os

def install_requirements():
    """Install required packages for emotion detection"""
    
    requirements = [
        'opencv-python',
        'fer',
        'tensorflow',
        'numpy',
        'matplotlib',
        'mtcnn',
        'keras',
        'moviepy==1.0.3'
    ]
    
    print("Installing required packages for emotion detection...")
    print("This may take a few minutes...")
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    print("\n✓ All packages installed successfully!")
    print("\nYou can now run the emotion detector with:")
    print("python emotion_detector.py")
    
    return True

if __name__ == "__main__":
    install_requirements()
