import time

def run(ip, port, duration, stop_event):
    end_time = time.time() + duration
    while not stop_event.is_set() and time.time() < end_time:
        print(f"[OVH-AMP] Simulando tráfico hacia {ip}:{port}")
        time.sleep(0.2)
