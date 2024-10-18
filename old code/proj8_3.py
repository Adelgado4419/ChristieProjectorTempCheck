#!/usr/bin/env python3

import socket
import csv
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

def main():
    """Main function to run the temperature data retrieval and logging."""
    # Open a CSV file for appending
    with open('received_data.csv', mode='r+', newline='') as file:
        writer = csv.writer(file)

        # Write the header row only if the file is empty
        file.seek(0)
        if not file.read(1):
            writer.writerow(['Host Name', 'IP Address', 'Temperature (F)', 'Timestamp'])

        while True:
            for name, host in hosts.items():
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(10)  # Set a timeout for the socket connection
                        s.connect((host, PORT))
                        s.sendall(b'(SST?)')

                        data = s.recv(1024)
                        if not data:
                            print(f"No data received from {name} ({host})")
                            continue

                        # Convert received bytes to string
                        data_str = data.decode('utf-8', errors='ignore').strip()

                        temperature_number = extract_temperature(data_str)
                        temperature_fahrenheit = None

                        if temperature_number:
                            celsius = float(temperature_number)
                            temperature_fahrenheit = round(celsius_to_fahrenheit(celsius), 2)

                        timestamp = get_current_time()
                        print(f"{name}, {timestamp}: {temperature_fahrenheit if temperature_fahrenheit is not None else 'No Data'} F")

                        # Write the data to the CSV file
                        writer.writerow([name, host, temperature_fahrenheit if temperature_fahrenheit is not None else '', timestamp])

                except socket.error as e:
                    print(f"Socket error with {name} ({host}): {e}")
                except Exception as e:
                    print(f"Unexpected error with {name} ({host}): {e}")

            # Wait for 5 minutes before the next iteration
            print("Waiting for 5 minutes before retrying...")
            time.sleep(300)

if __name__ == "__main__":
    main()
