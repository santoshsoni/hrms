####################Today Date : 22/03/2026###########SONI123########################### 
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash
from datetime import timedelta
import mimetypes

mimetypes.add_type('text/css', '.css')

app = Flask(__name__)
app.secret_key = 'hrms_super_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hrms_db"
    )

@app.route('/')
def index():
    if 'hr_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'hr_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM hr_users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['hr_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'hr_id' not in session:
        return redirect(url_for('login'))
        
    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT COUNT(*) as count FROM employees')
    total = cursor.fetchone()['count']
    total_pages = (total + per_page - 1) // per_page
    
    cursor.execute('SELECT * FROM employees ORDER BY created_at DESC LIMIT %s OFFSET %s', (per_page, offset))
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', employees=employees, page=page, total_pages=total_pages)

@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if 'hr_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        designation = request.form['designation']
        salary = request.form['salary']
        date_joined = request.form['date_joined']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO employees (name, email, phone, designation, salary, date_joined)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, email, phone, designation, salary, date_joined))
            conn.commit()
            flash('Employee onboarded successfully!', 'success')
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return render_template('onboard.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'hr_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        designation = request.form['designation']
        salary = request.form['salary']
        date_joined = request.form['date_joined']
        
        try:
            cursor.execute('''
                UPDATE employees
                SET name=%s, email=%s, phone=%s, designation=%s, salary=%s, date_joined=%s
                WHERE id=%s
            ''', (name, email, phone, designation, salary, date_joined, id))
            conn.commit()
            flash('Employee details updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    cursor.execute('SELECT * FROM employees WHERE id = %s', (id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('dashboard'))
        
    return render_template('edit.html', emp=employee)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
