import socket
from datetime import datetime
import time
# กำหนดค่าคงที่สำหรับ SQS Software
SQS_IP = '192.168.1.20'  
SQS_PORT = 51000      
TELEGRAM_LENGTH = 128 
def receive_and_print_signals():
    """
    ฟังก์ชันสำหรับเชื่อมต่อกับ SQS และรับสัญญาณที่เข้ามาพร้อมพิมพ์ออกในคอนโซล
    """
    client_socket = None
    is_connected = False
    while True: # วนลูปเพื่อพยายามเชื่อมต่อและรับสัญญาณตลอดเวลา
        if not is_connected:
            print(f"Attempting to connect to SQS at {SQS_IP}:{SQS_PORT}...")
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SQS_IP, SQS_PORT))
                client_socket.settimeout(None) # Make socket blocking after connection
                is_connected = True
                print("Successfully connected to SQS. Waiting for signals...")
            except ConnectionRefusedError:
                print("Connection refused. SQS Software might not be running or IP/Port is incorrect.")
                is_connected = False
            except Exception as e:
                print(f"Could not connect to SQS: {e}")
                is_connected = False
            
            if not is_connected:
                time.sleep(5) # รอก่อนลองเชื่อมต่อใหม่ หากเชื่อมต่อไม่ได้
                continue # กลับไปลองเชื่อมต่อใหม่
        # ถ้าเชื่อมต่อแล้ว ให้เริ่มรับข้อมูล
        if is_connected and client_socket:
            try:
                data = client_socket.recv(TELEGRAM_LENGTH)
                if not data:
                    print("No data received, SQS might have closed the connection. Reconnecting...")
                    is_connected = False
                    client_socket.close()
                    client_socket = None
                    continue # กลับไปพยายามเชื่อมต่อใหม่
                received_telegram = data.decode('ascii').strip()
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{now} | Received: {received_telegram}")
                # สามารถเพิ่ม logic สำหรับการตอบกลับ LB Telegram ได้ตรงนี้
                # หาก SQS ส่ง LB Telegram มาและต้องการให้คุณตอบกลับ
                telegram_type = received_telegram[32:34]
                receipt_status = int(received_telegram[36:38])
                if telegram_type == "LB" and receipt_status == 0:
                    # สร้าง LB response
                    sender = received_telegram[0:16].strip()
                    receiver = received_telegram[16:32].strip()
                    seq_num = int(received_telegram[34:36])
                    
                    # ในโค้ดตัวอย่างนี้ เราจะสร้าง LB response แบบง่ายๆ
                    # ในโปรแกรมเต็มรูปแบบ ควรใช้ generate_telegram function
                    lb_response_telegram = f"{sender.ljust(16)}{receiver.ljust(16)}LB{seq_num:02d}010000" + ' ' * (TELEGRAM_LENGTH - 42)
                    lb_response_telegram = lb_response_telegram[:TELEGRAM_LENGTH] # Ensure 128 chars
                    try:
                        client_socket.sendall(lb_response_telegram.encode('ascii'))
                        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{now} | Sent LB response: {lb_response_telegram.strip()}")
                    except Exception as e:
                        print(f"Error sending LB response: {e}")
                        is_connected = False
                        client_socket.close()
                        client_socket = None
            except ConnectionResetError:
                print("Connection was reset by SQS. Reconnecting...")
                is_connected = False
                if client_socket:
                    client_socket.close()
                client_socket = None
            except Exception as e:
                print(f"Error during data reception: {e}. Reconnecting...")
                is_connected = False
                if client_socket:
                    client_socket.close()
                client_socket = None
            
            time.sleep(0.01) # หน่วงเวลาเล็กน้อยเพื่อป้องกันการใช้ CPU สูงเกินไป
# เริ่มต้นโปรแกรม
if __name__ == "__main__":
    try:
        receive_and_print_signals()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as ex:
        print(f"An unhandled error occurred: {ex}")