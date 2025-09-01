import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import cv2
# Import the new configuration file
from config import DB_CONFIG, TRAINING_CONFIG, PATHS

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Information System")

        # ===== Use Database Connection Details from config.py =====
        self.db_config = DB_CONFIG

        # ===== Variables =====
        self.var_dep = tk.StringVar()
        self.var_sem = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_search = tk.StringVar()
        self.var_search_by = tk.StringVar()

        # Get the directory of the current script
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # ===== UI Setup (No changes here) =====
        # Background Image
        bg_img_path = os.path.join(self.script_dir, "Images", "Interface.jpg")
        try:
            img = Image.open(bg_img_path)
            img = img.resize((1366, 768), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            bg_img = tk.Label(self.root, image=self.photoimg)
            bg_img.place(x=0, y=0, width=1366, height=768)
        except FileNotFoundError:
            self.root.config(bg="#a2d2ff")
            print(f"Warning: Background image not found at {bg_img_path}.")

        title_lbl = tk.Label(self.root, text="STUDENT INFORMATION SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="#03045e")
        title_lbl.place(x=0, y=0, width=1366, height=50)
        
        main_frame = tk.Frame(self.root, bd=2, bg="white")
        main_frame.place(x=20, y=60, width=1310, height=680)

        left_frame = tk.LabelFrame(main_frame, bd=2, relief=tk.RIDGE, text="Student Information", font=("times new roman", 12, "bold"), bg="white")
        left_frame.place(x=10, y=10, width=640, height=660)

        # ... (All other UI widget definitions remain the same) ...
        dep_label = tk.Label(left_frame, text="Department:", font=("times new roman", 12), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        dep_combo = ttk.Combobox(left_frame, textvariable=self.var_dep, font=("times new roman", 12), state="readonly", width=18)
        dep_combo["values"] = ("Select Department", "Computer Science", "IT", "Mechanical", "Civil", "Electrical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        sem_label = tk.Label(left_frame, text="Semester:", font=("times new roman", 12), bg="white")
        sem_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        sem_combo = ttk.Combobox(left_frame, textvariable=self.var_sem, font=("times new roman", 12), state="readonly", width=18)
        sem_combo["values"] = ("Select Semester", "I", "II", "III", "IV", "V", "VI", "VII", "VIII")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=2, pady=5, sticky="w")

        name_label = tk.Label(left_frame, text="Student Name:", font=("times new roman", 12), bg="white")
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        name_entry = ttk.Entry(left_frame, textvariable=self.var_name, width=20, font=("times new roman", 12))
        name_entry.grid(row=2, column=1, padx=2, pady=5, sticky="w")

        roll_label = tk.Label(left_frame, text="Student Roll:", font=("times new roman", 12), bg="white")
        roll_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        roll_entry = ttk.Entry(left_frame, textvariable=self.var_roll, width=20, font=("times new roman", 12))
        roll_entry.grid(row=3, column=1, padx=2, pady=5, sticky="w")

        btn_frame = tk.Frame(left_frame, bd=2, relief=tk.RIDGE, bg="white")
        btn_frame.place(x=10, y=200, width=610, height=80)

        save_btn = tk.Button(btn_frame, text="Save", command=self.submit_data, font=("times new roman", 13, "bold"), bg="#0077b6", fg="white", width=14)
        save_btn.grid(row=0, column=0, padx=5, pady=5)
        # ... (and so on for all UI elements)
        update_btn = tk.Button(btn_frame, text="Update", command=self.update_data, font=("times new roman", 13, "bold"), bg="#0077b6", fg="white", width=14)
        update_btn.grid(row=0, column=1, padx=5, pady=5)
        delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_data, font=("times new roman", 13, "bold"), bg="#d00000", fg="white", width=14)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)
        reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_data, font=("times new roman", 13, "bold"), bg="#52b69a", fg="white", width=14)
        reset_btn.grid(row=0, column=3, padx=5, pady=5)
        photo_btn = tk.Button(btn_frame, text="Take Photo Sample", command=self.generate_dataset, font=("times new roman", 13, "bold"), bg="#ff9f1c", fg="white", width=30)
        photo_btn.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        right_frame = tk.LabelFrame(main_frame, bd=2, relief=tk.RIDGE, text="Student Details", font=("times new roman", 12, "bold"), bg="white")
        right_frame.place(x=660, y=10, width=640, height=660)
        search_frame = tk.Frame(right_frame, bd=2, relief=tk.RIDGE, bg="white")
        search_frame.place(x=5, y=5, width=625, height=50)
        search_label = tk.Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="white")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 12), state="readonly", width=12)
        search_combo["values"] = ("Select", "Roll No", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=18, font=("times new roman", 12))
        search_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        search_btn = tk.Button(search_frame, text="Search", command=self.search_data, font=("times new roman", 12, "bold"), bg="#0077b6", fg="white", width=10)
        search_btn.grid(row=0, column=3, padx=5)
        show_all_btn = tk.Button(search_frame, text="Show All", command=self.fetch_data, font=("times new roman", 12, "bold"), bg="#52b69a", fg="white", width=10)
        show_all_btn.grid(row=0, column=4, padx=5)
        table_frame = tk.Frame(right_frame, bd=2, relief=tk.RIDGE, bg="white")
        table_frame.place(x=5, y=60, width=625, height=570)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("times new roman", 12, "bold"))
        style.configure("Treeview", font=("times new roman", 11), rowheight=25)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.student_table = ttk.Treeview(table_frame, columns=("dep", "sem", "name", "roll"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.student_table.yview)
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll", text="Roll No")
        self.student_table["show"] = "headings"
        self.student_table.column("dep", width=150)
        self.student_table.column("sem", width=100)
        self.student_table.column("name", width=150)
        self.student_table.column("roll", width=100)
        self.student_table.pack(fill=tk.BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
    # ================== Database Connection Function ==================
    def _get_db_connection(self):
        """Establishes and returns a database connection using config."""
        try:
            # Use dictionary unpacking to pass credentials from config
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}", parent=self.root)
            return None
    
    # ================== Functions for Database Operations ==================
    # (No changes needed in submit_data, fetch_data, update_data, etc. as they all use _get_db_connection)
    def submit_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_roll.get() == "":
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        conn = self._get_db_connection()
        if not conn: return
        
        my_cursor = conn.cursor()
        try:
            my_cursor.execute("SELECT roll FROM students WHERE roll=%s", (self.var_roll.get(),))
            if my_cursor.fetchone():
                messagebox.showerror("Error", f"Student with Roll No {self.var_roll.get()} already exists.", parent=self.root)
                return

            my_cursor.execute("INSERT INTO students (dep, sem, name, roll) VALUES (%s, %s, %s, %s)", (
                self.var_dep.get(), self.var_sem.get(), self.var_name.get(), self.var_roll.get()
            ))
            conn.commit()
            self.fetch_data()
            self.reset_data()
            messagebox.showinfo("Success", "Student details have been added successfully.", parent=self.root)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}", parent=self.root)
        finally:
            if conn.is_connected():
                conn.close()

    def fetch_data(self):
        conn = self._get_db_connection()
        if not conn: return
        my_cursor = conn.cursor()
        try:
            my_cursor.execute("SELECT * FROM students")
            data = my_cursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            if data:
                for i in data:
                    self.student_table.insert("", tk.END, values=i)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch data: {err}", parent=self.root)
        finally:
            if conn.is_connected():
                conn.close()

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        if not cursor_focus: return
        content = self.student_table.item(cursor_focus)
        data = content.get("values")
        if data:
            self.var_dep.set(data[0])
            self.var_sem.set(data[1])
            self.var_name.set(data[2])
            self.var_roll.set(data[3])

    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_roll.get() == "":
            messagebox.showerror("Error", "All fields are required to update.", parent=self.root)
            return
        if messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root):
            conn = self._get_db_connection()
            if not conn: return
            my_cursor = conn.cursor()
            try:
                my_cursor.execute("UPDATE students SET dep=%s, sem=%s, name=%s WHERE roll=%s", (
                    self.var_dep.get(), self.var_sem.get(), self.var_name.get(), self.var_roll.get()
                ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                messagebox.showinfo("Success", "Student details successfully updated.", parent=self.root)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}", parent=self.root)
            finally:
                if conn.is_connected():
                    conn.close()
    
    def delete_data(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll No. is required to delete.", parent=self.root)
            return
        if messagebox.askyesno("Delete", "Do you want to delete this student?", parent=self.root):
            conn = self._get_db_connection()
            if not conn: return
            my_cursor = conn.cursor()
            try:
                sql = "DELETE FROM students WHERE roll=%s"
                val = (self.var_roll.get(),)
                my_cursor.execute(sql, val)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                messagebox.showinfo("Deleted", "Student details successfully deleted.", parent=self.root)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}", parent=self.root)
            finally:
                if conn.is_connected():
                    conn.close()

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_sem.set("Select Semester")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_search_by.set("Select")
        self.var_search.set("")

    def search_data(self):
        search_by = self.var_search_by.get()
        search_term = self.var_search.get()
        if search_by == "Select" or search_term == "":
            messagebox.showerror("Error", "Please select a search criterion and enter a value.", parent=self.root)
            return
        conn = self._get_db_connection()
        if not conn: return
        my_cursor = conn.cursor()
        try:
            query_map = {"Roll No": "roll", "Name": "name"}
            db_column = query_map.get(search_by)
            if db_column:
                my_cursor.execute(f"SELECT * FROM students WHERE {db_column} LIKE %s", ('%' + search_term + '%',))
                data = my_cursor.fetchall()
                self.student_table.delete(*self.student_table.get_children())
                if data:
                    for i in data:
                        self.student_table.insert("", tk.END, values=i)
                else:
                    messagebox.showinfo("Not Found", "No records found matching your criteria.", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Search failed: {err}", parent=self.root)
        finally:
            if conn.is_connected():
                conn.close()
    
    # ================== Generate Photo Samples ==================
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_roll.get() == "":
            messagebox.showerror("Error", "All student fields are required before taking photos.", parent=self.root)
            return
        
        roll_no = self.var_roll.get()
        
        # Use settings from config.py
        data_dir = os.path.join(self.script_dir, TRAINING_CONFIG['data_directory'])
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Use cascade path from config.py
        cascade_path = os.path.join(self.script_dir, PATHS['cascade'])
        if not os.path.exists(cascade_path):
            messagebox.showerror("Error", f"Haarcascade file not found at: {cascade_path}", parent=self.root)
            return
        
        face_classifier = cv2.CascadeClassifier(cascade_path)

        def face_cropped(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                return img[y:y+h, x:x+w]
            return None

        cap = cv2.VideoCapture(0)
        img_id = 0
        max_images = TRAINING_CONFIG.get('max_images_per_person', 100)
        
        while True:
            ret, my_frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Could not access the camera.", parent=self.root)
                break

            cropped_face = face_cropped(my_frame)
            if cropped_face is not None:
                img_id += 1
                face = cv2.resize(cropped_face, (450, 450))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                
                # Use file format from config.py
                file_name = TRAINING_CONFIG['image_format'].format(roll=roll_no, image_number=img_id)
                file_path = os.path.join(data_dir, file_name)
                
                cv2.imwrite(file_path, face)
                cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                cv2.imshow("Capturing Face...", face)

            # Wait for 'q' key to be pressed or until max images are taken
            if cv2.waitKey(1) == 13 or img_id >= max_images:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", f"Generated {img_id} photo samples for Roll No: {roll_no}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = Student(root)
    root.mainloop()

