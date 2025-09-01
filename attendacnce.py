import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600+300+100")
        self.root.title("Attendance Records")
        self.root.configure(bg="#f0f8ff")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.attendance_file = os.path.join(self.script_dir, "attendance.csv")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_lbl = tk.Label(main_frame, text="ATTENDANCE RECORDS", font=("tahoma", 20, "bold"), bg="#f0f8ff", fg="#003366")
        title_lbl.pack(pady=(0, 10))

        # Table Frame
        table_frame = tk.Frame(main_frame, bd=2, relief=tk.RIDGE)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # Treeview (Table)
        self.attendance_table = ttk.Treeview(table_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        self.attendance_table['columns'] = ("Name", "Roll", "Department", "Time", "Date", "Status")
        
        # Headings
        self.attendance_table.heading("#0", text="")
        self.attendance_table.heading("Name", text="Name")
        self.attendance_table.heading("Roll", text="Roll No.")
        self.attendance_table.heading("Department", text="Department")
        self.attendance_table.heading("Time", text="Time")
        self.attendance_table.heading("Date", text="Date")
        self.attendance_table.heading("Status", text="Status")

        # Columns
        self.attendance_table.column("#0", width=0, stretch=tk.NO)
        self.attendance_table.column("Name", width=150)
        self.attendance_table.column("Roll", width=100)
        self.attendance_table.column("Department", width=150)
        self.attendance_table.column("Time", width=100)
        self.attendance_table.column("Date", width=100)
        self.attendance_table.column("Status", width=100)

        self.attendance_table.pack(fill=tk.BOTH, expand=True)
        self.load_data()

        # Button Frame
        btn_frame = tk.Frame(main_frame, bg="#f0f8ff")
        btn_frame.pack(fill=tk.X, pady=10)

        # Buttons
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.load_data, font=("tahoma", 12), bg="#4682b4", fg="white", width=15)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        export_btn = tk.Button(btn_frame, text="Export CSV", command=self.export_csv, font=("tahoma", 12), bg="#32cd32", fg="white", width=15)
        export_btn.pack(side=tk.LEFT, padx=5)
        
    def load_data(self):
        """Loads data from the attendance.csv file into the table."""
        # Clear existing data
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)
            
        try:
            with open(self.attendance_file, 'r', newline='') as f:
                reader = csv.reader(f)
                # Skip header
                next(reader, None)
                for row in reader:
                    if row: # Ensure row is not empty
                        self.attendance_table.insert('', 'end', values=row)
        except FileNotFoundError:
            messagebox.showinfo("Info", "Attendance file not found. It will be created when you first mark attendance.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}", parent=self.root)

    def export_csv(self):
        """Exports the current table data to a new CSV file."""
        if not self.attendance_table.get_children():
            messagebox.showerror("Error", "No data to export.", parent=self.root)
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Attendance As"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Name", "Roll", "Department", "Time", "Date", "Status"])
                # Write data
                for row_id in self.attendance_table.get_children():
                    row = self.attendance_table.item(row_id)['values']
                    writer.writerow(row)
            messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}", parent=self.root)
