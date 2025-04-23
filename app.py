import itertools
from collections import deque

import matplotlib.pyplot as plt
import psutil
from matplotlib.animation import FuncAnimation

# Parâmetros
WINDOW_SIZE = 60     # histórico de 60s
INTERVAL = 1000      # atualização a cada 1s

# Estruturas de dados
x_data = deque(maxlen=WINDOW_SIZE)
cpu_data = deque(maxlen=WINDOW_SIZE)
mem_pct_data = deque(maxlen=WINDOW_SIZE)

# Estilo moderno
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10,6))
ax.set_title('Uso de CPU e Memória em Tempo Real', pad=20)
ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Uso (%)')
ax.set_ylim(0, 100)
ax.set_xlim(0, WINDOW_SIZE-1)
ax.grid(alpha=0.3)

# Linhas e legendas
cpu_line, = ax.plot([], [], label='CPU %',   linewidth=2, marker='o', markersize=4, color='#1FDA9A')
mem_line, = ax.plot([], [], label='Memória %',linewidth=2, marker='o', markersize=4, color='#F24C4C')
ax.legend(loc='upper right')

# Textos dos valores
cpu_text    = ax.text(0.02, 0.95, '', transform=ax.transAxes)
mem_pct_text= ax.text(0.02, 0.90, '', transform=ax.transAxes)
mem_gb_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)
freq_text   = ax.text(0.02, 0.80, '', transform=ax.transAxes)
cores_text  = ax.text(0.02, 0.75, '', transform=ax.transAxes)

# Init
def init():
    for obj in (cpu_line, mem_line, cpu_text, mem_pct_text, mem_gb_text, freq_text, cores_text):
        obj.set_text('') if hasattr(obj, 'set_text') else obj.set_data([], [])
    return cpu_line, mem_line, cpu_text, mem_pct_text, mem_gb_text, freq_text, cores_text

# Contador de tempo
time_counter = itertools.count(0, 1)

# Update
def update(_):
    t = next(time_counter)
    # CPU e memória
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    mem_pct = mem.percent
    mem_gb = mem.used / (1024**3)
    # Frequência e núcleos
    freq_ghz = psutil.cpu_freq().current / 1000
    cores   = psutil.cpu_count(logical=True)

    # Guardar histórico
    x_data.append(t)
    cpu_data.append(cpu)
    mem_pct_data.append(mem_pct)

    # Janela rolante
    xmin = max(0, t - WINDOW_SIZE + 1)
    ax.set_xlim(xmin, xmin + WINDOW_SIZE - 1)

    # Atualiza linhas
    cpu_line.set_data(list(x_data), list(cpu_data))
    mem_line.set_data(list(x_data), list(mem_pct_data))

    # Atualiza textos
    cpu_text.set_text(f'CPU: {cpu:.1f}%')
    mem_pct_text.set_text(f'Memória: {mem_pct:.1f}%')
    mem_gb_text.set_text(f'RAM usada: {mem_gb:.2f} GB')
    freq_text.set_text(f'Freq CPU: {freq_ghz:.2f} GHz')
    cores_text.set_text(f'Núcleos: {cores}')

    return cpu_line, mem_line, cpu_text, mem_pct_text, mem_gb_text, freq_text, cores_text

# Animação
ani = FuncAnimation(fig, update, init_func=init,
                    interval=INTERVAL, blit=True)

plt.tight_layout()
plt.show()
