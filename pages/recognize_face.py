import cv2
import os
import sys
import sqlite3
from datetime import datetime
import streamlit as st

cascade_path = os.path.join(os.path.dirname(__file__), '..', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

sys.path.append(os.path.abspath(os.path.join("database")))
from database.database import fetch_faces

stframe = st.empty()

st.title("Click the button to mark attendance")

mark_button = st.button("Mark Attendance")
current_name = st.empty()
confirm_button = st.empty()
attendance_marked = False
num_frames_rec = 0

def fetch_name_by_label(label):
    for row in fetch_faces():
        if row[0] == label:
            return row[1]

def recognize_and_mark_attendance():
    global attendance_marked

    recognizer.read('face_recognizer.yml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        frame = cv2.flip(frame, 1)

        if len(faces) == 0 and not attendance_marked:
            stframe.error("No face detected.")

        for (x, y, w, h) in faces:
            gray_face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(gray_face)

            if confidence < 100:
                name = fetch_name_by_label(label)
                print(f"Recognized: {name} with confidence: {confidence}")
                cv2.putText(frame, f"{name} ({confidence:.2f})", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                num_frames_rec += 1
                if num_frames_rec >= 10:
                    confirm_recognition(name)
                    cap.release()
                    cv2.destroyAllWindows()
            else:
                cv2.putText(frame, "Unknown", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if not attendance_marked:
            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 'Recognizing face')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def confirm_recognition(name):
    global attendance_marked

    current_name.write(f"Recognized as: {name}")
    if confirm_button.button("Confirm"):
        mark_attendance(name)
        st.success(f"Attendance marked successfully for {name}.")
        attendance_marked = True

def mark_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, current_date, current_time))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if mark_button:
        recognize_and_mark_attendance()
