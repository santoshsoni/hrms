import mysql.connector
from werkzeug.security import generate_password_hash

def create_database():
    try:
        # Connect to local MySQL server without specifying db initially
        # Make sure user 'root' and password '' are correct for XAMPP default
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS hrms_db")
        print("Database 'hrms_db' ensured successfully.")
        
        # Connect to the newly created database
        conn.database = "hrms_db"
        
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hr_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'hr_users' ensured successfully.")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            designation VARCHAR(100),
            salary DECIMAL(10, 2),
            date_joined DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'employees' ensured successfully.")
        
        # Insert default Admin user if not exists (password: admin123)
        cursor.execute("SELECT * FROM hr_users WHERE username='admin'")
        if not cursor.fetchone():
            hashed_pw = generate_password_hash('admin123')
            cursor.execute("INSERT INTO hr_users (username, password) VALUES (%s, %s)", ('admin', hashed_pw))
            conn.commit()
            print("Default admin user created: Username='admin' / Password='admin123'")
        else:
            print("Admin user already exists.")
            
        print("Database setup complete!")
        
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_database()
