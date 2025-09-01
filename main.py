import tkinter as tk
from tkinter import Toplevel, Frame, Button, Label, messagebox
from PIL import Image, ImageTk, ImageDraw
import os

# Import all the other class modules that make up the application
from student import Student 
from train import Train
from face_recognizer import FaceRecognizer
from attendacnce import Attendance

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        # Get the directory where the script is located to make paths relative
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # ===== Background =====
        bg_img_path = os.path.join(self.script_dir, "Images", "Interface.jpg")
        try:
            img = Image.open(bg_img_path)
            img = img.resize((1366, 768), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            bg_img = Label(self.root, image=self.photoimg)
            bg_img.place(x=0, y=0, width=1366, height=768)
        except FileNotFoundError:
            self.root.config(bg="#03001C") # Fallback background color
            print(f"Warning: Background image not found at {bg_img_path}")
        
        # Title Label
        title_lbl = Label(self.root, text="CLASS MONITORING SYSTEM", font=("tahoma", 35, "bold"), bg="#0a0a23", fg="white")
        title_lbl.place(x=0, y=0, width=1366, height=60)

        # ===== BUTTON 1: Student =====
        student_icon_path = os.path.join(self.script_dir, "Images", "student.png")
        self.student_photo = self.make_rounded(student_icon_path, fallback_color="#3498db")
        self.create_button_with_text(bg_img, self.student_photo, "STUDENT DETAILS", x=150, y=500, command=self.student_details)

        # ===== BUTTON 2: Face Recognition =====
        face_icon_path = os.path.join(self.script_dir, "Images", "Face_Recognition.png")
        self.face_photo = self.make_rounded(face_icon_path, fallback_color="#e74c3c")
        self.create_button_with_text(bg_img, self.face_photo, "FACE RECOGNITION", x=350, y=500, command=self.face_recognition)

        # ===== BUTTON 3: Attendance =====
        attendance_icon_path = os.path.join(self.script_dir, "Images", "Attendance.png")
        self.attendance_photo = self.make_rounded(attendance_icon_path, fallback_color="#2ecc71")
        self.create_button_with_text(bg_img, self.attendance_photo, "ATTENDANCE", x=550, y=500, command=self.attendance_details)
        
        # ===== BUTTON 4: Train Data =====
        # Note: You can create/download an icon named "Train_Data.png" for this
        train_icon_path = os.path.join(self.script_dir, "Images", "Train_Data.png")
        self.train_photo = self.make_rounded(train_icon_path, fallback_color="#f39c12")
        self.create_button_with_text(bg_img, self.train_photo, "TRAIN DATA", x=750, y=500, command=self.train_data)


    # ================== Helper Functions for Hover Effect ==================
    def on_enter(self, frame):
        """Changes the background of the frame and its children on hover."""
        hover_color = "#2fa4ff"
        frame.config(bg=hover_color)
        # Change background for all widgets inside the frame (button, label)
        for child in frame.winfo_children():
            child.config(bg=hover_color)

    def on_leave(self, frame):
        """Resets the background of the frame and its children when not hovered."""
        default_color = "#0f0f2d"
        frame.config(bg=default_color)
        # Reset background for all widgets inside the frame
        for child in frame.winfo_children():
            child.config(bg=default_color)

    # ================== Helper Function for Creating Rounded Images ==================
    def make_rounded(self, img_path, size=(70, 70), fallback_color="#cccccc"):
        """Creates a rounded image. If the image path is not found, creates a plain colored circle."""
        try:
            img = Image.open(img_path).resize(size, Image.LANCZOS).convert("RGBA")
        except FileNotFoundError:
            # If icon is missing, create a placeholder circle
            print(f"Warning: Icon not found at {img_path}. Creating fallback.")
            img = Image.new("RGBA", size)
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0) + size, fill=fallback_color)

        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    # ================== Function for Creating Buttons ==================
    def create_button_with_text(self, parent, image, text, x, y, command):
        """Creates a button with an image and text below it, with a stable hover effect."""
        frame = Frame(parent, bg="#0f0f2d", width=140, height=140)
        frame.place(x=x, y=y)
        frame.pack_propagate(False) # Prevents the frame from shrinking

        # Set activebackground to the same color to prevent a color flash on click
        btn = Button(frame, image=image, command=command, cursor="hand2",
                     borderwidth=0, bg="#0f0f2d", activebackground="#0f0f2d")
        btn.pack(pady=(10, 5))

        lbl = Label(frame, text=text, font=("tahoma", 10, "bold"), bg="#0f0f2d", fg="white")
        lbl.pack()

        # Bind events to the frame and all its children to make the whole area reactive
        widgets_to_bind = [frame, btn, lbl]
        for widget in widgets_to_bind:
            widget.bind("<Enter>", lambda e, f=frame: self.on_enter(f))
            widget.bind("<Leave>", lambda e, f=frame: self.on_leave(f))


    # ================== Button Command Functions (App Navigation) ==================
    def student_details(self):
        """Opens the student details window."""
        new_window = Toplevel(self.root)
        app = Student(new_window)

    def train_data(self):
        """Opens the model training window."""
        new_window = Toplevel(self.root)
        app = Train(new_window)

    def face_recognition(self):
        """Opens the face recognition window."""
        new_window = Toplevel(self.root)
        app = FaceRecognizer(new_window)
    
    def attendance_details(self):
        """Opens the new attendance viewer window."""
        new_window = Toplevel(self.root)
        app = Attendance(new_window)


if __name__ == "__main__":
    root = tk.Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()

