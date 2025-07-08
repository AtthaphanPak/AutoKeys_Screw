import socket
import time

def response_telegram(product_id="CIN251230000", ip="192.168.1.20", port=51000):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.timeout(5)
            s.connect((ip, port))
            s.sendall(telegram.encode())
            print("✅ FI telegram sent to SQS3")

            while True:
                try:
                    response = s.recv(128).decode().strip()
                    print("📥 Response from SQS3:", response)
                    if "DONE" in response.upper():
                        print("completed")
                        return response
                except socket.timeout:
                    pass
    except Exception as e:
        print(e)
        return e

def send_fi_telegram(product_id, ip="192.168.1.20", port=51000):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)
    # print(telegram)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(telegram.encode())
        print("✅ FI telegram sent to SQS3")
        response = s.recv(128).decode().strip()
        print("📥 Response from SQS3:", response)
    return

# CIN251230000
result = response_telegram("CIN251230000")
print(result)