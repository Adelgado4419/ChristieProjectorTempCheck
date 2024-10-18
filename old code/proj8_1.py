import socket

# List of IP addresses to parse through

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
                data_received += 1

                if not data:
                    print("No Data, Break")
                    break
                
                if data_received == 21:
                    print(f"{name}: {data}")
                    s.shutdown(socket.SHUT_RDWR)
                    #print("Received Data, Close")
                    break
        
        except socket.error as e:
            print(f"Socket error with {name} ({HOST}): {e}")
        except Exception as e:
            print(f"Unexpected error with {name} ({HOST}): {e}")

    s.close()
    #print(f"Connection to {name} ({HOST}) closed\n")
        


