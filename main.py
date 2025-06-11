import tkinter as tk
import pygame
import os
import random
import time
from threading import Thread
from pynput import mouse, keyboard

# Caminho da pasta com músicas
PASTA_MUSICAS = "C:/caminho/para/suas/musicas"
EXTENSOES_SUPORTADAS = ('.mp3', '.wav', '.ogg')

# Carrega a playlist
playlist = [
    os.path.join(PASTA_MUSICAS, f)
    for f in os.listdir(PASTA_MUSICAS)
    if f.lower().endswith(EXTENSOES_SUPORTADAS)
]

if not playlist:
    raise Exception("Nenhum arquivo de áudio encontrado na pasta!")

random.shuffle(playlist)
pygame.mixer.init()

current_track = 0
paused = False
volume = 0.5
pygame.mixer.music.set_volume(volume)

last_pause_click_time = 0
DOUBLE_CLICK_INTERVAL = 0.4
pressed_keys = set()

def play_music():
    global paused
    pygame.mixer.music.load(playlist[current_track])
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    paused = False

def pause_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_music()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_music()

def check_music_end():
    if not paused and not pygame.mixer.music.get_busy():
        next_track()
    root.after(1000, check_music_end)

def toggle_pause_or_next():
    global last_pause_click_time
    now = time.time()
    if now - last_pause_click_time <= DOUBLE_CLICK_INTERVAL:
        next_track()
    else:
        pause_music()
    last_pause_click_time = now

def change_volume(delta):
    global volume
    volume = min(1.0, max(0.0, volume + delta))
    pygame.mixer.music.set_volume(volume)
    print(f"Volume: {int(volume * 100)}%")

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.middle:
        toggle_pause_or_next()

def on_press(key):
    global last_pause_click_time
    try:
        if key == keyboard.Key.esc:
            if 'tab' in pressed_keys:
                print("Atalho Tab + Esc detectado. Fechando.")
                root.quit()
                return
            now = time.time()
            if now - last_pause_click_time <= DOUBLE_CLICK_INTERVAL:
                next_track()
            else:
                pause_music()
            last_pause_click_time = now
        elif key == keyboard.Key.tab:
            pressed_keys.add('tab')
        elif hasattr(key, 'char'):
            if key.char == ',' and 'tab' in pressed_keys:
                change_volume(-0.05)
            elif key.char == '.' and 'tab' in pressed_keys:
                change_volume(0.05)
    except:
        pass

def on_release(key):
    if key == keyboard.Key.tab:
        pressed_keys.discard('tab')

def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Interface gráfica Tkinter
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="gray")
root.attributes("-alpha", 0.3)

frame = tk.Frame(root, bg="gray")
frame.pack(padx=10, pady=10)

btn_prev = tk.Button(frame, text="⏮ Voltar", command=prev_track,
                     relief="flat", bd=0, highlightthickness=0,
                     bg="gray", fg="#FFFFFF", activebackground="gray")
btn_prev.pack(side=tk.LEFT, padx=10)

btn_pause = tk.Button(frame, text="⏯ Pausar", command=pause_music,
                      relief="flat", bd=0, highlightthickness=0,
                      bg="gray", fg="#FFFFFF", activebackground="gray")
btn_pause.pack(side=tk.LEFT, padx=10)

btn_next = tk.Button(frame, text="⏭ Próxima", command=next_track,
                     relief="flat", bd=0, highlightthickness=0,
                     bg="gray", fg="#FFFFFF", activebackground="gray")
btn_next.pack(side=tk.LEFT, padx=10)

play_music()
check_music_end()

Thread(target=start_mouse_listener, daemon=True).start()
Thread(target=start_keyboard_listener, daemon=True).start()

root.mainloop()
