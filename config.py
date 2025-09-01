import os

# Database Configuration
DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", "root"),  # Your MySQL password
    'database': os.getenv("DB_NAME", "student_management")
}

# Face Recognition Configuration
FACE_RECOGNITION_CONFIG = {
    'confidence_threshold': 80,  # Lower = more strict recognition
    'frame_interval': 15,  # milliseconds between frame updates
    'face_scale_factor': 1.3,
    'face_min_neighbors': 5
}

# Training Configuration
TRAINING_CONFIG = {
    'data_directory': 'data',
    'image_format': 'user.{roll}.{image_number}.jpg',
    'min_images_per_person': 1,
    'max_images_per_person': 100
}

# File Paths
PATHS = {
    'classifier': 'classifier.xml',
    'cascade': 'haarcascade_frontalface_default.xml',
    'attendance': 'attendance.csv'
}

# UI Configuration
UI_CONFIG = {
    'window_size': '800x650',
    'window_position': '+300+80',
    'title': 'Face Recognition System'
}
