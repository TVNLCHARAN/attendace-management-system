# Attendance Management System

Welcome to the **Attendance Management System**! This project leverages face recognition technology to simplify and automate attendance marking. The system is designed to work with facial recognition, real-time detection, and a user-friendly interface built using Streamlit.

---

## Table of Contents
1. [Features](#features)
2. [Folder Structure](#folder-structure)
3. [Prerequisites](#prerequisites)
4. [Setup and Installation](#setup-and-installation)
5. [How to Use](#how-to-use)
6. [Future Enhancements](#future-enhancements)
7. [Contributing](#contributing)

---

## Features
- **Face Registration**: Add new faces to the system for recognition.
- **Face Recognition**: Real-time recognition of registered faces.
- **Attendance Logging**: Automatically logs attendance with date and time.
- **View Attendance**: Display attendance records in an interactive table.
- **Modular Design**: Organized into separate components for ease of maintenance.

---

## Folder Structure
```
attendance_system
├── app.py                # Main entry point for the Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── database
│   ├── database.db       # SQLite database (auto-created)
│   └── database.py       # Script to create database and tables
├── models
│   └── face_recognition_model.py  # Face recognition model
├── pages
│   ├── register_face.py  # Face registration functionality
│   ├── recognize_face.py # Face recognition functionality
│   └── view_attendance.py # View attendance records
├── utils
│   ├── db_operations.py  # Database operations helper functions
│   └── helpers.py        # General utility functions
└── assets
    └── styles.css        # CSS styles (optional)
```

---

## Prerequisites

Ensure you have the following installed on your system:
1. **Python**: Version 3.8 or higher
2. **pip**: Python package installer
3. **Virtual Environment** (optional but recommended)

---

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/attendance_system.git
cd attendance_system
```

### 2. Create a Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the Database
Run the `database.py` script to create the required SQLite database and tables:
```bash
python database/database.py
```

### 5. Run the Application
Start the Streamlit application:
```bash
streamlit run app.py
```

---

## How to Use

### Step 1: Register Faces
1. Navigate to the "Register Face" page.
2. Follow the instructions to capture and save facial data.

### Step 2: Recognize Faces
1. Go to the "Recognize Face" page.
2. Use the webcam to recognize faces in real-time.
3. Attendance will be marked automatically for recognized faces.

### Step 3: View Attendance
1. Visit the "View Attendance" page.
2. Browse attendance records in an interactive table.

---

## Notes
- **Authentication**: Authentication functionality is not yet developed. Consider restricting access to certain pages in the future.
- **Database**: Ensure `database.db` is created using the `database.py` script before accessing other functionalities.
- **Webcam Access**: Grant permission to access the webcam for face registration and recognition.

---

## Future Enhancements
- **User Authentication**: Add a secure login system for administrators and users.
- **Dashboard**: Create a summary dashboard with charts and analytics.
- **Notifications**: Send email or SMS notifications for attendance updates.
- **Enhanced Security**: Improve database security and implement encrypted storage.

---

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed explanation of your changes.

---

Happy Coding! 😊
