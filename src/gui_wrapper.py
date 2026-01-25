#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import threading
import queue
import re
import runpy
import os
from tkinter import font
from resource_helper import get_script_path, get_asset_path
from simi import VERSION_ACTUAL_SIMI
from tkinterdnd2 import DND_FILES, TkinterDnD

if os.name == 'nt':
    from ctypes import windll

# Configuración de la consola
TIPOGRAFIA_TERMINAL = "Consolas" if os.name == 'nt' else "Menlo"
TAMANIO_TIPOGRAFIA = 14 if os.name == 'nt' else 14
COLOR_BG_TERMINAL = "#0c0c0c" if os.name == 'nt' else "#1e1e1e"
COLOR_FG_TERMINAL = "#cccccc" if os.name == 'nt' else "#ffffff"
COLOR_CURSOR = "#f2f2f2" if os.name == 'nt' else "#9d9d9d"

# Variables
icono_win = "icono_win.ico"

class DisplayTerminal(tk.Text):
    """
    Widget que muestra una consola donde se ejecuta el script principal.
    Muestra texto con color, limpia la pantalla y hace lectura de los inputs del usuario.
    """
    def __init__(self, master, input_queue, **kwargs):
        super().__init__(master, **kwargs)
        self.input_queue = input_queue
        self.tag_configure("default", foreground=COLOR_FG_TERMINAL)

        # Configuración de colores y estilos ANSI que usa Colorama
        self.map_color_ansi = {
            '30': '#0C0C0C', '31': '#C50F1F', '32': '#13A10E', '33': '#c19c00',
            '34': '#0037da', '35': '#881798', '36': '#3a96dd', '37': '#cccccc',
            '90': '#767676', '91': '#e74856', '92': '#16c60c', '93': '#f9f1a5',
            '94': '#3b78ff', '95': '#b4009e', '96': '#61d6d6', '97': '#f2f2f2'
        }
        for codigo, color in self.map_color_ansi.items():
            self.tag_configure(f"color-{codigo}", foreground=color)

        # Regex para buscar códigos de escape ANSI
        self.regex_escape_ansi = re.compile(r'\x1b\[((?:\d|;)*)([a-zA-Z])')
        self.tags_actuales = ("default",)

        # Define el inicio del área que el usuario puede editar (el input)
        self.mark_set("input_start", "end-1c")
        self.mark_gravity("input_start", "left")

        # Habilita input hacia la terminal
        self.bind("<KeyPress>", self._presiona_teclas)

    def arrastrar_soltar(self, event):
        """ Permite arrastrar y soltar carpetas para leer la ruta """
        # Limpia la ruta
        ruta = event.data.strip()
        if ruta.startswith('{') and ruta.endswith('}'):
            ruta = ruta[1:-1]

        # Si se arrastran varias carpetas, solo toma la primera
        primera_ruta = ruta.split('} {')[0]

        # Pone la ruta en el área del input
        self.insert("insert", primera_ruta)

    def _presiona_teclas(self, event):
        """ Lee las teclas que se tipean para simular un input de la terminal """
        # Sólo le permite al usuario tipear en el área del input
        if self.compare("insert", "<", "input_start"):
            # Si el cursor está antes del área designada, lo mueve hacia el final
            self.mark_set("insert", "end")

        if event.keysym == "Return":
            self._envia_input()
            return "break" # Evita que se inserte una nueva línea

        if event.keysym == "BackSpace":
            # Evita que se borre la línea de input
            if self.compare("insert", "==", "input_start"):
                return "break"

        # Permite copiar
        es_macos = sys.platform == "Darwin"
        tecla_copiar = 8 if es_macos else 4 # 8 es Command en Mac, 4 es Control en Windows

        if event.state & tecla_copiar and event.keysym.lower() == 'c':
            if self.tag_ranges("sel"):
                texto_seleccionado = self.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(texto_seleccionado)
            # Si no hay texto seleccionado, interrumpe el programa y lo cierra
            else:
                self.master.destroy()
            return "break" # Evita que se inserte el caracter 'c'

        return # Permite que se ingresen los caracteres para cualquier otra tecla

    def _envia_input(self):
        """Envía lo ingresado por el usuario """
        input_usuario = self.get("input_start", "end-1c")

        # Agrega una nueva línea en la consola
        self.insert("end", "\n")

        # Pone el input en cola para que el script lo lea
        self.input_queue.put(input_usuario + "\n")

        # Mueve el indicador del input al nuevo final
        self.mark_set("input_start", "end-1c")
        self.see("end") # Autoscroll

    def write(self, text):
        """
        Escribe texto a la consola y procesa los códigos ANSI
        """
        self.master.after(0, self._escribe_en_thread_principal, text)

    def _procesa_texto_plano(self, text):
        """ Procesa texto sin códigos ANSI, pero con \r"""
        # '\r' significa que debe ir al inicio de la línea y sobreescribir
        if '\r' in text:
            # Inserta la primera parte del texto normalmente
            partes = text.split('\r')
            if partes[0]:
                self.insert("insert", partes[0], self.tags_actuales)

            # Se aplica para las partes siguientes precedidas por un '\r'
            for parte in partes[1:]:
                # Mueve el cursor al inicio de la línea actual
                self.mark_set("insert", "insert linestart")
                # Borra desde el cursor hasta el final de la línea
                self.delete("insert", "insert lineend")
                # Inserta la nueva parte de texto y sobreescribe la anterior
                if parte:
                    self.insert("insert", parte, self.tags_actuales)
        else:
            # No se detectó '/r', inserta texto normalmente
            self.insert("insert", text, self.tags_actuales)

    def _escribe_en_thread_principal(self, text):
        """ Actualiza el widget con la consola """
        # Procesa texto de stdout
        last_end = 0
        for coincide in self.regex_escape_ansi.finditer(text):
            # Procesa el texto plano
            self._procesa_texto_plano(text[last_end:coincide.start()])

            # Procesa el código ANSI
            parametros = coincide.group(1)
            comando = coincide.group(2)

            if comando == 'm': # Color/Style
                if not parametros or parametros == '0':
                    self.tags_actuales = ("default",)
                else:
                    codigo_color = parametros.split(';')[-1]
                    if codigo_color in self.map_color_ansi:
                        self.tags_actuales = (f"color-{codigo_color}",)
                    else:
                        self.tags_actuales = ("default",)
            elif comando == 'J': # Borra en Display
                if parametros == '2': # Limpia toda la pantalla
                    self.delete("1.0", "end")
            elif comando == 'H': # Posición del cursor
                # Mueve el cursor a top-left
                self.mark_set("insert", "1.0")
            elif comando == 'K': # Borra en la línea
                if parametros == '' or parametros == '0': # Borra desde el cursor hasta el final de la línea
                    self.delete("insert", "insert lineend")
                elif parametros == '1': # Borra desde el inicio de la línea hasta el cursor
                    self.delete("insert linestart", "insert")
                elif parametros == '2': # Borra la línea completa
                    self.delete("insert linestart", "insert lineend")

            last_end = coincide.end()

        # Procesa el resto del texto plano luego del último código ANSI
        self._procesa_texto_plano(text[last_end:])

        # Actualiza el input y scrollea hacia el final
        self.mark_set("input_start", self.index("insert-1c"))
        self.see("insert")

    def flush(self):
        pass

