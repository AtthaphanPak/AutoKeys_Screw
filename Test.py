import socket
import time
from datetime import datetime

def send_and_wait_sqs_response(product_id, ip="192.168.1.20", port=51000, timeout=30, retry_delay=3):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}".ljust(128)
    already_sent_fi = False  # จะส่ง FI แค่ครั้งเดียว
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((ip, port))
                print(f"[{datetime.now()}] 🔌 Connected to SQS3")
                if not already_sent_fi:
                    s.sendall(telegram.encode())
                    print(f"[{datetime.now()}] FI telegram sent to SQS3")
                    already_sent_fi = True
                buffer = ""
                start_time = time.time()
                while True:
                    try:
                        data = s.recv(128)
                        if not data:
                            print(f"[{datetime.now()}] No data received, reconnecting...")
                            break  # ออกจาก inner loop เพื่อ reconnect ใหม่
                        response = data.decode(errors="ignore")
                        print(f"[{datetime.now()}] Received: {repr(response)}")
                        buffer += response
                        if product_id in buffer:
                            print(f"[{datetime.now()}] Product ID found in response")
                            return buffer.strip()
                    except socket.timeout:
                        print(f"[{datetime.now()}]  Waiting for response...")
                    if time.time() - start_time > timeout:
                        print(f"[{datetime.now()}] Timeout - reconnecting...")
                        break  # ออกจาก inner loop เพื่อ reconnect ใหม่
        except Exception as e:
            print(f"[{datetime.now()}] Connection error: {e}")
        # รอระหว่าง reconnect
        time.sleep(retry_delay)

result = send_and_wait_sqs_response("CIN251230000")
print(result)