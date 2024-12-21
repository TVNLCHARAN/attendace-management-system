import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Attendance Management System", layout="wide")
st.title("Welcome to the Attendance Management System")
st.markdown("""
This application is designed to provide an efficient and user-friendly way to manage attendance 
using face recognition technology. With features like real-time face detection, recognition, and automated attendance logging, 
The aim to simplify the attendance process for organizations, schools, and events. 🎯📸
""")

def fetch_attendance_data():
    try:
        conn = sqlite3.connect("attendance.db")
        query = "SELECT * FROM attendance"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    except Exception as e:
        st.error(f"Error fetching data from the database: {e}")
        return None

def fetch_user_data():
    try:
        conn = sqlite3.connect("attendance.db")
        query = "SELECT DISTINCT name FROM attendance"
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    except Exception as e:
        st.error(f"Error fetching user data from the database: {e}")
        return None

st.subheader("Attendance Overview 📊")

attendance_data = fetch_attendance_data()
if attendance_data is not None and not attendance_data.empty:
    st.markdown(f"### Total Records: {len(attendance_data)}")
    st.dataframe(attendance_data)
else:
    st.info("No attendance data available.")

st.subheader("Users in the System 🧑‍💻")

user_data = fetch_user_data()
if user_data is not None and not user_data.empty:
    st.markdown(f"### Total Registered Users: {len(user_data)}")
    st.write(user_data)
else:
    st.info("No user data available.")

st.sidebar.subheader("Current Date and Time")
st.sidebar.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.markdown("---")
st.markdown("© 2024 Attendance Management System. All rights reserved.")
