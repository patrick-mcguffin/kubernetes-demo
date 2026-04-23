from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'database-service'),
        database=os.environ.get('DB_NAME', 'appdb'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn

@app.route('/status')
def status():
    return jsonify({
        'status': 'ok',
        'message': 'Backend is running'
    })

@app.route('/db')
def db_status():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            ' status': 'ok',
            'message': 'Database connection successful'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
