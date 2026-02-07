import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
from datetime import datetime
from config import DB_CONFIG, FACE_RECOGNITION_CONFIG, PATHS, UI_CONFIG

class FaceRecognizer:
    def __init__(self, root):
        self.root = root
        ui_settings = UI_CONFIG['face_recognizer']
        self.root.geometry(ui_settings['window_geometry'])
        self.root.title(ui_settings['title'])
        self.root.configure(bg=ui_settings['bg_color'])

        self.is_running = True
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_config = DB_CONFIG

        title_lbl = Label(self.root, text="LIVE FACE RECOGNITION", font=("tahoma", 20, "bold"), bg="#2c3e50", fg="white")
        title_lbl.pack(pady=20)

        self.video_label = Label(self.root)
        self.video_label.pack(pady=10, padx=10)

        # Load the trained model
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        classifier_path = os.path.join(self.script_dir, PATHS['classifier'])
        if not os.path.exists(classifier_path):
             messagebox.showerror("Error", "classifier.xml not found. Please train the model first.", parent=self.root)
             self.is_running = False
             self.root.destroy()
             return
        self.recognizer.read(classifier_path)

        # Load the cascade for face detection
        cascade_path = os.path.join(self.script_dir, PATHS['cascade'])
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam.", parent=self.root)
            self.is_running = False
            self.root.destroy()
            return

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def mark_attendance(self, roll, name, dep):
        """Records attendance in a CSV file, ensuring no duplicates for the same day."""
        attendance_file = os.path.join(self.script_dir, PATHS['attendance'])
        try:
            with open(attendance_file, "r+", newline="\n") as f:
                myDataList = f.readlines()
                nameList = []
                today_str = datetime.now().strftime("%d/%m/%Y")
                for line in myDataList:
                    entry = line.split(',')
                    # Check if the entry has enough parts and the date matches
                    if len(entry) > 4 and entry[4].strip() == today_str:
                         nameList.append(entry[0])

                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime("%H:%M:%S")
                    f.writelines(f"\n{name},{roll},{dep},{dtString},{today_str},Present")
        except FileNotFoundError:
            # If file doesn't exist, create it with headers
            with open(attendance_file, "w", newline="\n") as f:
                f.writelines("Name,Roll,Department,Time,Date,Status")
                # Now add the first entry
                now = datetime.now()
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{name},{roll},{dep},{dtString},{today_str},Present")


    def update_frame(self):
        if not self.is_running: return

        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Corrected line
            faces = self.face_cascade.detectMultiScale(
                gray,
                FACE_RECOGNITION_CONFIG['face_scale_factor'],
                FACE_RECOGNITION_CONFIG['face_min_neighbors']
            )

            # This loop processes every face found in the frame
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

                if confidence < FACE_RECOGNITION_CONFIG['confidence_threshold']:
                    try:
                        conn = mysql.connector.connect(**self.db_config)
                        my_cursor = conn.cursor()
                        my_cursor.execute("SELECT name, dep FROM students WHERE roll=%s", (str(id),))
                        row = my_cursor.fetchone()
                        
                        if row:
                            name, dep = row
                            roll = str(id)
                            cv2.putText(frame, f"Name: {name}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                            self.mark_attendance(roll, name, dep)
                        else:
                            cv2.putText(frame, "Unknown Student", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                        
                        conn.close()
                    except mysql.connector.Error:
                        cv2.putText(frame, f"DB Error", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                else:
                    cv2.putText(frame, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(FACE_RECOGNITION_CONFIG['frame_interval_ms'], self.update_frame)

    def on_close(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()
