import streamlit as st
import cv2



st.title("Attendance Management System")

cap = cv2.VideoCapture(0)

stframe = st.empty()

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture video.")
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    stframe.image(frame, channels="RGB", use_container_width=True)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()
