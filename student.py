import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Information System")

        # ===== Variables =====
        self.var_dep = tk.StringVar()
        self.var_sem = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_search = tk.StringVar()
        self.var_search_by = tk.StringVar()

        # ===== Background Image =====
        # Note: Please make sure the image path is correct on your system.
        bg_img_path = r"C:\Users\dutta\OneDrive\Desktop\Class_Monitoring_System_Using_Computer_Vision\Images\Interface.jpg"
        if os.path.exists(bg_img_path):
            img = Image.open(bg_img_path)
            img = img.resize((1366, 768), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            bg_img = tk.Label(self.root, image=self.photoimg)
            bg_img.place(x=0, y=0, width=1366, height=768)
        else:
            self.root.config(bg="lightblue")
            print(f"Warning: The background image was not found at {bg_img_path}.")


        # ===== Title Label =====
        title_lbl = tk.Label(self.root, text="STUDENT INFORMATION SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="darkblue")
        title_lbl.place(x=0, y=0, width=1366, height=50)
        
        # ===== Main Frame =====
        main_frame = tk.Frame(self.root, bd=2, bg="white")
        main_frame.place(x=20, y=60, width=1310, height=680)

        # ===== Left Frame =====
        left_frame = tk.LabelFrame(main_frame, bd=2, relief=tk.RIDGE, text="Student Information", font=("times new roman", 12, "bold"), bg="white")
        left_frame.place(x=10, y=10, width=640, height=660)

        # --- Student Info Content ---
        # Department
        dep_label = tk.Label(left_frame, text="Department:", font=("times new roman", 12), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        dep_combo = ttk.Combobox(left_frame, textvariable=self.var_dep, font=("times new roman", 12), state="readonly", width=18)
        dep_combo["values"] = ("Select Department", "Computer Science", "IT", "Mechanical", "Civil", "Electrical")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=5, sticky="w")

        # Semester
        sem_label = tk.Label(left_frame, text="Semester:", font=("times new roman", 12), bg="white")
        sem_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        sem_combo = ttk.Combobox(left_frame, textvariable=self.var_sem, font=("times new roman", 12), state="readonly", width=18)
        sem_combo["values"] = ("Select Semester", "I", "II", "III", "IV", "V", "VI", "VII", "VIII")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=2, pady=5, sticky="w")

        # Student Name
        name_label = tk.Label(left_frame, text="Student Name:", font=("times new roman", 12), bg="white")
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        name_entry = ttk.Entry(left_frame, textvariable=self.var_name, width=20, font=("times new roman", 12))
        name_entry.grid(row=2, column=1, padx=2, pady=5, sticky="w")

        # Student ROLL
        roll_label = tk.Label(left_frame, text="Student ROLL:", font=("times new roman", 12), bg="white")
        roll_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        roll_entry = ttk.Entry(left_frame, textvariable=self.var_roll, width=20, font=("times new roman", 12))
        roll_entry.grid(row=3, column=1, padx=2, pady=5, sticky="w")

        # ===== Button Frame =====
        btn_frame = tk.Frame(left_frame, bd=2, relief=tk.RIDGE, bg="white")
        btn_frame.place(x=10, y=200, width=430, height=45)

        save_btn = tk.Button(btn_frame, text="Save", command=self.submit_data, font=("times new roman", 13, "bold"), bg="blue", fg="white", width=14)
        save_btn.grid(row=0, column=0, padx=2, pady=5)

        update_btn = tk.Button(btn_frame, text="Update", command=self.update_data, font=("times new roman", 13, "bold"), bg="blue", fg="white", width=14)
        update_btn.grid(row=0, column=1, padx=2, pady=5)

        delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_data, font=("times new roman", 13, "bold"), bg="blue", fg="white", width=14)
        delete_btn.grid(row=0, column=2, padx=2, pady=5)

        # ===== Right Frame =====
        right_frame = tk.LabelFrame(main_frame, bd=2, relief=tk.RIDGE, text="Student Details", font=("times new roman", 12, "bold"), bg="white")
        right_frame.place(x=660, y=10, width=640, height=660)

        # --- Search Bar ---
        search_frame = tk.Frame(right_frame, bd=2, relief=tk.RIDGE, bg="white")
        search_frame.place(x=5, y=5, width=625, height=50)

        search_label = tk.Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="white")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("times new roman", 12), state="readonly", width=15)
        search_combo["values"] = ("Select", "Roll No", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=20, font=("times new roman", 12))
        search_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        search_btn = tk.Button(search_frame, text="Search", font=("times new roman", 12, "bold"), bg="blue", fg="white", width=12)
        search_btn.grid(row=0, column=3, padx=5, pady=5)

        # --- Table Frame ---
        table_frame = tk.Frame(right_frame, bd=2, relief=tk.RIDGE, bg="white")
        table_frame.place(x=5, y=60, width=625, height=570)

        # Style for the table
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

    # ================== Functions ==================
    def submit_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_roll.get() == "":
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="student_management")
            my_cursor = conn.cursor()
            my_cursor.execute("insert into students values(%s,%s,%s,%s)", (
                self.var_dep.get(),
                self.var_sem.get(),
                self.var_name.get(),
                self.var_roll.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Student details have been added successfully.", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="student_management")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from students")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", tk.END, values=i)
            conn.commit()
        else:
                self.student_table.delete(*self.student_table.get_children())
        conn.close()

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        if data:
            self.var_dep.set(data[0])
            self.var_sem.set(data[1])
            self.var_name.set(data[2])
            self.var_roll.set(data[3])

    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_roll.get() == "":
            messagebox.showerror("Error", "All fields are required to update.", parent=self.root)
        else:
            update = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
            if update > 0:
                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="student_management")
                my_cursor = conn.cursor()
                my_cursor.execute("update students set dep=%s, sem=%s, name=%s where roll=%s", (
                    self.var_dep.get(),
                    self.var_sem.get(),
                    self.var_name.get(),
                    self.var_roll.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details successfully updated.", parent=self.root)

    def delete_data(self):
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Roll No. is required to delete.", parent=self.root)
        else:
            delete = messagebox.askyesno("Delete", "Do you want to delete this student?", parent=self.root)
            if delete > 0:
                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="student_management")
                my_cursor = conn.cursor()
                sql = "delete from students where roll=%s"
                val = (self.var_roll.get(),)
                my_cursor.execute(sql, val)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Deleted", "Student details successfully deleted.", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = Student(root)
    root.mainloop()
