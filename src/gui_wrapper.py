#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import threading
import queue
import re
import runpy
import os
import subprocess
import platform
from tkinter import font
from pathlib import Path
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
    Widget que muestra una consola donde se ejecuta el script principal
    Muestra texto con color, limpia la pantalla y lee los inputs del usuario
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

        # Configuración para rutas clickeables - tags únicos por color
        self.tag_configure("path_base", underline=False)
        self.tag_configure("path_hover", underline=True)

        for codigo, color in self.map_color_ansi.items():
            self.tag_configure(f"path-color-{codigo}", foreground=color, underline=False)
            self.tag_configure(f"path-hover-color-{codigo}", foreground=color, underline=True)

        # Diccionario para guardar las rutas asociadas a los rangos de texto
        self.rutas_registradas = {}

        # Variable para tracking de hover
        self.ruta_hover_actual = None
        self.ultimo_cursor_pos = None

        # Define cursores nativos para cada plataforma
        self.cursor_normal = "xterm"
        if platform.system() == 'Darwin': # macOS
            self.cursor_clickeable = "pointinghand"
        else: # Windows
            self.cursor_clickeable = "hand2"

        # Bind de eventos de mouse
        self.bind("<Motion>", self._on_mouse_motion)
        self.bind("<Button-1>", self._on_click)

        # Regex para buscar códigos de escape ANSI
        self.regex_escape_ansi = re.compile(r'\x1b\[((?:\d|;)*)([a-zA-Z])')
        self.tags_actuales = ("default",)

        # Patrones para detectar rutas
        if platform.system() == 'Windows':
            self.patron_ruta = re.compile(r'[A-Z]:[\\\/][^\n\r\x1b\]]+')
        else:
            self.patron_ruta = re.compile(r'/[^\n\r\x1b\]]+(?:/[^\n\r\x1b\]]+)*')

        # Define el inicio del área que el usuario puede editar (el input)
        self.mark_set("input_start", "end-1c")
        self.mark_gravity("input_start", "left")

        # Habilita input hacia la terminal
        self.bind("<KeyPress>", self._presiona_teclas)

    def _on_mouse_motion(self, event):
        """ Maneja el movimiento del mouse para hover effects """
        try:
            index = self.index(f"@{event.x},{event.y}")

            if index == self.ultimo_cursor_pos:
                return

            self.ultimo_cursor_pos = index

            # Busca si el cursor está sobre una ruta
            ruta_encontrada = None
            rango_encontrado = None

            for rango, ruta in self.rutas_registradas.items():
                start, end = rango.split('|')
                try:
                    if self.compare(index, ">=", start) and self.compare(index, "<=", end):
                        ruta_encontrada = ruta
                        rango_encontrado = rango
                        break

                except tk.TclError:
                    continue

            # Si cambió la ruta sobre la que está el cursor
            if rango_encontrado != self.ruta_hover_actual:
                # Quita el hover de la ruta anterior (todos los segmentos)
                if self.ruta_hover_actual:
                    self._quitar_hover_todos_segmentos(self.ruta_hover_actual)

                # Aplica hover a la nueva ruta (todos los segmentos)
                if rango_encontrado:
                    self._aplicar_hover_todos_segmentos(ruta_encontrada)
                    self.config(cursor=self.cursor_clickeable)
                else:
                    self.config(cursor=self.cursor_normal)

                self.ruta_hover_actual = rango_encontrado

        except tk.TclError:
            pass

    def _aplicar_hover_todos_segmentos(self, ruta):
        """ Aplica el efecto hover a todos los segmentos de una ruta """
        for rango, ruta_en_rango in self.rutas_registradas.items():
            if ruta_en_rango == ruta:
                self._aplicar_hover(rango)

    def _quitar_hover_todos_segmentos(self, rango_actual):
        """ Quita el efecto hover de todos los segmentos de una ruta """
        if rango_actual not in self.rutas_registradas:
            return

        ruta = self.rutas_registradas[rango_actual]

        for rango, ruta_en_rango in self.rutas_registradas.items():
            if ruta_en_rango == ruta:
                self._quitar_hover(rango)

    def _aplicar_hover(self, rango):
        """ Aplica el efecto hover a una ruta """
        try:
            start, end = rango.split('|')
            tags = self.tag_names(start)

            color_tag = None
            for tag in tags:
                if tag.startswith("color-"):
                    color_tag = tag.replace("color-", "")
                    break

            if color_tag:
                hover_tag = f"path-hover-color-{color_tag}"
                self.tag_add(hover_tag, start, end)
                self.tag_raise(hover_tag)
            else:
                self.tag_add("path_hover", start, end)
                self.tag_raise("path_hover")

        except tk.TclError:
            pass

    def _quitar_hover(self, rango):
        """ Quita el efecto hover de una ruta """
        try:
            start, end = rango.split('|')

            for codigo in self.map_color_ansi.keys():
                self.tag_remove(f"path-hover-color-{codigo}", start, end)
            self.tag_remove("path_hover", start, end)

        except tk.TclError:
            pass

    def _on_click(self, event):
        """ Maneja el click del mouse """
        try:
            index = self.index(f"@{event.x},{event.y}")
            if self.compare(index, ">=", "input_start"):
                return

        except tk.TclError:
            return

        if self.ruta_hover_actual and self.ruta_hover_actual in self.rutas_registradas:
            ruta = self.rutas_registradas[self.ruta_hover_actual]
            self._abrir_ruta_en_explorador(ruta)
            return "break"

    def _abrir_ruta_en_explorador(self, ruta):
        """ Abre una ruta en el explorador de archivos del sistema """
        def abrir_async():
            try:
                ruta_path = Path(ruta)

                if not ruta_path.exists():
                    return

                if ruta_path.is_file():
                    if platform.system() == 'Windows':
                        subprocess.Popen(['explorer', '/select,', str(ruta_path)])
                    elif platform.system() == 'Darwin':
                        subprocess.Popen(['open', '-R', str(ruta_path)])
                    else:
                        subprocess.Popen(['xdg-open', str(ruta_path.parent)])

                else:
                    if platform.system() == 'Windows':
                        subprocess.Popen(['explorer', str(ruta_path)])
                    elif platform.system() == 'Darwin':
                        subprocess.Popen(['open', str(ruta_path)])
                    else:
                        subprocess.Popen(['xdg-open', str(ruta_path)])

            except Exception:
                pass

        threading.Thread(target=abrir_async, daemon=True).start()

    def _detectar_rutas_wrapeadas_delayed(self):
        """ Detecta rutas wrapeadas después de un delay """
        try:
            texto_completo = self.get("1.0", "end")

            if platform.system() == 'Windows':
                patron_wrap = re.compile(r'\[([A-Z]:[^]]*?)\]', re.DOTALL)
            else:
                patron_wrap = re.compile(r'\[(/[^]]*?)\]', re.DOTALL)

            matches = list(patron_wrap.finditer(texto_completo))

            for match in matches:
                ruta_con_saltos = match.group(1)

                # Limpia saltos de línea, espacios extras Y caracteres de la caja redondeada
                ruta_limpia = re.sub(r'[│─╭╮╯╰┌┐└┘├┤┬┴┼]', '', ruta_con_saltos)
                ruta_limpia = ' '.join(ruta_limpia.split())

                if not Path(ruta_limpia).exists():
                    continue

                # Busca esta ruta en el widget
                pos_corchete = self.search('[', "1.0", "end", nocase=False)

                while pos_corchete:
                    pos_inicio = self.index(f"{pos_corchete}+1c")
                    pos_actual = pos_inicio
                    ruta_reconstruida = ""
                    pos_antes_corchete_cierre = pos_inicio
                    encontro_cierre = False

                    for _ in range(500):
                        try:
                            char = self.get(pos_actual, f"{pos_actual}+1c")

                            if char == ']':
                                encontro_cierre = True
                                break

                            if char not in '\n\r│─╭╮╯╰┌┐└┘├┤┬┴┼':
                                ruta_reconstruida += char
                                pos_antes_corchete_cierre = self.index(f"{pos_actual}+1c")

                            pos_actual = self.index(f"{pos_actual}+1c")

                        except tk.TclError:
                            break

                    ruta_reconstruida = ' '.join(ruta_reconstruida.split())

                    if encontro_cierre and ruta_reconstruida == ruta_limpia:
                        rango_key = f"{pos_inicio}|{pos_antes_corchete_cierre}"
                        if rango_key not in self.rutas_registradas:
                            self._registrar_ruta_multilinea(ruta_limpia, pos_inicio, pos_antes_corchete_cierre)
                        break

                    pos_corchete = self.search('[', self.index(f"{pos_corchete}+1c"), "end", nocase=False)

        except Exception:
            pass

    def _detectar_y_registrar_rutas(self, texto, posicion_inicio):
        """ Detecta rutas en el texto y las registra con tags clickeables """
        self._detectar_rutas_simples(texto, posicion_inicio)

        if '[' in texto and ('\\' in texto or '/' in texto):
            if hasattr(self, '_deteccion_wrap_pendiente') and self._deteccion_wrap_pendiente:
                self.after_cancel(self._deteccion_wrap_pendiente)

            self._deteccion_wrap_pendiente = self.after(100, self._detectar_rutas_wrapeadas_delayed)

    def _detectar_rutas_simples(self, texto, posicion_inicio):
        """ Detecta rutas que están en una sola línea """
        for match in self.patron_ruta.finditer(texto):
            ruta_candidata = match.group().strip()

            while ruta_candidata and ruta_candidata[-1] in '.,;:!?)]}':
                ruta_candidata = ruta_candidata[:-1]

            if not ruta_candidata:
                continue

            try:
                if not Path(ruta_candidata).exists():
                    continue

                start_offset = match.start()
                end_offset = start_offset + len(ruta_candidata)

                start_index = f"{posicion_inicio}+{start_offset}c"
                end_index = f"{posicion_inicio}+{end_offset}c"

                try:
                    self.index(start_index)
                    self.index(end_index)

                except tk.TclError:
                    continue

                self._registrar_ruta(ruta_candidata, start_index, end_index)

            except Exception:
                pass

    def _registrar_ruta_multilinea(self, ruta, pos_inicio, pos_fin):
        """ Registra una ruta que está en múltiples líneas """
        try:
            pos_inicio_norm = self.index(pos_inicio)
            pos_fin_norm = self.index(pos_fin)

            pos_actual = pos_inicio_norm
            segmento_primer_char = None
            segmento_ultimo_char = None
            segmento_texto = ""

            while self.compare(pos_actual, "<", pos_fin_norm):
                try:
                    char = self.get(pos_actual, f"{pos_actual}+1c")

                    if char in '\n\r│─╭╮╯╰┌┐└┘├┤┬┴┼':
                        if segmento_primer_char and segmento_ultimo_char and segmento_texto.strip():
                            pos_fin_segmento = self.index(f"{segmento_ultimo_char}+1c")
                            self._registrar_ruta(ruta, segmento_primer_char, pos_fin_segmento)

                        segmento_texto = ""
                        segmento_primer_char = None
                        segmento_ultimo_char = None

                    else:
                        if segmento_primer_char is None and char.strip():
                            segmento_primer_char = pos_actual

                        if char.strip():
                            segmento_ultimo_char = pos_actual

                        segmento_texto += char

                    pos_actual = self.index(f"{pos_actual}+1c")

                except tk.TclError:
                    break

            if segmento_primer_char and segmento_texto.strip():
                if segmento_ultimo_char:
                    pos_fin_segmento = self.index(f"{segmento_ultimo_char}+1c")
                    if self.compare(pos_fin_norm, "<", pos_fin_segmento):
                        pos_fin_segmento = pos_fin_norm
                else:
                    pos_fin_segmento = pos_fin_norm

                self._registrar_ruta(ruta, segmento_primer_char, pos_fin_segmento)

        except Exception:
            pass

    def _registrar_ruta(self, ruta, start_index, end_index):
        """ Registra una ruta con sus tags correspondientes """
        try:
            rango_key = f"{start_index}|{end_index}"
            self.rutas_registradas[rango_key] = ruta

            tags_en_posicion = self.tag_names(start_index)
            color_tag = None
            for tag in tags_en_posicion:
                if tag.startswith("color-"):
                    color_tag = tag.replace("color-", "")
                    break

            if color_tag:
                tag_aplicado = f"path-color-{color_tag}"
                self.tag_add(tag_aplicado, start_index, end_index)
                self.tag_raise(tag_aplicado)
            else:
                self.tag_add("path_base", start_index, end_index)

        except Exception:
            pass

    def arrastrar_soltar(self, event):
        """ Permite arrastrar y soltar carpetas dentro de la ventana """
        ruta = event.data.strip()
        if ruta.startswith('{') and ruta.endswith('}'):
            ruta = ruta[1:-1]

        primera_ruta = ruta.split('} {')[0]
        self.insert("insert", primera_ruta)

    def _presiona_teclas(self, event):
        """ Lee las teclas que se tipean para simular un input de la terminal """
        if self.compare("insert", "<", "input_start"):
            self.mark_set("insert", "end")

        if event.keysym == "Return":
            self._envia_input()
            return "break"

        if event.keysym == "BackSpace":
            if self.tag_ranges("sel"):
                sel_start = self.index("sel.first")
                if self.compare(sel_start, "<", "input_start"):
                    return "break"
            elif self.compare("insert", "==", "input_start"):
                return "break"

        if event.keysym == "Delete":
            if self.tag_ranges("sel"):
                sel_start = self.index("sel.first")
                if self.compare(sel_start, "<", "input_start"):
                    return "break"
            return

        es_macos = sys.platform == "darwin"
        tecla_copiar = 8 if es_macos else 4

        if event.state & tecla_copiar and event.keysym.lower() == 'c':
            if self.tag_ranges("sel"):
                texto_seleccionado = self.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(texto_seleccionado)
            else:
                self.master.destroy()
            return "break"

        return

    def _envia_input(self):
        """ Envía lo ingresado por el usuario """
        input_usuario = self.get("input_start", "end-1c")
        self.insert("end", "\n")
        self.input_queue.put(input_usuario + "\n")
        self.mark_set("input_start", "end-1c")
        self.see("end")

    def write(self, text):
        """ Escribe texto a la consola y procesa los códigos ANSI """
        self.master.after(0, self._escribe_en_thread_principal, text)

    def _procesa_texto_plano(self, text):
        """ Procesa texto sin códigos ANSI, pero con \r"""
        posicion_antes_insertar = self.index("insert")

        if '\r' in text:
            partes = text.split('\r')
            if partes[0]:
                self.insert("insert", partes[0], self.tags_actuales)

            for parte in partes[1:]:
                self.mark_set("insert", "insert linestart")
                self.delete("insert", "insert lineend")
                if parte:
                    self.insert("insert", parte, self.tags_actuales)
        else:
            self.insert("insert", text, self.tags_actuales)

        self._detectar_y_registrar_rutas(text, posicion_antes_insertar)

    def _escribe_en_thread_principal(self, text):
        """ Actualiza el widget que contiene la consola """
        last_end = 0
        for coincide in self.regex_escape_ansi.finditer(text):
            self._procesa_texto_plano(text[last_end:coincide.start()])

            parametros = coincide.group(1)
            comando = coincide.group(2)

            if comando == 'm':
                if not parametros or parametros == '0':
                    self.tags_actuales = ("default",)
                else:
                    codigo_color = parametros.split(';')[-1]
                    if codigo_color in self.map_color_ansi:
                        self.tags_actuales = (f"color-{codigo_color}",)
                    else:
                        self.tags_actuales = ("default",)
            elif comando == 'J':
                if parametros == '2':
                    self.delete("1.0", "end")
                    self.rutas_registradas.clear()
                    self.ruta_hover_actual = None
            elif comando == 'H':
                self.mark_set("insert", "1.0")
            elif comando == 'K':
                if parametros == '' or parametros == '0':
                    self.delete("insert", "insert lineend")
                elif parametros == '1':
                    self.delete("insert linestart", "insert")
                elif parametros == '2':
                    self.delete("insert linestart", "insert lineend")

            last_end = coincide.end()

        self._procesa_texto_plano(text[last_end:])
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
            try:
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass

            try:
                ruta_icono = get_asset_path(icono_win)
                if os.path.exists(ruta_icono):
                    self.iconbitmap(ruta_icono)
            except Exception:
                pass

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

        self.input_queue = queue.Queue()
        self.stdin_redirector = RedireccionaStdin(self.input_queue)

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
        """ Cierra la app """
        self.destroy()

if __name__ == "__main__":
    EJECUTAR_SCRIPT = get_script_path('simi.py')
    app = App(script_path=EJECUTAR_SCRIPT)
    app.mainloop()