class RedireccionaStdin:
    """ Lee y redirecciona stdin """
    def __init__(self, queue):
        self.queue = queue

    def readline(self):
        """ Bloquea hasta que una línea está disponible en la cola """
        return self.queue.get()

class App(TkinterDnD.Tk):
    """ Ventana principal de la GUI """
    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path
        self.title(f"Simi v{VERSION_ACTUAL_SIMI}")
        self.terminal_font = font.Font(family=TIPOGRAFIA_TERMINAL, size=TAMANIO_TIPOGRAFIA)

        if os.name == 'nt':
            # DPI aware
            try:
                windll.shcore.SetProcessDpiAwareness(1)
            
            except Exception:
                pass # DPI aware no disponible

            # Icono para Windows
            try:
                ruta_icono = get_asset_path(icono_win)
                if os.path.exists(ruta_icono):
                    self.iconbitmap(ruta_icono)
                else:
                    print(f"No se encontró el ícono en la ruta [{ruta_icono}]")
            
            except Exception as e:
                print(f"No se pudo aplicar el ícono: {e}")

            # Calcula el tamaño de la ventana de forma dinámica basado en la tipografía
            COLUMNAS = 90
            FILAS = 36

            ancho_caracter = self.terminal_font.measure('0')
            altura_linea = self.terminal_font.metrics('linespace')

            padding_total_x = 0
            ancho = (COLUMNAS * ancho_caracter) + padding_total_x
            alto = FILAS * altura_linea

            self.geometry(f"{int(ancho)}x{int(alto)}")
        else: # macOS
            self.geometry("730x580")

        self.configure(bg=COLOR_BG_TERMINAL)

        # Configura cola para redirección de stdin
        self.input_queue = queue.Queue()
        self.stdin_redirector = RedireccionaStdin(self.input_queue)

        # Crea el área de display de la terminal
        self.console = DisplayTerminal(
            self,
            self.input_queue,
            wrap=tk.WORD,
            font=self.terminal_font,
            bg=COLOR_BG_TERMINAL,
            fg=COLOR_FG_TERMINAL,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BG_TERMINAL,
            highlightcolor=COLOR_BG_TERMINAL,
            insertbackground=COLOR_CURSOR,
            selectbackground="#4C566A",
            selectforeground="#cccccc",
            padx=10,
            pady=0
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        # Registra el widget para que puedan soltarse carpetas en la ventana
        self.console.drop_target_register(DND_FILES) # type: ignore
        self.console.dnd_bind('<<Drop>>', self.console.arrastrar_soltar) # type: ignore

        self.console.focus_set()
        self.inicia_thread_script()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def inicia_thread_script(self):
        """ Redirecciona I/O e inicia un thread para el script """
        sys.stdout = self.console
        sys.stderr = self.console
        sys.stdin = self.stdin_redirector

        self.script_thread = threading.Thread(target=self.ejecuta_script, daemon=True)
        self.script_thread.start()

    def ejecuta_script(self):
        """ Ejecuta el script principal """
        try:
            if not os.path.exists(self.script_path):
                print(f"Error: no se encontró el script '{self.script_path}'\n")
                print(f"Se buscó en la ruta: [{os.path.abspath(self.script_path)}]\n")
                return

            runpy.run_path(self.script_path, run_name="__main__")
            
        except SystemExit:
            self.after(0, self.on_closing)

        except Exception as e:
            print(f"Error en el script: {e}\n")
        
        finally:
            self.console.config(state=tk.DISABLED)

    def on_closing(self):
        """ Cierra la ventana """
        self.destroy()

if __name__ == "__main__":
    EJECUTAR_SCRIPT = get_script_path('simi.py')
    app = App(script_path=EJECUTAR_SCRIPT)
    app.mainloop()
