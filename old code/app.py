from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = 'received_data.db'

def query_database():
    """Query the SQLite database for the last 32 records."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT host_name, ip_address, temperature_f, timestamp
        FROM temperature_data
        ORDER BY id DESC
        LIMIT 32
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

#@app.route('/data')
#def data():
#    """Endpoint to get temperature data in JSON format."""
#    rows = query_database()
#    data = [{
#        'name': row[0],
#        'host': row[1],
#        'temperature': row[2],
#        'timestamp': row[3]
#    } for row in rows]
#    return jsonify(data)

#@app.route('/data')
#def get_data():
#    conn = sqlite3.connect('data.db')
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 32")
#    rows = cursor.fetchall()
#    conn.close()
    
    # Convert rows to a list of dictionaries
#    data = [{'name': row[0], 'host': row[1], 'temperature': row[2], 'timestamp': row[3]} for row in rows]
#    return jsonify(data)

@app.route('/data')
def get_data():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM temperatures ORDER BY timestamp DESC LIMIT 32")
        rows = cursor.fetchall()
        conn.close()
        
        data = [{'name': row[0], 'host': row[1], 'temperature': row[2], 'timestamp': row[3]} for row in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
