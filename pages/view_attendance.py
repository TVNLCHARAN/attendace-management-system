import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def get_attendance_by_name(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, time FROM attendance WHERE name = ?", (name,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_attendance_summary():
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT name, date FROM attendance", conn)
    conn.close()
    return df

st.title("View Attendance Records")

name = st.text_input("Enter your registered name:")
if st.button("Search"):
    if name:
        attendance_records = get_attendance_by_name(name)
        if attendance_records:
            st.success(f"Attendance records for {name}:")
            df = pd.DataFrame(attendance_records, columns=["Date", "Time"])
            st.table(df)
        else:
            st.warning("No attendance records found for the entered name.")
    else:
        st.error("Please enter a name to search.")

st.header("Attendance Summary")
summary_df = get_attendance_summary()
print(summary_df)

if not summary_df.empty:
    st.dataframe(summary_df)

    st.subheader("Attendance Counts per Person")
    attendance_counts = summary_df.groupby("name").count()["date"].reset_index()
    attendance_counts.columns = ["Name", "Attendance Count"]

    fig, ax = plt.subplots()
    ax.bar(attendance_counts["Name"], attendance_counts["Attendance Count"], color="skyblue")
    ax.set_xlabel("Name")
    ax.set_ylabel("Attendance Count")
    ax.set_title("Attendance Summary")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Attendance Trends")
    summary_df["date"] = pd.to_datetime(summary_df["date"])
    trends = summary_df.groupby("date").count()["name"].reset_index()
    trends.columns = ["Date", "Attendance Count"]

    fig, ax = plt.subplots()
    ax.plot(trends["Date"], trends["Attendance Count"], marker="o", color="green")
    ax.set_xlabel("Date")
    ax.set_ylabel("Attendance Count")
    ax.set_title("Daily Attendance Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("No attendance data available.")
