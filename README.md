# Class Monitoring System

## Overview
This project provides a Tkinter-based class monitoring system with face recognition, student management, and model training.

## Configuration
All database credentials, file paths, thresholds, and UI settings live in `config.py`. The application reads database credentials from environment variables.

### Environment variables
Copy the example file and update values for your environment:

```bash
cp .env.example .env
```

Set the following variables in your shell (or load them from your preferred `.env` workflow):

- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Example (bash):

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password_here
export DB_NAME=student_management
```

### Application settings
Adjust thresholds, file paths, and UI settings in `config.py`:

- `DB_CONFIG` for database connectivity defaults
- `FACE_RECOGNITION_CONFIG` for recognition thresholds and frame timing
- `TRAINING_CONFIG` for dataset and training inputs
- `PATHS` for classifier, cascade, and attendance files
- `UI_CONFIG` for per-window geometry and UI defaults

## Running the app
Launch the main application entrypoint:

```bash
python main.py
```

If you only want to manage students, run:

```bash
python student.py
```

To train the recognition model, run:

```bash
python train.py
```
