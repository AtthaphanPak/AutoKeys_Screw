import socket
import time
from datetime import datetime
import re

def response_telegram(product_id="CIN251230000", ip="192.168.1.20", port=51000):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(telegram.encode())
            print("✅ FI telegram sent to SQS3")

            while True:
                now = datetime.now().strftime("%d/%m/%Y %H-%M-%S")
                try:
                    response = s.recv(128).decode().strip()
                    print(now, "\t📥 Response from SQS3:", response)
                except socket.timeout:
                    return None
    except Exception as e:
        print(e)
        return e

def send_fi_telegram(product_id, ip="192.168.1.20", port=51000, retries=3):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)
    # print(telegram)

    for attempt in range(1, retries +1):
        print(f"Attempt {attempt}/{retries}")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, port))
                s.settimeout(None)

                s.sendall(telegram.encode())
                print("✅ FI telegram sent to SQS3")

                response = s.recv(128).decode().strip()
                print("📥 Response from SQS3:", response)
                return response
        except socket.timeout:
            print("Timeout occurred, retrying... ")
        except Exception as e:
            print("Can't connect SQS")
            print(e)
        time.sleep(1)

    return False

def response_telegram(product_id="CIN251230000", ip="192.168.1.20", port=51000):
    prefix = "PC STATION      PLC             "
    telegram_type = "FI0100"
    header = "0012"
    telegram = f"{prefix}{telegram_type}{header}{product_id}"
    telegram = telegram.ljust(128)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(telegram.encode())
        print("✅ FI telegram sent to SQS3")

        while True:
            try:
                response = s.recv(128).decode().strip()
                print("📥 Response from SQS3:", response)
                matche = re.search(r'(LB\d{2}0)', response)
                # if "LB" in response.upper():
                #     print("completed")
                #     return response
                if matche:
                    prefix = "PLC             PC STATION      "
                    LB = matche.group(1)
                    telegram = f"{prefix}{LB}10000"
                    telegram = telegram.ljust(128)
                    print("📥 Sent from PLC: ",telegram)
                    s.sendall(telegram.encode())
                # FE01010000
                matche = re.search(r'(FE\d{2}0)', response)
                if matche:
                    prefix = "PLC             PC STATION      "  
                    FE = matche.group(1)
                    print()
                    telegram = f"{prefix}{FE}10000"
                    telegram = telegram.ljust(128)
                    print("📥 Sent from PLC: ",telegram)
                    s.sendall(telegram.encode())                  

            except socket.timeout:
                print("timeout")

# CIN251230000
# result = send_fi_telegram("CIN251700000")
# print(result)