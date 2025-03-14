import cv2, imutils, socket
import numpy as np
import os

def cameraOn(self):
    # Load Haar Cascade before the loop
    face_data = cv2.CascadeClassifier('/home/erick/projects/learnerApp/admin/haarcascade_frontalface_default.xml')
    
    # Open webcam
    webcam = cv2.VideoCapture(0)
    
    # Validate registration and get pic name
    self.validateReg()
    self.pic_name = self.regNO
    
    # Define rectangle color (B, G, R)
    color = (128, 128, 128)
    
    # Ensure save directory exists
    save_dir = '../imgs/student_profiles/'
    os.makedirs(save_dir, exist_ok=True)

    while True:
        success, frame = webcam.read()
        if not success:
            print("Failed to capture frame")
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_data.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        # Show video feed
        cv2.imshow('Video', frame)

        # Capture key press
        k = cv2.waitKey(1) & 0xFF
        
        # Save image when 's' is pressed
        if k == ord('s'):
            img_path = os.path.join(save_dir, self.pic_name + '.jpg')
            cv2.imwrite(img_path, frame)
            print(f"Image saved to {img_path}")

        # Exit when 'q' is pressed
        elif k == ord('q'):
            break

    # Release camera and close windows
    webcam.release()
    cv2.destroyAllWindows()
cameraOn()