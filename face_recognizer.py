import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
from datetime import datetime

class FaceRecognizer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x650+300+80")
        self.root.title("Face Recognition")
        self.root.configure(bg="#2c3e50")

        self.is_running = True
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # --- Database Connection Details ---
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "root" # CHANGE THIS TO YOUR MYSQL PASSWORD
        self.db_name = "student_management"

        title_lbl = Label(self.root, text="LIVE FACE RECOGNITION", font=("tahoma", 20, "bold"), bg="#2c3e50", fg="white")
        title_lbl.pack(pady=20)

        self.video_label = Label(self.root)
        self.video_label.pack(pady=10, padx=10)

        # Load the trained model
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        classifier_path = os.path.join(self.script_dir, "classifier.xml")
        if not os.path.exists(classifier_path):
             messagebox.showerror("Error", "classifier.xml not found. Please train the model first.", parent=self.root)
             self.is_running = False
             self.root.destroy()
             return
        self.recognizer.read(classifier_path)

        # Load the cascade for face detection
        cascade_path = os.path.join(self.script_dir, 'haarcascade_frontalface_default.xml')
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
        attendance_file = os.path.join(self.script_dir, "attendance.csv")
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
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # This loop processes every face found in the frame
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])

                if confidence < 80:
                    try:
                        conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
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

        self.root.after(15, self.update_frame)

    def on_close(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

