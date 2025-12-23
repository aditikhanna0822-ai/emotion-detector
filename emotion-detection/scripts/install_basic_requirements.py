import subprocess
import sys

def install_basic_requirements():
    """Install only the essential packages needed"""
    
    requirements = [
        'opencv-python',
        'numpy'
    ]
    
    print("Installing basic requirements for emotion detection...")
    print("This should only take a minute...")
    
    for package in requirements:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            print("Try running: pip install opencv-python numpy")
            return False
    
    print("\n✓ Basic requirements installed successfully!")
    print("\nYou can now run the simple emotion detector with:")
    print("python simple_emotion_detector.py")
    
    # Test OpenCV installation
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV import failed")
        return False
    
    return True

if __name__ == "__main__":
    install_basic_requirements()
