#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import csv

# Path to the CSV file where data is stored
CSV_FILE = 'received_data.csv'
NUM_RECENT_RECORDS = 32

def read_csv():
    """Read the CSV file and return the last NUM_RECENT_RECORDS entries as a list of dictionaries."""
    data = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # Read all rows into a list
            data = rows[-NUM_RECENT_RECORDS:]  # Get the last NUM_RECENT_RECORDS rows
    except FileNotFoundError:
        # File does not exist yet, return an empty list
        pass
    return data

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            # Serve JSON data
            data = read_csv()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            # Serve the HTML file
            super().do_GET()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
