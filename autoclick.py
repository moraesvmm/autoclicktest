import tkinter as tk
from tkinter import ttk
from threading import Thread
import keyboard
import ctypes
import time
import pyautogui

class AutoClickerApp:
    def __init__(self, master):
        self.master = master
        master.title("Swift Click")

        self.style = ttk.Style()

        # Configuração do tema escuro
        self.master.configure(bg='#292929')  # Cor de fundo da janela principal

        self.style.theme_use('clam')
        self.style.configure('.', background='#292929', foreground='#FFF')  # Configuração de cor de fundo e texto para todos os elementos
        self.style.configure('TButton', font=('calibri', 12, 'bold'), foreground='white', background='#A020F0',
                             borderwidth=0, focuscolor='#800080', focusthickness=0, padding=10, relief='flat')
        self.style.map('TButton', background=[('active', '#800080')])  # Cor de fundo do botão quando pressionado

        self.click_type = tk.StringVar(value="Double Click")  # Variável para armazenar o tipo de clique

        self.click_type_label = ttk.Label(master, text="Click Type:", background='#292929', foreground='#FFF')
        self.click_type_label.pack(pady=5)

        self.click_type_combobox = ttk.Combobox(master, textvariable=self.click_type, values=["Single Click", "Double Click"], state="readonly")
        self.click_type_combobox.pack(pady=5)

        # Configurando cores para o novo widget
        self.click_type_combobox.config(background='#A020F0', foreground='white')

        self.start_button = ttk.Button(master, text="Start", command=self.start_clicker)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_clicker)
        self.stop_button.pack(pady=5)

        self.choose_key_button = ttk.Button(master, text="Choose Key", command=self.choose_key)
        self.choose_key_button.pack(pady=5)

        self.status_label = ttk.Label(master, text="Status: Stopped")
        self.status_label.pack(pady=10)

        self.clicking = False
        self.click_thread = None
        self.click_position = None

        self.auto_click_speed = 0.5  # Velocidade do autoclick em segundos
        self.stop_key = 'p'  # Tecla padrão para interromper o autoclick

        # Configuração do botão para definir a posição de clique
        self.set_click_position_button = ttk.Button(master, text="Set Click Position", command=self.set_click_position)
        self.set_click_position_button.pack(pady=5)

        # Configuração do evento de teclado para interromper o autoclick globalmente
        keyboard.on_press(self.check_stop_key)

        # Define o ícone do aplicativo na barra de tarefas
        set_app_icon(master)

        # Adiciona a mensagem de direitos reservados
        self.add_copyright_message(master)

    def add_copyright_message(self, parent):
        copyright_label = ttk.Label(parent, text="© 2024 Vitor Moraes. Todos os direitos reservados.", 
                                     foreground='#FFF', background='#292929', font=('calibri', 8))
        copyright_label.pack(side="bottom", anchor="se", padx=10, pady=10)

    def start_clicker(self):
        # Espera para o usuário posicionar o cursor
        self.status_label.config(text="Status: Position the cursor and press 'Set Click Position' button")
        self.master.update()

    def set_click_position(self):
        # Aguarda 10 segundos para a posição do cursor ser definida
        time.sleep(10)
        self.click_position = pyautogui.position()
        self.status_label.config(text="Status: Click position set")
        self.clicking = True
        self.click_thread = Thread(target=self.run_clicker)
        self.click_thread.start()

    def stop_clicker(self, event=None):
        self.clicking = False
        self.status_label.config(text="Status: Stopped")

    def run_clicker(self):
        while self.clicking:
            if self.click_position:
                click_func = pyautogui.click if self.click_type.get() == "Single Click" else pyautogui.doubleClick
                print(f"{self.click_type.get()} at position:", self.click_position)
                click_func(self.click_position[0], self.click_position[1])
            time.sleep(self.auto_click_speed)

    def choose_key(self):
        key_selection_window = KeySelectionWindow(self.master, self)
        key_selection_window.show()

    def check_stop_key(self, event):
        if event.name.lower() == self.stop_key:
            self.master.after(0, self.stop_clicker)

class KeySelectionWindow:
    def __init__(self, master, auto_clicker_app):
        self.master = master
        self.auto_clicker_app = auto_clicker_app

        self.window = tk.Toplevel(master)
        self.window.title("Choose Key")
        self.window.geometry("300x100")

        self.label = ttk.Label(self.window, text="Press a key to set it as the stop key")
        self.label.pack(pady=5)

        # Configuração do evento de teclado para selecionar a tecla de parada
        keyboard.on_press(self.set_stop_key)

    def set_stop_key(self, event):
        self.auto_clicker_app.stop_key = event.name.lower()
        self.auto_clicker_app.status_label.config(text=f"Stop Key: {event.name.upper()}")
        self.window.destroy()

    def show(self):
        self.window.wait_window()

def set_app_icon(window):
    # Carrega o arquivo .ico
    icon_path = "rato.ico"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    window.iconbitmap(default=icon_path)

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
