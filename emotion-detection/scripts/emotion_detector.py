import cv2
import numpy as np
from fer import FER
from datetime import datetime

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detector with FER model and face cascade"""
        print("Initializing Emotion Detector...")
        
        # Initialize FER (Facial Emotion Recognition) detector
        self.emotion_detector = FER(mtcnn=True)
        
        # Initialize OpenCV face cascade for backup face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Emotion labels and colors for visualization
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.emotion_colors = {
            'angry': (0, 0, 255),      # Red
            'disgust': (0, 128, 0),    # Dark Green
            'fear': (128, 0, 128),     # Purple
            'happy': (0, 255, 0),      # Green
            'sad': (255, 0, 0),        # Blue
            'surprise': (0, 255, 255), # Yellow
            'neutral': (128, 128, 128) # Gray
        }

        # Store last detection results for consistent display
        self.last_detections = []
        
        print("Emotion Detector initialized successfully!")
    

    
    def detect_emotions_realtime(self):
        """Real-time emotion detection using webcam"""
        print("Starting real-time emotion detection...")
        print("Press 'q' to quit, 's' to save screenshot")
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            # Process every 5th frame for better performance
            if frame_count % 5 == 0:
                # Convert BGR to RGB for FER
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect emotions
                self.last_detections = self.emotion_detector.detect_emotions(rgb_frame)

            # Always draw the last detection results on the frame
            frame = self.draw_emotions(frame, self.last_detections)

            # Display the frame
            cv2.imshow('Emotion Detection', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"emotion_screenshot_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved as {filename}")
            
            frame_count += 1
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("Real-time detection stopped")
    
    def draw_emotions(self, image, detections):
        """Draw emotion labels and bounding boxes on image"""
        for detection in detections:
            # Get bounding box coordinates
            x, y, w, h = detection['box']
            
            # Get dominant emotion
            emotions = detection['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            confidence = emotions[dominant_emotion]
            
            # Get color for the emotion
            color = self.emotion_colors.get(dominant_emotion, (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            
            # Draw emotion label
            label = f"{dominant_emotion}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # Draw label background
            cv2.rectangle(image, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), color, -1)
            
            # Draw label text
            cv2.putText(image, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw emotion probabilities
            y_offset = y + h + 20
            for emotion, prob in emotions.items():
                if prob > 0.1:  # Only show emotions with >10% probability
                    emotion_text = f"{emotion}: {prob:.2f}"
                    cv2.putText(image, emotion_text, (x, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                    y_offset += 15
        
        return image
    


def main():
    """Main function to demonstrate real-time emotion detection"""
    detector = EmotionDetector()

    print("\n=== Real-Time Human Emotion Detection System ===")
    detector.detect_emotions_realtime()

if __name__ == "__main__":
    main()
