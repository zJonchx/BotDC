from methods.ntp import run as ntp_run

def run(ip, port, duration, stop_event):
    ntp_run(ip, port, duration, stop_event)
