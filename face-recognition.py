import cv2
import os
import numpy as np
from PIL import Image
from tkinter import messagebox

class FaceRecognizerOpenCV:
    def __init__(self, mode='recognize'):
        """
        Initializes the face recognizer.
        - mode: 'recognize', 'gather', or 'train'.
        """
        self.mode = mode
        
        # Path for the Haar Cascade classifier file
        self.cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_detector = cv2.CascadeClassifier(self.cascade_path)

        if self.mode == 'recognize':
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            # Ensure the trainer.yml file exists before trying to read it
            if os.path.exists('trainer/trainer.yml'):
                self.recognizer.read('trainer/trainer.yml')
                self.run_recognition()
            else:
                messagebox.showerror("Error", "Trainer file not found. Please gather data and train the model first.")
                return

        elif self.mode == 'gather':
            self.gather_dataset()

        elif self.mode == 'train':
            self.train_model()

    def gather_dataset(self):
        """Captures and saves face samples for training."""
        face_id = input('\n===> Enter a numeric user ID and look at the camera: ')
        print("\n===> Initializing face capture. Look at the camera and wait...")
        
        # Create dataset directory if it doesn't exist
        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        count = 0
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # Set video width
        cam.set(4, 480)  # Set video height

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", gray[y:y+h, x:x+w])
                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face samples and stop
                break

        print("\n===> Exiting Program and cleaning up.")
        cam.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Dataset created successfully!")

    def train_model(self):
        """Trains the face recognizer and saves the model."""
        path = 'dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        print("\n===> Training faces. It will take a few seconds. Wait...")

        faces, ids = self.get_images_and_labels(path)
        recognizer.train(faces, np.array(ids))

        # Create trainer directory if it doesn't exist
        if not os.path.exists('trainer'):
            os.makedirs('trainer')
            
        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml')

        print(f"\n===> {len(np.unique(ids))} faces trained. Exiting Program.")
        messagebox.showinfo("Result", "Model trained successfully!")

    def get_images_and_labels(self, path):
        """Gets face images and their corresponding labels from the dataset folder."""
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples = []
        ids = []

        for image_path in image_paths:
            PIL_img = Image.open(image_path).convert('L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            
            # Extract the user ID from the filename
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces = self.face_detector.detectMultiScale(img_numpy)
            
            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
                
        return face_samples, ids

    def run_recognition(self):
        """Main loop for recognizing faces from the webcam."""
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)

        # For now, we'll use IDs. You can map these IDs to names from your database.
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

                # Check if confidence is less than 100 ==> "0" is perfect match
                if confidence < 100:
                    # In a real app, you would look up the name for this ID from your database
                    name = f"User: {id}" 
                    confidence_text = f"  {round(100 - confidence)}%"
                else:
                    name = "Unknown"
                    confidence_text = f"  {round(100 - confidence)}%"

                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence_text), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('camera', img)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        print("\n===> Exiting Program.")
        cam.release()
        cv2.destroyAllWindows()

# ================== How to Run ==================
# 1. To gather data for a new user:
#    FaceRecognizerOpenCV(mode='gather')
#
# 2. After gathering data, to train the model:
#    FaceRecognizerOpenCV(mode='train')
#
# 3. To run live recognition (this should be called from your main app):
#    # In your main.py, the button command would call a function that does:
#    # new_window = Toplevel(self.root)
#    # app = FaceRecognizerOpenCV(mode='recognize') 
#    # Note: The Toplevel window is not used here as OpenCV creates its own window.
#    # A better integration would embed the cv2 video feed into a Tkinter canvas.
