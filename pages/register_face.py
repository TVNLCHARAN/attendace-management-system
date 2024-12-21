import cv2
import numpy as np
import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join("database")))
from database.database import insert_face, fetch_faces


cascade_path = os.path.join(os.path.dirname(__file__), '..', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

stframe = st.empty()

def collect_images():
    cap = cv2.VideoCapture(0)
    collected_images = []
    count = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            collected_images.append(face)
            count += 1
            cv2.putText(frame, f"Captured {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # cv2.imshow("Collecting Images", frame)
            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 'Recording face')
        if len(faces)==0:
            stframe.write("## No Faces detected")

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 70:
            if count >= 70:
                stframe.success(f"Face Registered successfully for {name}")
            break

    cap.release()
    cv2.destroyAllWindows()
    return collected_images

def train_model(name):
    faces = []
    ids = []
    db_faces = fetch_faces()
    label = len(db_faces) + 1

    print(db_faces[-1][0], db_faces[-1][1])

    images = collect_images()
    for img in images:
        faces.append(img)
        ids.append(label)

    model_path = 'face_recognizer.yml'
    if os.path.exists(model_path):
        recognizer.read(model_path)
        print("Loaded existing model.")
    
    recognizer.update(faces, np.array(ids))
    recognizer.write(model_path)
    
    insert_face(name, recognizer.getHistograms()[label - 1].tobytes())
    print(f"Model updated and features stored for {name}.")

if __name__ == "__main__":
    name = st.text_input("Enter name to record face")
    button = st.button("Register Face")
    if button and name.strip() != "":
        train_model(name)