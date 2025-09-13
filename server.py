import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Richumysql',
    'database': 'register'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except mysql.connector.Error as err:
        return jsonify({'message': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except mysql.connector.Error as err:
        return jsonify({'message': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/testdb')
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return 'Database connection successful!', 200
    except Exception as e:
        return f'Database connection failed: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)

{
  "username": "yourname",
  "email": "your@email.com",
  "password": "yourpassword"
}