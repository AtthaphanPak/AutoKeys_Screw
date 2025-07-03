import socket
import tkinter as tk
from tkinter import simpledialog
from Sources.fitsdll import fn_Handshake

def send_fi_telegram(ip="192.168.1.20", port=51000):
    root = tk.Tk()
    root.withdraw()
    while True:
        product_id = simpledialog.askstring("Scan Product ID", "Please scan product ID")
        status_handshake = fn_Handshake("*", "IN230", product_id)
        if status_handshake == True:
            break
        else: 
            print(status_handshake)

    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)
    print(telegram)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(telegram.encode())
        print("✅ FI telegram sent to SQS3")
        response = s.recv(128).decode().strip()
        print("📥 Response from SQS3:", response)

# CIN251230000
send_fi_telegram()