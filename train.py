import tkinter as tk
from tkinter import Label, Button, messagebox, ttk
from PIL import Image
import os
import cv2
import numpy as np

# Import the centralized configuration
from config import TRAINING_CONFIG, PATHS

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x350+500+200")
        self.root.title("Train Face Recognition Model")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.progress_var = tk.DoubleVar()
        
        title_lbl = Label(self.root, text="TRAIN THE MODEL", font=("tahoma", 20, "bold"), bg="#2c3e50", fg="white")
        title_lbl.pack(pady=20)

        info_lbl = Label(self.root, text="Click the button below to start training\non the collected face samples.", 
                         font=("tahoma", 12), bg="#2c3e50", fg="#ecf0f1")
        info_lbl.pack(pady=10, padx=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, padx=20, fill='x')

        # Status label
        self.status_label = Label(self.root, text="Ready to train", 
                                  font=("tahoma", 10), bg="#2c3e50", fg="#ecf0f1")
        self.status_label.pack(pady=5)

        train_btn = Button(self.root, text="TRAIN MODEL", command=self.train_classifier, 
                           font=("tahoma", 14, "bold"), bg="#2980b9", fg="white", cursor="hand2",
                           activebackground="#3498db", activeforeground="white", borderwidth=0)
        train_btn.pack(pady=20, ipadx=20, ipady=10)

    def train_classifier(self):
        """
        Reads face images from the 'data' directory, trains a recognizer,
        and saves the trained model to 'classifier.xml'.
        """
        # Use settings from config.py
        data_dir = os.path.join(self.script_dir, TRAINING_CONFIG['data_directory'])
        if not os.path.exists(data_dir) or not os.listdir(data_dir):
            messagebox.showerror("Error", "No data found to train. Please collect photo samples first.", parent=self.root)
            return

        # Get all image paths from the data directory
        image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        
        faces = []
        ids = []

        self.status_label.config(text="Processing images...")
        self.progress_var.set(0)
        
        total_images = len(image_paths)
        if total_images == 0:
            messagebox.showerror("Error", "Data folder is empty.", parent=self.root)
            return

        processed = 0

        for image_path in image_paths:
            try:
                img = Image.open(image_path).convert('L') # Convert to grayscale
                imageNp = np.array(img, 'uint8')
                # Extract the ID (roll number) from the filename (e.g., "user.123.1.jpg")
                id = int(os.path.split(image_path)[1].split('.')[1])
                
                faces.append(imageNp)
                ids.append(id)
                processed += 1
                
                # Update progress (first 50% is for processing images)
                progress = (processed / total_images) * 50
                self.progress_var.set(progress)
                self.status_label.config(text=f"Processing image {processed}/{total_images}")
                self.root.update_idletasks() # Use update_idletasks to prevent UI freeze
                
            except Exception as e:
                print(f"Skipping file {image_path} due to error: {e}")
                continue

        if not ids:
            messagebox.showerror("Error", "Could not process any valid images. Check the data folder.", parent=self.root)
            self.status_label.config(text="Ready to train")
            return

        ids = np.array(ids)

        # ========== Train the classifier and save ===========
        self.status_label.config(text="Training model... Please wait.")
        self.progress_var.set(60)
        self.root.update_idletasks()
        
        # LBPH (Local Binary Patterns Histograms) is a robust face recognition algorithm.
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, ids)
        
        self.progress_var.set(90)
        self.status_label.config(text="Saving model...")
        self.root.update_idletasks()
        
        # Use path from config.py
        classifier_path = os.path.join(self.script_dir, PATHS['classifier'])
        recognizer.write(classifier_path)

        self.progress_var.set(100)
        self.status_label.config(text="Training completed!")
        
        messagebox.showinfo("Success", f"Training completed successfully!\nProcessed {len(faces)} images.\nModel saved to classifier.xml", parent=self.root)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Train(root)
    root.mainloop()

