import mysql.connector

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="hrms_db")
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE hr_users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    cursor.execute("ALTER TABLE employees ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    conn.commit()
    print("Database altered successfully with created_at fields.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
