import tkinter as tk
import pygame
import os
import random
import time
from threading import Thread
from pynput import mouse, keyboard

# Pasta onde estão as músicas (modifique para o caminho da sua pasta)
PASTA_MUSICAS = "C:/CAMINHO/DA/PASTA/DE/MUSICAS"

# Extensões de áudio suportadas pelo player
EXTENSOES_SUPORTADAS = ('.mp3', '.wav', '.ogg')

# Monta a lista de arquivos de música na pasta, filtrando pelas extensões suportadas
playlist = [
    os.path.join(PASTA_MUSICAS, f)
    for f in os.listdir(PASTA_MUSICAS)
    if f.lower().endswith(EXTENSOES_SUPORTADAS)
]

# Caso a playlist esteja vazia, interrompe com exceção
if not playlist:
    raise Exception("Nenhum arquivo de áudio encontrado na pasta!")

# Embaralha a playlist para tocar em ordem aleatória
random.shuffle(playlist)

# Inicializa o mixer do pygame para reprodução de áudio
pygame.mixer.init()

# Índice da faixa atual na playlist
current_track = 0
# Estado do player: pausado ou tocando
paused = False

# Controle de tempo para detectar duplo clique / duplo pressionamento
last_pause_click_time = 0
DOUBLE_CLICK_INTERVAL = 0.4  # intervalo em segundos para considerar duplo clique

# Controle para detectar combinação de teclas (Ctrl + Alt + Q)
pressed_keys = set()

def play_music():
    """Carrega e toca a música atual da playlist."""
    global paused
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.play()
    paused = False

def pause_music():
    """Pausa ou despausa a música dependendo do estado atual."""
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_track():
    """Avança para a próxima música na playlist (com loop)."""
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_music()

def prev_track():
    """Volta para a música anterior na playlist (com loop)."""
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_music()

def check_music_end():
    """Verifica periodicamente se a música terminou e avança para a próxima."""
    if not paused and not pygame.mixer.music.get_busy():
        next_track()
    root.after(1000, check_music_end)  # verifica a cada 1 segundo

def toggle_pause_or_next():
    """
    Alterna entre pausar/despausar ou, em caso de duplo clique rápido,
    pula para a próxima música.
    """
    global last_pause_click_time
    now = time.time()
    if now - last_pause_click_time <= DOUBLE_CLICK_INTERVAL:
        next_track()
    else:
        pause_music()
    last_pause_click_time = now

def on_click(x, y, button, pressed):
    """Listener global para clique do mouse.
    Se o botão do meio (scroll) for clicado, executa toggle_pause_or_next."""
    if pressed and button == mouse.Button.middle:
        toggle_pause_or_next()

def on_press(key):
    """
    Listener global para teclado.
    - Tecla Esc pausa/despausa ou pula música no duplo clique.
    - Detecta Ctrl + Alt + Q para fechar o app.
    """
    global last_pause_click_time
    try:
        if key == keyboard.Key.esc:
            now = time.time()
            if now - last_pause_click_time <= DOUBLE_CLICK_INTERVAL:
                next_track()
            else:
                pause_music()
            last_pause_click_time = now
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pressed_keys.add('ctrl')
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            pressed_keys.add('alt')
        elif hasattr(key, 'char') and key.char == 'q':
            pressed_keys.add('q')

        # Se todas as teclas Ctrl + Alt + Q estiverem pressionadas, fecha o app
        if {'ctrl', 'alt', 'q'}.issubset(pressed_keys):
            print("Atalho Ctrl + Alt + Q detectado. Fechando.")
            root.quit()
    except:
        pass

def on_release(key):
    """Remove a tecla do conjunto pressed_keys ao ser liberada."""
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pressed_keys.discard('ctrl')
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        pressed_keys.discard('alt')
    elif hasattr(key, 'char') and key.char == 'q':
        pressed_keys.discard('q')

def start_mouse_listener():
    """Inicia o listener global do mouse em uma thread separada."""
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_keyboard_listener():
    """Inicia o listener global do teclado em uma thread separada."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Configuração da interface gráfica Tkinter
root = tk.Tk()
root.overrideredirect(True)  # remove bordas da janela
root.attributes("-topmost", True)  # janela sempre no topo
root.configure(bg="gray")  # cor de fundo
root.attributes("-alpha", 0.3)  # transparência da janela

frame = tk.Frame(root, bg="gray")
frame.pack(padx=10, pady=10)

# Botão para voltar música
btn_prev = tk.Button(frame, text="⏮ Voltar", command=prev_track,
                     relief="flat", bd=0, highlightthickness=0,
                     bg="gray", fg="#FFFFFF", activebackground="gray")
btn_prev.pack(side=tk.LEFT, padx=10)

# Botão para pausar/despausar música
btn_pause = tk.Button(frame, text="⏯ Pausar", command=pause_music,
                      relief="flat", bd=0, highlightthickness=0,
                      bg="gray", fg="#FFFFFF", activebackground="gray")
btn_pause.pack(side=tk.LEFT, padx=10)

# Botão para próxima música
btn_next = tk.Button(frame, text="⏭ Próxima", command=next_track,
                     relief="flat", bd=0, highlightthickness=0,
                     bg="gray", fg="#FFFFFF", activebackground="gray")
btn_next.pack(side=tk.LEFT, padx=10)

# Começa a tocar música e inicia a checagem do fim da faixa
play_music()
check_music_end()

# Inicia listeners globais em threads daemon para não travar a interface
Thread(target=start_mouse_listener, daemon=True).start()
Thread(target=start_keyboard_listener, daemon=True).start()

# Loop principal da interface Tkinter
root.mainloop()
