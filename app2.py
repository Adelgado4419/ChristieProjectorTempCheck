from flask import Flask, send_from_directory, jsonify
import sqlite3

app = Flask(__name__, static_folder='static', static_url_path='')

def get_db_connection():
    conn = sqlite3.connect(received_data.db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = sqlite3.connect('received_data.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM temperature_data ORDER BY timestamp DESC LIMIT 32")
        rows = cursor.fetchall()
        conn.close()
        
        data = [{'host_name': row[1], 'ip_address': row[2], 'temperature_f': row[3], 'timestamp': row[4]} for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
