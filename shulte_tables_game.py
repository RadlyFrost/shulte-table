import tkinter as tk # первая версия игры Таблицы Шульте
import random        # импорт библиотек (GUI, случайные числа, время)
import time

# -------------------- СОСТОЯНИЕ --------------------
GRID_SIZE = 5
EMPTY_CELLS = 0
buttons = []
numbers = []
next_number = 1
start_time = None
timer_id = None
fullscreen = False

# -------------------- ИГРА --------------------
def start_game():
    global GRID_SIZE, EMPTY_CELLS
    GRID_SIZE = int(size_var.get())
    EMPTY_CELLS = int(empty_var.get())
    settings_frame.pack_forget()
    game_frame.pack(expand=True, fill="both")
    new_game()

def new_game():
    global buttons, numbers, next_number, start_time, timer_id

    if timer_id:
        root.after_cancel(timer_id)

    start_time = None
    next_number = 1
    time_label.config(text="Время: 0.000 с")
    info_label.config(text="Нажмите числа по возрастанию.", fg="black")

    for b in buttons:
        b.destroy()
    buttons.clear()

    total_cells = GRID_SIZE * GRID_SIZE
    usable_cells = total_cells - EMPTY_CELLS

    numbers = list(range(1, usable_cells + 1))
    random.shuffle(numbers)

    # индексы пустых ячеек
    empty_indexes = set(random.sample(range(total_cells), EMPTY_CELLS))

    num_index = 0
    for i in range(GRID_SIZE):
        grid_frame.rowconfigure(i, weight=1)
        grid_frame.columnconfigure(i, weight=1)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            idx = r * GRID_SIZE + c

            if idx in empty_indexes:
                lbl = tk.Label(grid_frame, bg="#222")
                lbl.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                buttons.append(lbl)
            else:
                value = numbers[num_index]
                num_index += 1
                btn = tk.Button(
                    grid_frame,
                    text=str(value),
                    command=lambda i=len(buttons): on_click(i)
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                buttons.append(btn)

    root.after(50, resize_fonts)

def on_click(index):
    global next_number, start_time

    btn = buttons[index]
    if not isinstance(btn, tk.Button):
        return

    value = int(btn["text"])

    if value == 1 and next_number == 1:
        start_timer()

    if value == next_number:
        btn.config(state="disabled", bg="#c4f0c4")
        next_number += 1
        if next_number > len(numbers):
            stop_timer()
    else:
        flash_error(btn)

def flash_error(btn):
    old = btn["bg"]
    btn.config(bg="#f8c6c6")
    info_label.config(text=f"Ошибка! Нужно: {next_number}", fg="red")
    root.after(200, lambda: (
        btn.config(bg=old),
        info_label.config(text="Нажмите числа по возрастанию.", fg="black")
    ))

# -------------------- ТАЙМЕР --------------------
def start_timer():
    global start_time
    start_time = time.perf_counter()
    update_timer()

def update_timer():
    global timer_id
    if start_time is None:
        return
    elapsed = time.perf_counter() - start_time
    time_label.config(text=f"Время: {elapsed:.3f} с")
    timer_id = root.after(50, update_timer)

def stop_timer():
    global start_time, timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    start_time = None
    info_label.config(text="Готово!", fg="blue")

# -------------------- МАСШТАБ --------------------
def resize_fonts(event=None):
    if not buttons:
        return

    w = grid_frame.winfo_width()
    h = grid_frame.winfo_height()
    if w < 50 or h < 50:
        return

    cell = min(w, h) // GRID_SIZE
    font_size = max(12, int(cell * 0.45))
    font = ("Helvetica", font_size, "bold")

    for b in buttons:
        if isinstance(b, tk.Button):
            b.config(font=font)

# -------------------- FULLSCREEN --------------------
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)
    root.after(50, resize_fonts)

def exit_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    root.attributes("-fullscreen", False)
    root.after(50, resize_fonts)

# -------------------- UI --------------------
root = tk.Tk()
root.title("Таблица Шульте")
root.geometry("900x700")
root.bind("<Escape>", exit_fullscreen)

# ----------- НАСТРОЙКИ -----------
settings_frame = tk.Frame(root)
settings_frame.pack(expand=True)

tk.Label(settings_frame, text="Таблица Шульте", font=("Helvetica", 24, "bold")).pack(pady=20)

tk.Label(settings_frame, text="Размер таблицы (N×N):").pack()
size_var = tk.StringVar(value="5")
tk.Spinbox(settings_frame, from_=3, to=8, textvariable=size_var, width=5).pack(pady=5)

tk.Label(settings_frame, text="Удалить ячеек:").pack()
empty_var = tk.StringVar(value="0")
tk.Spinbox(settings_frame, from_=0, to=20, textvariable=empty_var, width=5).pack(pady=5)

tk.Button(settings_frame, text="Старт", font=("Helvetica", 14),
          command=start_game).pack(pady=20)

# ----------- ИГРА -----------
game_frame = tk.Frame(root)

top = tk.Frame(game_frame)
top.pack(fill="x", padx=5, pady=5)

tk.Button(top, text="Новая игра", command=new_game).pack(side="left", padx=5)
tk.Button(top, text="Полный экран", command=toggle_fullscreen).pack(side="left", padx=5)

time_label = tk.Label(top, text="Время: 0.000 с")
time_label.pack(side="left", padx=15)

info_label = tk.Label(game_frame, text="Нажмите числа по возрастанию.")
info_label.pack()

grid_frame = tk.Frame(game_frame)
grid_frame.pack(expand=True, fill="both", padx=5, pady=5)
grid_frame.bind("<Configure>", resize_fonts)

root.mainloop()
