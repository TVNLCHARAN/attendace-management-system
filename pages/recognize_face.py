import cv2
import os
import sys
import sqlite3
from datetime import datetime
import streamlit as st

if "attendance_marked" not in st.session_state:
    st.session_state.attendance_marked = False
if "num_frames_rec" not in st.session_state:
    st.session_state.num_frames_rec = 0
if "recognized_name" not in st.session_state:
    st.session_state.recognized_name = None

cascade_path = os.path.join(os.path.dirname(__file__), '..', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

sys.path.append(os.path.abspath(os.path.join("database")))
from database.database import fetch_faces

st.title("Click the button to mark attendance")
stframe = st.empty()

mark_button = st.button("Mark Attendance")
confirm_button, retry_button = st.columns(2)

def fetch_name_by_label(label):
    for row in fetch_faces():
        if row[0] == label:
            return row[1]

def recognize_and_mark_attendance():
    recognizer.read('face_recognizer.yml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0 and not st.session_state.attendance_marked:
                stframe.error("No face detected.")

            for (x, y, w, h) in faces:
                gray_face = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(gray_face)

                if confidence < 50:
                    name = fetch_name_by_label(label)
                    st.session_state.recognized_name = name
                    st.session_state.num_frames_rec += 1
                    cv2.putText(frame, f"{name} ({100-confidence:.2f})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    if st.session_state.num_frames_rec >= 10:
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if not st.session_state.attendance_marked:
                stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 'Recognizing face')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def confirm_recognition():
    current_name = st.session_state.recognized_name
    if current_name:
        st.write(f"## Recognized as: {current_name}")
        if st.button("Confirm Attendance"):
            mark_attendance(current_name)
            st.success(f"Attendance marked successfully for {current_name}.")
            st.session_state.attendance_marked = True
            st.session_state.num_frames_rec = 0
            st.session_state.recognized_name = None
        elif st.button("Retry"):
            st.session_state.num_frames_rec = 0
            st.session_state.recognized_name = None
            st.session_state.attendance_marked = False
            recognize_and_mark_attendance()

def mark_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, current_date, current_time))
    conn.commit()
    conn.close()

if mark_button:
    recognize_and_mark_attendance()

if st.session_state.recognized_name and not st.session_state.attendance_marked:
    confirm_recognition()
