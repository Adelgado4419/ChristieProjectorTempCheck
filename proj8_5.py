import socket
import sqlite3
from datetime import datetime
import re
import time

# Dictionary of names and their corresponding IP addresses
hosts = {
    "Bay01_Proj1": "10.51.0.19",
    "Bay01_Proj2": "10.51.0.20",
    "Bay01_Proj3": "10.51.0.21",
    "Bay01_Proj4": "10.51.0.22",
    "Bay02_Proj1": "10.51.0.33",
    "Bay02_Proj2": "10.51.0.34",
    "Bay02_Proj3": "10.51.0.35",
    "Bay02_Proj4": "10.51.0.36",
    "Bay03_Proj1": "10.51.0.47",
    "Bay03_Proj2": "10.51.0.48",
    "Bay03_Proj3": "10.51.0.49",
    "Bay03_Proj4": "10.51.0.50",
    "Bay04_Proj1": "10.51.0.61",
    "Bay04_Proj2": "10.51.0.62",
    "Bay04_Proj3": "10.51.0.63",
    "Bay04_Proj4": "10.51.0.64",
    "Bay05_Proj1": "10.51.0.75",
    "Bay05_Proj2": "10.51.0.76",
    "Bay05_Proj3": "10.51.0.77",
    "Bay05_Proj4": "10.51.0.78",
    "Bay06_Proj1": "10.51.0.89",
    "Bay06_Proj2": "10.51.0.90",
    "Bay06_Proj3": "10.51.0.91",
    "Bay06_Proj4": "10.51.0.92",
    "Bay07_Proj1": "10.51.0.103",
    "Bay07_Proj2": "10.51.0.104",
    "Bay07_Proj3": "10.51.0.105",
    "Bay07_Proj4": "10.51.0.106",
    "Bay08_Proj1": "10.51.0.117",
    "Bay08_Proj2": "10.51.0.118",
    "Bay08_Proj3": "10.51.0.119",
    "Bay08_Proj4": "10.51.0.120",
}

PORT = 3002
DB_FILE = 'received_data.db'

def extract_temperature(data):
    """Extract temperature data from the received string."""
    match = re.search(r'"(\d+) C"', data)
    if match:
        return match.group(1)
    return None

def get_current_time():
    """Return the current time formatted as a string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def setup_database():
    """Set up the SQLite database and table."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS temperature_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_name TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            temperature_f REAL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(host_name, ip_address, temperature_f, timestamp):
    """Insert data into the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO temperature_data (host_name, ip_address, temperature_f, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (host_name, ip_address, temperature_f, timestamp))
    conn.commit()
    conn.close()

def main():
    setup_database()

    while True:
        for name, HOST in hosts.items():
            data_received = 0
            #print(f"Connecting to {name} ({HOST}) on port {PORT}...")
        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((HOST, PORT))
                    #print("Starting Connection...")
                    s.sendall(b'(SST?)')
    
                    #print("Message Sent")
                    
                    while True:
                        data = s.recv(1024)
                        if not data:
                            print("No Data, Break")
                            break

                        data_received += 1
                        
                        if data_received == 21:
                            # Get current timestamp
                            timestamp = get_current_time()
                    
                            # Convert received bytes to string
                            data_str = data.decode('utf-8', errors='ignore').strip()
                            #print(f"Received Data: {data_str}")  # Debugging line

                            temperature_number = extract_temperature(data_str)
                            #print(f"Extracted Temperature Number: {temperature_number}")  # Debugging line
                    
                            temperature_fahrenheit = None

                            if temperature_number:
                                celsius = float(temperature_number)  # Convert string to float
                                temperature_fahrenheit = celsius_to_fahrenheit(celsius)
                                temperature_fahrenheit = round(temperature_fahrenheit, 2)  # Optional: Round to 2 decimal places

                            if temperature_fahrenheit is not None:
                                print(f"{name}, {timestamp}: {temperature_fahrenheit} F")
                              
                            # Insert the data into the SQLite database
                            insert_data(name, HOST, temperature_fahrenheit if temperature_fahrenheit is not None else None, timestamp)
                            #print("Data written to database")  # Debugging line

                            s.shutdown(socket.SHUT_RDWR)
                            #print("Received Data, Close")
                            break

                except socket.error as e:
                    print(f"Socket error with {name} ({HOST}): {e}")
                except Exception as e:
                    print(f"Unexpected error with {name} ({HOST}): {e}")
        print("WAITING FOR 5 MINUTES BEFORE RETRYING...")
        time.sleep(300)
    #s.close()
    #print(f"Connection to {name} ({HOST}) closed\n")

if __name__ == "__main__":
    main()
