import sqlite3

def print_faces_from_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    query = "SELECT * FROM faces"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            print("Face Data from 'faces' table:")
            for row in rows:
                print(row[2])
        else:
            print("No data found in the 'faces' table.")

    except sqlite3.Error as e:
        print(f"Error fetching data from the database: {e}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print_faces_from_db()
