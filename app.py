import streamlit as st
import cv2
import numpy as np
from database.database import fetch_faces
import os

st.title("Attendance Management System")
st.write("Face Recognition with Haar Cascades and LBPH")

recognizer = cv2.face.LBPHFaceRecognizer_create()
cascade_path = os.path.join('./', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)


def mark_attendance(name):
    st.success(f"Attendance marked for {name}!")

def recognize_face(frame, gray, face_db):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    name = None
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        label, confidence = recognizer.predict(face)
        if confidence > 70:
            name = face_db[label - 1][1]
            mark_attendance(name)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame, name

def load_recognizer_from_db(face_db):
    labels = []
    histograms = []
    
    name_to_label = {}
    label_count = 1

    for face in face_db:
        name = face[1]
        if name not in name_to_label:
            name_to_label[name] = label_count
            label_count += 1
        
        labels.append(name_to_label[name])
        histogram_data = face[2]
        if isinstance(histogram_data, str):
            histogram_data = bytes(histogram_data, 'utf-8')
        
        histograms.append(np.frombuffer(histogram_data, dtype=np.uint8))

    if len(histograms) == 0 or len(labels) == 0:
        raise ValueError("Histograms or Labels are empty.")
    
    if len(histograms) != len(labels):
        raise ValueError("Mismatch between number of histograms and labels.")

    labels = np.array(labels, dtype=np.int32)
    
    histograms = np.array(histograms, dtype=np.uint8)
    
    recognizer.train(histograms, labels)


run = st.button("Start Camera")
stframe = st.empty()

if run:
    cap = cv2.VideoCapture(0)
    face_db = fetch_faces() 
    load_recognizer_from_db(face_db)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame, name = recognize_face(frame, gray, face_db)

        stframe.image(frame, channels="BGR")

        if st.button("Stop"):
            cap.release()
            st.write("Camera Stopped")
            break