import tkinter as tk
from tkinter import Toplevel, Frame, Button, Label
from PIL import Image, ImageTk, ImageDraw
from student import Student  # Import the Student class from your student.py file

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")

        # ===== Background =====
        # Note: Please make sure the image path is correct on your system.
        bg_img_path = r"C:\Users\dutta\OneDrive\Desktop\Class_Monitoring_System_Using_Computer_Vision\Images\Interface.jpg"
        img = Image.open(bg_img_path)
        img = img.resize((1366, 768), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=0, width=1366, height=768)

        # ===== BUTTON 1: Student =====
        self.student_photo = self.make_rounded(r"C:\Users\dutta\OneDrive\Desktop\Class_Monitoring_System_Using_Computer_Vision\Images\student.png")
        self.create_button_with_text(bg_img, self.student_photo, "STUDENT DETAILS", x=150, y=500, command=self.student_details)

        # ===== BUTTON 2: Face Recognition =====
        self.face_photo = self.make_rounded(r"C:\Users\dutta\OneDrive\Desktop\Class_Monitoring_System_Using_Computer_Vision\Images\Face_Recognition.png")
        self.create_button_with_text(bg_img, self.face_photo, "FACE RECOGNITION", x=350, y=500, command=self.face_recognition)

        # ===== BUTTON 3: Attendance =====
        self.attendance_photo = self.make_rounded(r"C:\Users\dutta\OneDrive\Desktop\Class_Monitoring_System_Using_Computer_Vision\Images\Attendance.png")
        self.create_button_with_text(bg_img, self.attendance_photo, "ATTENDANCE", x=550, y=500, command=self.attendance)

    # ================== Helper Functions ==================
    @staticmethod
    def make_rounded(img_path, size=(70, 70)):
        """Creates a rounded image."""
        img = Image.open(img_path).resize(size, Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    @staticmethod
    def on_enter(e):
        """Changes button background on hover."""
        e.widget.config(bg="#2fa4ff")

    @staticmethod
    def on_leave(e):
        """Resets button background when not hovered."""
        e.widget.config(bg="#0f0f2d")

    def create_button_with_text(self, parent, image, text, x, y, command):
        """Creates a button with an image and text below it."""
        frame = Frame(parent, bg="#0f0f2d", width=140, height=140)
        frame.place(x=x, y=y)
        
        btn = Button(frame, image=image, command=command, cursor="hand2",
                     borderwidth=0, bg="#0f0f2d", activebackground="#2fa4ff")
        btn.pack(pady=(10, 5))

        lbl = Label(frame, text=text, font=("tahoma", 10, "bold"), bg="#0f0f2d", fg="white")
        lbl.pack()

        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)
        return btn

    # ================== Button Command Functions ==================
    def student_details(self):
        """Opens the student details window."""
        new_window = Toplevel(self.root)
        app = Student(new_window)  # Correctly instantiate the Student class

    def face_recognition(self):
        """Placeholder for face recognition functionality."""
        print("Face Recognition Clicked")

    def attendance(self):
        """Placeholder for attendance functionality."""
        print("Attendance Clicked")


if __name__ == "__main__":
    root = tk.Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
