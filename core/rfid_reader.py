import threading
import serial
import requests

PORT = "COM7"
BAUDRATE = 9600
API_URL = "http://127.0.0.1:8000/api/uid/"  # Django endpoint

LAST_UID = None

def set_last_uid(uid):
    global LAST_UID
    LAST_UID = uid

def get_last_uid():
    return LAST_UID

def read_rfid():
    try:
        ser = serial.Serial(PORT, BAUDRATE)
        print(f"✅ RFID reader started on {PORT}")
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line.startswith("UID:"):
                uid = line.replace("UID:", "").strip()
                print(f"📡 Card scanned: UID:{uid}")

                # отправляем POST на Django
                try:
                    requests.post(API_URL, json={"uid": uid}, timeout=1)
                except Exception as e:
                    print(f"⚠️ POST error: {e}")

    except Exception as e:
        print("RFID error:", e)

def start_reader():
    t = threading.Thread(target=read_rfid, daemon=True)
    t.start()
