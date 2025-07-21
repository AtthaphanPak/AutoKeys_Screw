import socket
import time
import re

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

def inital_telegram(ip="192.168.1.20", port=51000):
    prefix = "PC STATION      PLC             "

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        while True:
            try:
                response = s.recv(128).decode().strip()
                print("📥 Response from SQS3:", response)

                match_LB = re.search(r'(LB\d{2}0)', response)
                if match_LB:
                    LB = match_LB.group(1)
                    telegram = f"{prefix}{LB}10000"
                    telegram = telegram.ljust(128)
                    print("📥 Sent from PLC: ",telegram)
                    s.sendall(telegram.encode())

                # FE01010000
                match_FE = re.search(r'(FE\d{2}0)', response)
                if match_FE:
                    FE = match_FE.group(1)
                    telegram = f"{prefix}{FE}10000"
                    telegram = telegram.ljust(128)
                    print("📥 Sent from PLC: ",telegram)
                    s.sendall(telegram.encode())

            except socket.timeout:
                print("timeout")

def Check_result_telegram(product_id, ip="192.168.1.20", port=51000):
    print("Check_result_telegram")
    prefix = "PC STATION      PLC             "

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        while True:
            try:
                response = s.recv(128).decode().strip()
                print(response)

                match_LB = re.search(r'(LB\d{2}0)', response)
                if match_LB:
                    LB = match_LB.group(1)
                    telegram = f"{prefix}{LB}10000"
                    telegram = telegram.ljust(128)
                    print(telegram)
                    s.sendall(telegram.encode())

                match_FE = re.search(fr'(FE\d{{2}}00\d{{4}}{product_id}XXXX(00|01))', response)
                if match_FE:
                    FE = match_FE.group(1)
                    telegram = f"{prefix}{FE[:5]}10000"
                    telegram = telegram.ljust(128)
                    print(telegram)
                    s.sendall(telegram.encode())
                    return True

            except socket.timeout:
                print("timeout")

# serial = "CIN251230066"
# inital_telegram()
# send_fi_telegram(serial)
# Check_result_telegram(serial)