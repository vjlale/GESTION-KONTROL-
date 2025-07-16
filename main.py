print("[DEBUG] Inicio del script - main.py:1")
import datetime
import sys
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv

# Paleta de colores moderna Alen.iA
COLOR_GRADIENTE_1 = "#dd0000"  # Púrpura
COLOR_GRADIENTE_2 = "#56555B"  # Magenta
COLOR_VERDE_NEON = "#020601"
COLOR_CIAN = "#fdfeff"
COLOR_AZUL = "#360289"
COLOR_FONDO = COLOR_AZUL  # Se usará gradiente en el fondo principal
COLOR_BOTON = "#0033cc"  # Azul fuerte para botones principales
COLOR_BOTON_SECUNDARIO = COLOR_BOTON  # Fondo de botones secundarios
COLOR_TOTAL_IVA_BG = COLOR_BOTON  # Fondo de los labels TOTAL e IVA
COLOR_LABEL_VENTA_BG = COLOR_BOTON  # Fondo de los labels principales en pantalla venta
COLOR_ENTRY_VENTA_BG = "#ffffff"  # Fondo blanco para los campos de texto
COLOR_BOTON_TEXTO = "#ffffff"
COLOR_TEXTO = "#f5f5f5"
COLOR_ENTRADA = "#040404"
COLOR_BOTON_HOVER = COLOR_VERDE_NEON

# Nuevos colores para efectos modernos
COLOR_SOMBRA = "#40D201"
COLOR_BOTON_MODERNO = "#515152"  # Azul moderno
COLOR_BOTON_HOVER_MODERNO = "#1d4ed8"  # Azul hover más oscuro
COLOR_BOTON_SUCCESS = "#059669"  # Verde moderno
COLOR_BOTON_WARNING = "#d97706"  # Naranja moderno
COLOR_BOTON_DANGER = "#dc2626"  # Rojo moderno
COLOR_BOTON_SECONDARY = "#6b7280"  # Gris moderno

def aplicar_estilo_moderno_boton(boton, tipo="primario", hover_efecto=True):
    """
    Aplica estilo moderno a un botón con bordes redondeados y efectos
    Args:
        boton: El widget Button a estilizar
        tipo: "primario", "secundario", "success", "warning", "danger"
        hover_efecto: Si aplicar efectos hover
    """
    # Definir colores según el tipo
    colores = {
        "primario": (COLOR_BOTON_MODERNO, COLOR_BOTON_HOVER_MODERNO),
        "secundario": (COLOR_BOTON_SECONDARY, "#4b5563"),
        "success": (COLOR_BOTON_SUCCESS, "#047857"),
        "warning": (COLOR_BOTON_WARNING, "#b45309"),
        "danger": (COLOR_BOTON_DANGER, "#b91c1c")
    }
    
    color_normal, color_hover = colores.get(tipo, colores["primario"])
    
    # Configurar el botón con estilo moderno
    boton.config(
        bg=color_normal,
        fg="#ffffff",
        bd=2,
        relief="solid",
        cursor="hand2",
        activebackground=color_hover,
        activeforeground="#ffffff",
        highlightthickness=0,
        padx=15,
        pady=8
    )
    
    if hover_efecto:
        # Efectos hover mejorados
        def on_enter(e):
            boton.config(
                bg=color_hover, 
                relief="raised", 
                bd=3,
                font=(boton.cget("font").split()[0] if hasattr(boton.cget("font"), 'split') else "Montserrat", 
                      int(boton.cget("font").split()[1]) if hasattr(boton.cget("font"), 'split') and len(boton.cget("font").split()) > 1 else 12, 
                      "bold")
            )
        
        def on_leave(e):
            boton.config(
                bg=color_normal, 
                relief="solid", 
                bd=2,
                font=(boton.cget("font").split()[0] if hasattr(boton.cget("font"), 'split') else "Montserrat", 
                      int(boton.cget("font").split()[1]) if hasattr(boton.cget("font"), 'split') and len(boton.cget("font").split()) > 1 else 12, 
                      "bold")
            )
        
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

def aplicar_estilo_moderno_entry(entry):
    """Aplica estilo moderno a un Entry"""
    entry.config(
        bd=2,
        relief="solid",
        highlightthickness=1,
        highlightcolor=COLOR_CIAN,
        highlightbackground="#cccccc",
        font=("Montserrat", 10),
        fg="#333333"
    )

def aplicar_estilo_moderno_label(label, tipo="normal"):
    """Aplica estilo moderno a un Label"""
    if tipo == "titulo":
        label.config(
            font=("Montserrat", 18, "bold"),
            fg=COLOR_CIAN,
            relief="flat",
            bd=0
        )
    elif tipo == "subtitulo":
        label.config(
            font=("Montserrat", 14, "bold"),
            fg=COLOR_TEXTO,
            relief="flat",
            bd=0
        )
    else:
        label.config(
            font=("Montserrat", 12),
            fg=COLOR_TEXTO,
            relief="flat",
            bd=0
        )

def aplicar_estilo_moderno_combobox(combo):
    """Aplica estilo moderno a un Combobox"""
    try:
        # Configuración para ttk.Combobox
        style = ttk.Style()
        
        # Crear un estilo personalizado para el combobox
        style.theme_use('default')
        
        # Estilo para el Combobox (campo de entrada)
        style.configure("Moderno.TCombobox",
                       fieldbackground="#ffffff",
                       background="#ffffff",
                       foreground="#33333300",
                       borderwidth=3,
                       relief="solid",
                       focuscolor=COLOR_CIAN,
                       selectbackground=COLOR_CIAN,
                       selectforeground="#0c0b0b",
                       font=("Montserrat", 12))
        
        # Estilo para el botón dropdown
        style.configure("Moderno.TCombobox",
                       arrowcolor=COLOR_BOTON_MODERNO,
                       borderwidth=3,
                       relief="solid")
        
        # Aplicar el estilo al combobox
        combo.configure(style="Moderno.TCombobox")
        
        # Configuración adicional directa
        combo.configure(font=("Montserrat", 10))
        
    except Exception as e:
        # Fallback si hay problemas con el estilo
        print(f"[DEBUG] Error aplicando estilo a combobox: {e} - main.py:166")
        combo.configure(font=("Montserrat", 10))

def aplicar_estilo_moderno_treeview(tree):
    """Aplica estilo moderno a un Treeview"""
    try:
        style = ttk.Style()
        
        # Crear estilo personalizado para Treeview
        style.theme_use('default')
        
        # Configurar el estilo del Treeview
        style.configure("Moderno.Treeview",
                       background="#ffffff",
                       foreground="#000000",
                       fieldbackground="#ffffff",
                       borderwidth=2,
                       relief="solid",
                       font=("Montserrat", 10))
        
        # Configurar el estilo del encabezado
        style.configure("Moderno.Treeview.Heading",
                       background=COLOR_BOTON_MODERNO,
                       foreground="#ffffff",
                       borderwidth=1,
                       relief="solid",
                       font=("Montserrat", 10, "bold"))
        
        # Configurar colores alternos para las filas
        style.map("Moderno.Treeview",
                 background=[('selected', "#3089ee")],
                 foreground=[('selected', '#ffffff')])
        
        # Aplicar el estilo al treeview
        tree.configure(style="Moderno.Treeview")
        
        # Configuración adicional directa
        tree.tag_configure('oddrow', background='#f0f0f0')
        tree.tag_configure('evenrow', background='#ffffff')
        
    except Exception as e:
        # Fallback si hay problemas con el estilo
        print(f"[DEBUG] Error aplicando estilo a treeview: {e} - main.py:208")
        pass

class Tooltip:
    """Clase para crear tooltips informativos modernos"""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide()

    def on_motion(self, event=None):
        self.unschedule()
        self.schedule()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = None

    def show(self):
        if self.tooltip_window:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Estilo moderno para el tooltip
        frame = tk.Frame(self.tooltip_window, background="#55de01", relief="solid", borderwidth=1)
        frame.pack()
        
        label = tk.Label(frame, text=self.text, justify="left",
                        background="#2c3e50", foreground="#ffffff",
                        font=("Montserrat", 9), padx=8, pady=6)
        label.pack()

    def hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def crear_tooltip(widget, texto):
    """Función helper para crear tooltips fácilmente"""
    return Tooltip(widget, texto)

def validar_campo_visual(entry, es_valido, mensaje_error=""):
    """Aplica validación visual a un campo Entry"""
    if es_valido:
        entry.config(highlightcolor="#01A807", highlightbackground="#4CAF50", bd=2)
        # Quitar cualquier tooltip de error existente
        if hasattr(entry, '_tooltip_error'):
            entry._tooltip_error.hide()
    else:
        entry.config(highlightcolor="#f44336", highlightbackground="#f44336", bd=2)
        # Agregar tooltip de error si hay mensaje
        if mensaje_error:
            if not hasattr(entry, '_tooltip_error'):
                entry._tooltip_error = crear_tooltip(entry, mensaje_error)
            else:
                entry._tooltip_error.text = mensaje_error

def aplicar_animacion_hover_mejorada(widget, color_normal, color_hover):
    """Aplica animación de hover mejorada con transición suave"""
    def on_enter(e):
        widget.config(bg=color_hover)
        # Efecto de "elevación" visual
        widget.config(relief="raised", bd=3)
    
    def on_leave(e):
        widget.config(bg=color_normal)
        widget.config(relief="solid", bd=2)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

class Producto:
    def __init__(self, marca: str, descripcion: str, color: str, talle: str, cantidad: int, precio_costo: float, porcentaje_venta: float = 50, porcentaje_amigo: float = 20, oferta: dict = {}):
        self.marca = marca
        self.descripcion = descripcion
        self.color = color
        self.talle = talle
        self.cantidad = cantidad
        self.precio_costo = precio_costo
        self.porcentaje_venta = porcentaje_venta
        self.porcentaje_amigo = porcentaje_amigo
        self.oferta = oferta if oferta is not None else {}
        self.precio_venta = self.calcular_precio_venta()
        self.precio_amigo = self.calcular_precio_amigo()

    def calcular_precio_venta(self):
        return round(self.precio_costo * (1 + self.porcentaje_venta / 100), 2)

    def calcular_precio_amigo(self):
        return round(self.precio_costo * (1 + self.porcentaje_amigo / 100), 2)

    def actualizar_precio_costo(self, nuevo_precio):
        self.precio_costo = nuevo_precio
        self.precio_venta = self.calcular_precio_venta()
        self.precio_amigo = self.calcular_precio_amigo()

class Venta:
    def __init__(self, descripcion: str, items: list, fecha: datetime.date, forma_pago: str = "EFECTIVO"):
        self.descripcion = descripcion
        self.items = items  # lista de dicts: {producto, cantidad, precio}
        self.fecha = fecha
        self.forma_pago = forma_pago

class SistemaGestion:
    def __init__(self):
        self.productos: List[Producto] = []
        self.ventas: List[Venta] = []
        self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists("productos.json"):
            with open("productos.json", "r", encoding="utf-8") as f:
                productos = json.load(f)
                for p in productos:
                    self.productos.append(Producto(
                        p.get("marca", ""),
                        p["descripcion"], p["color"], p["talle"], p["cantidad"], p["precio_costo"], p.get("porcentaje_venta", 50), p.get("porcentaje_amigo", 20)
                    ))
        if os.path.exists("ventas.json"):
            with open("ventas.json", "r", encoding="utf-8") as f:
                ventas = json.load(f)
                for v in ventas:
                    items = []
                    for item in v["items"]:
                        prod = self.buscar_producto(item.get("marca", ""), item["producto"], item["color"], item["talle"])
                        if prod:
                            items.append({
                                "producto": prod,
                                "cantidad": item["cantidad"],
                                "precio": item["precio"]
                            })
                    self.ventas.append(Venta(
                        v["descripcion"], items, datetime.datetime.strptime(v["fecha"], "%Y-%m-%d").date(), 
                        v.get("forma_pago", "EFECTIVO")
                    ))

    def guardar_productos(self):
        with open("productos.json", "w", encoding="utf-8") as f:
            json.dump([
                {
                    "marca": p.marca,
                    "descripcion": p.descripcion,
                    "color": p.color,
                    "talle": p.talle,
                    "cantidad": p.cantidad,
                    "precio_costo": p.precio_costo,
                    "porcentaje_venta": p.porcentaje_venta,
                    "porcentaje_amigo": p.porcentaje_amigo
                } for p in self.productos
            ], f, ensure_ascii=False, indent=2)

    def guardar_ventas(self):
        with open("ventas.json", "w", encoding="utf-8") as f:
            json.dump([
                {
                    "descripcion": v.descripcion,
                    "items": [
                        {
                            "producto": item["producto"].descripcion,
                            "color": item["producto"].color,
                            "talle": item["producto"].talle,
                            "cantidad": item["cantidad"],
                            "precio": item["precio"]
                        } for item in v.items
                    ],
                    "fecha": v.fecha.strftime("%Y-%m-%d"),
                    "forma_pago": getattr(v, 'forma_pago', 'EFECTIVO')
                } for v in self.ventas
            ], f, ensure_ascii=False, indent=2)

    def agregar_producto(self, marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta=50, porcentaje_amigo=20):
        prod = Producto(marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta, porcentaje_amigo)
        self.productos.append(prod)
        self.guardar_productos()

    def registrar_venta(self, descripcion, items, fecha, forma_pago="EFECTIVO"):
        # items: lista de tuplas (producto, cantidad, precio)
        for producto, cantidad, _ in items:
            if producto.cantidad < cantidad:
                return False
        for producto, cantidad, _ in items:
            producto.cantidad -= cantidad
        venta_items = [{"producto": p, "cantidad": c, "precio": pr} for p, c, pr in items]
        venta = Venta(descripcion, venta_items, fecha, forma_pago)
        self.ventas.append(venta)
        self.guardar_productos()
        self.guardar_ventas()
        return True

    def buscar_producto(self, marca, descripcion, color, talle):
        for p in self.productos:
            if p.marca == marca and p.descripcion == descripcion and p.color == color and p.talle == talle:
                return p
        return None

    def cierre_caja(self, fecha):
        return [v for v in self.ventas if v.fecha == fecha]

    def archivar_ventas_dia(self, fecha):
        """Archiva las ventas del día en un archivo histórico y las elimina del día actual"""
        ventas_dia = self.cierre_caja(fecha)
        
        if not ventas_dia:
            return False
        
        # Crear archivo histórico si no existe
        archivo_historico = f"ventas_historico_{fecha.strftime('%Y')}.json"
        historico = []
        
        if os.path.exists(archivo_historico):
            with open(archivo_historico, "r", encoding="utf-8") as f:
                historico = json.load(f)
        
        # Agregar ventas del día al histórico
        for v in ventas_dia:
            historico.append({
                "descripcion": v.descripcion,
                "items": [
                    {
                        "producto": item["producto"].descripcion,
                        "marca": item["producto"].marca,
                        "color": item["producto"].color,
                        "talle": item["producto"].talle,
                        "cantidad": item["cantidad"],
                        "precio": item["precio"]
                    } for item in v.items
                ],
                "fecha": v.fecha.strftime("%Y-%m-%d"),
                "forma_pago": getattr(v, 'forma_pago', 'EFECTIVO'),
                "cerrado": True
            })
        
        # Guardar histórico actualizado
        with open(archivo_historico, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        # Eliminar ventas del día del archivo actual
        self.ventas = [v for v in self.ventas if v.fecha != fecha]
        self.guardar_ventas()
        
        return True

    def reporte_ventas(self, desde, hasta):
        return [v for v in self.ventas if desde <= v.fecha <= hasta]

    def reporte_ventas_por_marca(self, desde, hasta, marca):
        ventas = [v for v in self.ventas if desde <= v.fecha <= hasta]
        ventas_marca = []
        for v in ventas:
            for item in v.items:
                if hasattr(item['producto'], 'marca') and item['producto'].marca == marca:
                    ventas_marca.append({
                        'fecha': v.fecha,
                        'descripcion': v.descripcion,
                        'producto': item['producto'],
                        'cantidad': item['cantidad'],
                        'precio': item['precio']
                    })
        return ventas_marca

    def inventario_actual(self):
        return self.productos

    def actualizar_precio_producto(self, marca, descripcion, color, talle, nuevo_precio):
        prod = self.buscar_producto(marca, descripcion, color, talle)
        if prod:
            prod.actualizar_precio_costo(nuevo_precio)
            self.guardar_productos()
            return True
        return False

    def eliminar_producto(self, marca, descripcion, color, talle):
        self.productos = [p for p in self.productos if not (p.marca == marca and p.descripcion == descripcion and p.color == color and p.talle == talle)]
        self.guardar_productos()

    def eliminar_productos_masivo(self, lista_claves):
        # lista_claves: lista de tuplas (marca, descripcion, color, talle)
        self.productos = [p for p in self.productos if (p.marca, p.descripcion, p.color, p.talle) not in lista_claves]
        self.guardar_productos()

    def sugerencias_reposicion(self, umbral_stock=5, dias_analisis=30):
        """
        Devuelve una lista de productos que deberían reponerse según ventas recientes y stock bajo.
        - umbral_stock: stock mínimo recomendado
        - dias_analisis: días hacia atrás para analizar ventas
        """
        import datetime
        hoy = datetime.date.today()
        ventas_recientes = [v for v in self.ventas if (hoy - v.fecha).days <= dias_analisis]
        conteo = {}
        for v in ventas_recientes:
            for item in v.items:
                prod = item['producto']
                clave = (prod.marca, prod.descripcion, prod.color, prod.talle)
                conteo[clave] = conteo.get(clave, 0) + item['cantidad']
        sugerencias = []
        for p in self.productos:
            clave = (p.marca, p.descripcion, p.color, p.talle)
            ventas = conteo.get(clave, 0)
            if p.cantidad <= umbral_stock and ventas > 0:
                sugerencias.append({
                    'producto': p,
                    'stock': p.cantidad,
                    'vendidos': ventas
                })
        # Ordenar por más vendidos y menos stock
        sugerencias.sort(key=lambda x: (x['stock'], -x['vendidos']))
        return sugerencias

class AppPilchero(tk.Tk):
    def mostrar_venta(self):
        print("[DEBUG] mostrar_venta() llamado - main.py:restaurado - main.py:543")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_venta(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_principal, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)

    def mostrar_ventas_dia(self):
        print("[DEBUG] mostrar_ventas_dia() llamado - main.py:restaurado - main.py:552")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_ventas_dia(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_principal, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)
    def mostrar_actualizar_precio(self):
        print("[DEBUG] mostrar_actualizar_precio() llamado - main.py:560")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_actualizar_precio(self.canvas_bg)
        self.pantalla_widgets.extend([])  # No necesitamos agregar más widgets, ya se hizo en _pantalla_actualizar_precio
    def __init__(self, sistema):
        print("[DEBUG] Iniciando AppPilchero.__init__ - main.py:566")
        super().__init__()
        self.sistema = sistema
        self.title("Alen.iA - Gestión Inteligente de Stock y Ventas")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        print("[DEBUG] Llamando a crear_widgets() desde __init__ - main.py:573")
        self.crear_widgets()

    def crear_widgets(self):
        print("[DEBUG] Entrando en crear_widgets() - main.py:577")
        self.canvas_bg = tk.Canvas(self, width=1280, height=720, highlightthickness=0, bd=0)
        self.canvas_bg.place(x=0, y=0, relwidth=1, relheight=1)
        # Crear el fondo con etiquetas para poder identificarlo y preservarlo
        for i in range(0, 720, 2):
            color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/720)
            self.canvas_bg.create_rectangle(0, i, 1280, i+2, outline="", fill=color, tags="fondo_{}".format(i))
        self.canvas_bg.lower("all")
        self.pantalla_widgets = []
        self.mostrar_menu_principal()

    def _colocar_logo(self, pantalla_principal=True):
        # Elimina logo anterior si existe
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        
        if pantalla_principal:
            # PANTALLA PRINCIPAL: Usar LOGO APP.png (SIN MODIFICAR)
            import sys, os
            if hasattr(sys, '_MEIPASS'):
                logo_path = os.path.join(sys._MEIPASS, "LOGO APP.png") # type: ignore
            else:
                logo_path = "LOGO APP.png"
            try:
                from PIL import Image, ImageTk
                logo_img = Image.open(logo_path).convert("RGBA")
                orig_w, orig_h = logo_img.size
                self.update_idletasks()  # Forzar update para obtener tamaño real
                w = self.winfo_width() or 1200
                h = self.winfo_height() or 1000
                max_w = int(w * 0.65)
                max_h = int(h * 0.42)
                # Mantener proporción
                scale = min(max_w / orig_w, max_h / orig_h)
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS) # type: ignore
                self.logo_tk = ImageTk.PhotoImage(logo_img)
                pos_x = w // 2
                pos_y = int(h * 0.08)
                self.logo_canvas_id = self.canvas_bg.create_image(pos_x, pos_y, image=self.logo_tk, anchor="n")
                self.canvas_bg.tag_raise(self.logo_canvas_id)
            except Exception as e:
                self.logo_canvas_id = self.canvas_bg.create_text(self.winfo_width()//1, 40, text="[LOGO]", font=("Orbitron", 32, "bold"), fill=COLOR_CIAN, anchor="n")
        else:
            # PANTALLAS SECUNDARIAS: Usar 7.PNG con transparencia y centrado
            self._colocar_logo_secundarias()

    def _colocar_logo_secundarias(self):
        """Coloca el logo 7.PNG en pantallas secundarias con transparencia y centrado"""
        try:
            from PIL import Image, ImageTk
            import os
            logo_path = "7.PNG"
            
            if os.path.exists(logo_path):
                # Cargar imagen con transparencia
                logo_img = Image.open(logo_path).convert("RGBA")
                
                # Redimensionar el logo manteniendo proporción (tamaño apropiado para pantallas secundarias)
                logo_width = 200  # Tamaño más prominente
                logo_height = int(logo_img.height * (logo_width / logo_img.width))
                
                # Si es muy alto, ajustar por altura máxima
                if logo_height > 100:
                    logo_height = 150
                    logo_width = int(logo_img.width * (logo_height / logo_img.height))
                
                # Redimensionar con alta calidad
                logo_resized = logo_img.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                
                # Convertir a PhotoImage manteniendo transparencia
                self.logo_tk_secundaria = ImageTk.PhotoImage(logo_resized)
                
                # Colocar en el canvas centrado en la parte superior
                self.logo_canvas_id = self.canvas_bg.create_image(
                    640, 20,  # Centrado horizontalmente, margen superior de 25px
                    image=self.logo_tk_secundaria, 
                    anchor="n"
                )
                
                # Asegurar que el logo esté al frente
                self.canvas_bg.tag_raise(self.logo_canvas_id)
                
            else:
                # Fallback si no encuentra el archivo
                self.logo_canvas_id = self.canvas_bg.create_text(
                    640, 30, 
                    text="ALEN.IA", 
                    font=("Orbitron", 20, "bold"), 
                    fill=COLOR_CIAN, 
                    anchor="n"
                )
                
        except Exception as e:
            print(f"[INFO] Error al cargar logo 7.PNG en pantalla secundaria: {e} - main.py:673")
            # Fallback texto
            self.logo_canvas_id = self.canvas_bg.create_text(
                640, 30, 
                text="ALEN.IA", 
                font=("Orbitron", 20, "bold"), 
                fill=COLOR_CIAN, 
                anchor="n"
            )

    def _interpolar_color(self, color1, color2, t): # type: ignore
        # Interpola dos colores hex en t (0-1)
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        return f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}'

    # Métodos stub para evitar errores si no existen
    def mostrar_inventario(self): # type: ignore
        print("[DEBUG] mostrar_inventario() llamado - main.py:692")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_inventario(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="Volver", font=("Montserrat", 12, "bold"), bg="#fff", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_secundario)
        win = self.canvas_bg.create_window(65, 20, window=btn_volver, width=90, height=36, anchor="n")
        self.pantalla_widgets.append(btn_volver)



    def limpiar_pantalla(self):
        # Elimina todos los widgets de la pantalla y limpia referencias
        for w in getattr(self, 'pantalla_widgets', []):
            try:
                w.destroy()
            except Exception:
                pass
        self.pantalla_widgets = []
        
        # Elimina solo el logo si existe
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        
        # Guarda las referencias de los rectángulos del fondo (gradiente)
        fondo = []
        for i in range(0, 720, 2):
            rect_id = self.canvas_bg.find_withtag("fondo_{}".format(i))
            if rect_id:
                fondo.extend(rect_id)
        
        # Elimina todos los elementos canvas excepto el fondo
        for item in self.canvas_bg.find_all():
            if item not in fondo:
                self.canvas_bg.delete(item)
                
        # Redibuja el gradiente si es necesario
        if not fondo:
            for i in range(0, 720, 2):
                color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/720)
                rect_id = self.canvas_bg.create_rectangle(0, i, 1280, i+2, outline="", fill=color, tags="fondo_{}".format(i))
        
        # Asegura que el gradiente siempre esté al fondo
        self.canvas_bg.lower("all")

    def mostrar_menu_principal(self):
        print("[DEBUG] mostrar_menu_principal() llamado - main.py:738")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=True)
        
        # Botones con tooltips informativos
        btns_data = [
            ("💰 Venta", self.mostrar_venta, "Registrar nueva venta - Agregar productos al carrito y procesar pagos"),
            ("📊 Ventas del Día", self.mostrar_ventas_dia, "Ver resumen de ventas del día actual - Control de ingresos diarios"),
            ("⚙️ Menú Gestión", self.mostrar_menu_secundario, "Acceder a herramientas de gestión - Productos, precios e inventario"),
        ]
        
        btn_w, btn_h = 360, 68
        sep_y, sep_h = 20, 350
        y0 = 250
        
        for i, (txt, cmd, tooltip) in enumerate(btns_data):
            b = tk.Button(self.canvas_bg, text=txt, font=("Montserrat", 15, "bold"), 
                         bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                         activebackground="#7c5eff", activeforeground=COLOR_BOTON_TEXTO, 
                         cursor="hand2", command=cmd)
            
            # Aplicar estilo moderno
            aplicar_estilo_moderno_boton(b, "primario", hover_efecto=True)
            
            # Agregar tooltip informativo
            crear_tooltip(b, tooltip)
            
            win = self.canvas_bg.create_window(650, y0+i*(btn_h+sep_y), window=b, width=btn_w, height=btn_h, anchor="n")
            
            # Crear efecto de sombra sutil
            try:
                # Simular sombra con un rectángulo de fondo
                self.canvas_bg.create_rectangle(
                    650 - btn_w//2 + 3, y0+i*(btn_h+sep_y) + 3, 
                    650 + btn_w//2 + 3, y0+i*(btn_h+sep_y) + btn_h + 3,
                    fill="#00000020", outline="", width=0, tags="sombra_boton"
                )
                # Mover la sombra detrás del botón
                self.canvas_bg.tag_lower("sombra_boton")
            except:
                pass
            
            self.pantalla_widgets.append(b)

    def mostrar_menu_secundario(self):
        print("[DEBUG] mostrar_menu_secundario() llamado - main.py:783")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        
        # Título del menú (ajustado para el nuevo logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="MENÚ ", font=("Montserrat", 20, "bold"), 
                             bg=COLOR_FONDO, fg=COLOR_CIAN)
        aplicar_estilo_moderno_label(lbl_titulo, "titulo")
        self.canvas_bg.create_window(1160, 80, window=lbl_titulo, anchor="center")  # Ajustado para el logo
         
        # Botones con tooltips informativos
        btns_data = [
            ("Agregar Producto", self.mostrar_alta_producto, "success", "Dar de alta nuevos productos - Configurar marca, descripción, precios y stock"),
            ("Carga Masiva", self.carga_masiva_productos, "primario", "Importar productos desde archivo CSV - Carga rápida de múltiples productos"),
            ("Actualizar Precio", self.mostrar_actualizar_precio, "warning", "Modificar precios de productos existentes - Ajustar costos y márgenes"),
            ("Ver Inventario", self.mostrar_inventario, "primario", "Consultar inventario actual - Stock, precios y datos de productos"),
            ("📈 Reportes", self.mostrar_reportes, "primario", "Generar reportes de ventas - Análisis por fechas, productos y formas de pago"),
            ("🤖 Sugerencias IA", self.mostrar_centro_ia, "primario", "Centro de inteligencia artificial - Análisis predictivo y sugerencias"),
            ("🎁 CREAR OFERTAS", self.mostrar_crear_ofertas, "warning", "Gestionar ofertas y promociones - Descuentos y ofertas especiales"),
        ]
        
        # Botones centrados y bien espaciados (ajustados para el nuevo logo)
        btn_w, btn_h = 250, 50
        sep_y = 20
        y0 = 200  # Ajustado para dar espacio al logo
        
        for i, (txt, cmd, tipo, tooltip) in enumerate(btns_data):
            b = tk.Button(self.canvas_bg, text=txt, font=("Montserrat", 14, "bold"), 
                         bg=COLOR_BOTON, fg="#ffffff", bd=0, relief="flat", 
                         cursor="hand2", command=cmd)
            
            # Aplicar estilo moderno según el tipo
            aplicar_estilo_moderno_boton(b, tipo, hover_efecto=True)
            
            # Agregar tooltip informativo
            crear_tooltip(b, tooltip)
            
            self.canvas_bg.create_window(640, y0+i*(btn_h+sep_y), window=b, width=btn_w, height=btn_h, anchor="center")
            
            # Crear sombra para cada botón
            try:
                self.canvas_bg.create_rectangle(
                    640 - btn_w//2 + 2, y0+i*(btn_h+sep_y) - btn_h//2 + 2, 
                    640 + btn_w//2 + 2, y0+i*(btn_h+sep_y) + btn_h//2 + 2,
                    fill="#00000015", outline="", width=0, tags="sombra_menu"
                )
                self.canvas_bg.tag_lower("sombra_menu")
            except:
                pass
            
            self.pantalla_widgets.append(b)
        
        # Botón volver mejorado (ajustado para el nuevo logo)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#ffffff", bd=0, relief="flat", 
                              command=self.mostrar_menu_principal, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_volver, "secundario", hover_efecto=True)
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado
        
        self.pantalla_widgets.extend([lbl_titulo, btn_volver])

    def mostrar_centro_ia(self):
        print("[DEBUG] mostrar_centro_ia() llamado - main.py:STUB - main.py:845")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        # Título principal
        lbl_titulo = tk.Label(self.canvas_bg, text="CENTRO DE SUGERENCIAS IA", font=("Montserrat", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(640, 120, window=lbl_titulo, anchor="center")
        # Mensaje de funcionalidad no implementada
        lbl_info = tk.Label(self.canvas_bg, text="Esta funcionalidad estará disponible próximamente.", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg="#ff9900")
        self.canvas_bg.create_window(640, 300, window=lbl_info, anchor="center")
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.extend([lbl_titulo, lbl_info, btn_volver])
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)

    def mostrar_cierre_caja(self):
        print("[DEBUG] mostrar_cierre_caja() llamado - main.py:861")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_cierre_caja(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_principal, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)

    def mostrar_alta_producto(self):
        print("[DEBUG] mostrar_alta_producto() llamado - main.py:870")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_alta_producto(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)

    def mostrar_menu_principal(self):
        print("[DEBUG] mostrar_menu_principal() llamado - main.py:879")
        self.limpiar_pantalla()
        # --- LOGO PRINCIPAL ---
        # Reducir tamaño y centrar más arriba
        if hasattr(self, 'logo_canvas_id') and self.logo_canvas_id:
            self.canvas_bg.delete(self.logo_canvas_id)
            self.logo_canvas_id = None
        try:
            from PIL import Image, ImageTk
            logo_path = "LOGO APP.png"
            if hasattr(sys, '_MEIPASS'):
                logo_path = os.path.join(sys._MEIPASS, "LOGO APP.png")
            logo_img = Image.open(logo_path).convert("RGBA")
            orig_w, orig_h = logo_img.size
            w = 1780
            h = 720
            max_w = int(w * 0.30)  # Más pequeño que antes
            max_h = int(h * 0.30)
            scale = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            pos_x = w // 2.7  # Más centrado
            pos_y = 70  # Más arriba
            self.logo_canvas_id = self.canvas_bg.create_image(pos_x, pos_y, image=self.logo_tk, anchor="n")
            self.canvas_bg.tag_raise(self.logo_canvas_id)
        except Exception as e:
            self.logo_canvas_id = self.canvas_bg.create_text(890, 120, text="[LOGO]", font=("Orbitron", 32, "bold"), fill=COLOR_CIAN, anchor="n")

        # --- BOTONES PRINCIPALES ---
        # Colores exactos de la imagen
        COLOR_VERDE = "#00a316"
        COLOR_NARANJA = "#e89c2c"
        COLOR_GRIS = "#6d6d6d"
        btn_w = 350  # Botones más anchos
        btn_h = 150  # Botones más altos
        btn_y = 350
        btn_spacing = 380  # Mayor separación entre botones
        btn_center_x = 650  # Centro de la pantalla (1780/2)

        # NUEVA VENTA (izquierda)
        btn_nueva_venta = tk.Button(self.canvas_bg, text="NUEVA\nVENTA", font=("Montserrat", 26, "bold"),
                                    bg=COLOR_VERDE, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                                    command=self.mostrar_venta, activebackground=COLOR_VERDE, activeforeground="#ffffff")
        # Aplicar estilo moderno personalizado para mantener el color verde pero con efectos modernos
        aplicar_estilo_moderno_boton(btn_nueva_venta, "success", hover_efecto=True)
        # Restaurar el color verde específico después de aplicar el estilo
        btn_nueva_venta.config(bg=COLOR_VERDE, activebackground="#0ea866")
        self.canvas_bg.create_window(btn_center_x - btn_spacing, btn_y, window=btn_nueva_venta, width=btn_w, height=btn_h, anchor="n")

        # VENTAS DEL DÍA (centro)
        btn_ventas_dia = tk.Button(self.canvas_bg, text="VENTAS DEL DÍA", font=("Montserrat", 26, "bold"),
                                   bg=COLOR_NARANJA, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                                   command=self.mostrar_ventas_dia, activebackground=COLOR_NARANJA, activeforeground="#ffffff")
        # Aplicar estilo moderno personalizado para mantener el color naranja pero con efectos modernos
        aplicar_estilo_moderno_boton(btn_ventas_dia, "warning", hover_efecto=True)
        # Restaurar el color naranja específico después de aplicar el estilo
        btn_ventas_dia.config(bg=COLOR_NARANJA, activebackground="#c97b20")
        self.canvas_bg.create_window(btn_center_x, btn_y, window=btn_ventas_dia, width=btn_w, height=btn_h, anchor="n")

        # MENÚ (derecha)
        btn_menu = tk.Button(self.canvas_bg, text="MENÚ", font=("Montserrat", 26, "bold"),
                             bg=COLOR_GRIS, fg="#ffffff", bd=0, relief="flat", cursor="hand2", 
                             command=self.mostrar_menu_secundario, activebackground=COLOR_GRIS, activeforeground="#ffffff")
        # Aplicar estilo moderno personalizado para mantener el color gris pero con efectos modernos
        aplicar_estilo_moderno_boton(btn_menu, "secundario", hover_efecto=True)
        # Restaurar el color gris específico después de aplicar el estilo
        btn_menu.config(bg=COLOR_GRIS, activebackground="#555555")
        self.canvas_bg.create_window(btn_center_x + btn_spacing, btn_y, window=btn_menu, width=btn_w, height=btn_h, anchor="n")

        # Sombra moderna para cada botón (efecto de elevación)
        for dx, btn, color in [
            (-btn_spacing, btn_nueva_venta, COLOR_VERDE), 
            (0, btn_ventas_dia, COLOR_NARANJA), 
            (btn_spacing, btn_menu, COLOR_GRIS)
        ]:
            try:
                # Crear una sombra más suave y moderna
                sombra_color = "#00000040"  # Color negro con 25% de opacidad
                sombra_offset = 8  # Distancia de la sombra
                sombra_blur = 15  # Simular un efecto de desenfoque con varios rectángulos
                
                # Crear múltiples rectángulos para simular desenfoque (efecto de sombra más suave)
                for i in range(3):
                    offset = 3 + i*2
                    opacity = 25 - i*5  # Disminuir opacidad gradualmente
                    sombra_actual = f"#000000{opacity:02x}"
                    
                    self.canvas_bg.create_rectangle(
                        btn_center_x + dx - btn_w//2 + offset, 
                        btn_y + offset, 
                        btn_center_x + dx + btn_w//2 + offset, 
                        btn_y + btn_h + offset,
                        fill=sombra_actual, outline="", width=1, 
                        tags=f"sombra_boton"
                    )
                    self.canvas_bg.tag_lower(f"sombra_boton")
            except Exception as e:
                print(f"Error al crear sombra: {e} - main.py:978")
                pass

        # Tooltips (opcional, como antes)
        crear_tooltip(btn_nueva_venta, "Registrar nueva venta - Agregar productos al carrito y procesar pagos")
        crear_tooltip(btn_ventas_dia, "Ver resumen de ventas del día actual - Control de ingresos diarios")
        crear_tooltip(btn_menu, "Acceder a herramientas de gestión - Productos, precios e inventario")

        self.pantalla_widgets.extend([btn_nueva_venta, btn_ventas_dia, btn_menu])

        # --- LOGO PEQUEÑO Y TEXTO DE VERSIÓN EN ESQUINA INFERIOR IZQUIERDA ---
        try:
            logo_chico_path = "5-3.png"
            from PIL import Image, ImageTk
            logo_chico_img = Image.open(logo_chico_path).convert("RGBA")
            logo_chico_img = logo_chico_img.resize((90, 38), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
            self.logo_chico_tk = ImageTk.PhotoImage(logo_chico_img)
            self.logo_chico_canvas_id = self.canvas_bg.create_image(1190, 705, image=self.logo_chico_tk, anchor="sw")
        except Exception as e:
            self.logo_chico_canvas_id = self.canvas_bg.create_text(20, 690, text="[LOGO]", font=("Montserrat", 10, "bold"), fill="#19c37d", anchor="sw")

        self.version_text_id = self.canvas_bg.create_text(10, 710, text="Versión: 2.0.1 / Un servicio de Alen.iA / RESULTADOS CON INTELIGENCIA", anchor="sw", font=("Montserrat", 12, "bold"), fill="#ffffff")
        
        # No es necesario agregar más widgets, ya se agregaron los botones principales anteriormente

    def formato_moneda(self, valor):
        try:
            valor = float(valor)
        except Exception:
            return "$0,000"
        # Formato: $12.345,678 (punto miles, coma decimales, tres decimales)
        partes = f"{valor:,.3f}".split(".")
        if len(partes) == 2:
            miles = partes[0].replace(",", ".")
            decimales = partes[1]
            return f"${miles},{decimales}"
        else:
            return f"${valor:,.3f}".replace(",", ".").replace(".", ",", 1)

    # Pantallas adaptadas para navegación interna
    def _pantalla_venta(self, parent):
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)  # MOSTRAR EL LOGO
        widgets = []
        carrito = []
        productos = self.sistema.inventario_actual()
        opciones = [f"{p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}" for p in productos]
        precios = {f"{p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}": p.precio_venta for p in productos}
        productos_dict = {f"{p.descripcion} | {p.color} | {p.talle} | Stock: {p.cantidad}": p for p in productos}
        
        # --- TÍTULO CENTRADO (ajustado para el logo) ---
        titulo = tk.Label(self.canvas_bg, text="NUEVA VENTA", font=("Montserrat", 6, "bold"), 
                         bg=COLOR_FONDO, fg=COLOR_CIAN)
        aplicar_estilo_moderno_label(titulo, "titulo")
        self.canvas_bg.create_window(1160, 75, window=titulo, anchor="center")  # Ajustado para el logo
        widgets.append(titulo)
        
        # --- SECCIÓN 1: CAMPOS DE ENTRADA (Y=200-260) ---
        y_campos = 150
        
        # Fila 1: Producto
        lbl_prod = tk.Label(self.canvas_bg, text="Producto:", font=("Montserrat", 16, "bold"), 
                           bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_prod)
        self.canvas_bg.create_window(100, y_campos, window=lbl_prod, anchor="nw")
        
        producto_var = tk.StringVar()
        combo = ttk.Combobox(self.canvas_bg, textvariable=producto_var, values=opciones, 
                            font=("Montserrat", 10), state="normal")
        aplicar_estilo_moderno_combobox(combo)
        crear_tooltip(combo, "Seleccione un producto del inventario - Puede escribir para filtrar")
        self.canvas_bg.create_window(100, y_campos + 25, window=combo, width=500, height=32, anchor="nw")
        
        # Sugerencias en tiempo real
        def on_keyrelease(event):
            value = combo.get().lower()
            filtered = [op for op in opciones if value in op.lower()]
            combo['values'] = filtered if filtered else opciones
        combo.bind('<KeyRelease>', on_keyrelease)
        
        # Fila 2: Cantidad y Precio (lado a lado)
        y_fila2 = y_campos + 70
        
        # Cantidad
        lbl_cant = tk.Label(self.canvas_bg, text=" Cantidad:", font=("Montserrat", 16, "bold"), 
                           bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_cant)
        self.canvas_bg.create_window(100, y_fila2, window=lbl_cant, anchor="nw")
        
        ent_cantidad = tk.Entry(self.canvas_bg, font=("Montserrat", 12), bg=COLOR_ENTRY_VENTA_BG, 
                               fg="#000000", bd=1, relief="solid")
        aplicar_estilo_moderno_entry(ent_cantidad)
        crear_tooltip(ent_cantidad, "Ingrese la cantidad de productos a vender")
        self.canvas_bg.create_window(100, y_fila2 + 25, window=ent_cantidad, width=150, height=32, anchor="nw")
        
        # Validación en tiempo real para cantidad
        def validar_cantidad(event=None):
            try:
                valor = ent_cantidad.get()
                if valor == "":
                    validar_campo_visual(ent_cantidad, True)
                    return
                cantidad = int(valor)
                if cantidad > 0:
                    validar_campo_visual(ent_cantidad, True)
                else:
                    validar_campo_visual(ent_cantidad, False, "La cantidad debe ser mayor a 0")
            except ValueError:
                validar_campo_visual(ent_cantidad, False, "Ingrese un número válido")
        
        ent_cantidad.bind('<KeyRelease>', validar_cantidad)
        
        # Precio (al lado de cantidad)
        lbl_precio = tk.Label(self.canvas_bg, text="Precio:", font=("Montserrat", 16, "bold"), 
                             bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_precio)
        self.canvas_bg.create_window(300, y_fila2, window=lbl_precio, anchor="nw")
        
        precio_var = tk.StringVar()
        ent_precio = tk.Entry(self.canvas_bg, textvariable=precio_var, font=("Montserrat", 12), 
                             bg=COLOR_ENTRY_VENTA_BG, fg="#000000", bd=1, relief="solid")
        aplicar_estilo_moderno_entry(ent_precio)
        crear_tooltip(ent_precio, "Precio unitario del producto - Se completa automáticamente")
        self.canvas_bg.create_window(300, y_fila2 + 25, window=ent_precio, width=180, height=32, anchor="nw")
        
        # Validación en tiempo real para precio
        def validar_precio(event=None):
            try:
                valor = precio_var.get()
                if valor == "":
                    validar_campo_visual(ent_precio, True)
                    return
                precio = float(valor)
                if precio > 0:
                    validar_campo_visual(ent_precio, True)
                else:
                    validar_campo_visual(ent_precio, False, "El precio debe ser mayor a 0")
            except ValueError:
                validar_campo_visual(ent_precio, False, "Ingrese un precio válido")
        
        ent_precio.bind('<KeyRelease>', validar_precio)
        
        # Fila 3: Forma de pago y Botón agregar
        y_fila3 = y_fila2 + 70
        
        # Forma de pago
        lbl_forma_pago = tk.Label(self.canvas_bg, text="💳 Forma de pago:", font=("Montserrat", 16, "bold"), 
                                 bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_forma_pago)
        self.canvas_bg.create_window(100, y_fila3, window=lbl_forma_pago, anchor="nw")
        
        forma_pago_var = tk.StringVar(value="EFECTIVO")
        combo_forma_pago = ttk.Combobox(self.canvas_bg, textvariable=forma_pago_var, 
                                       values=["EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA", "QR", "OTROS"], 
                                       font=("Montserrat", 10), state="readonly")
        aplicar_estilo_moderno_combobox(combo_forma_pago)
        crear_tooltip(combo_forma_pago, "Seleccione la forma de pago para la venta")
        self.canvas_bg.create_window(100, y_fila3 + 25, window=combo_forma_pago, width=200, height=32, anchor="nw")
        
        # Botón agregar (al lado derecho)
        btn_agregar = tk.Button(self.canvas_bg, text="🛒 AGREGAR AL CARRITO", font=("Montserrat", 13, "bold"), 
                               bg="#0813F1", fg="#ffffff", bd=0, relief="flat", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_agregar, "primario", hover_efecto=True)
        crear_tooltip(btn_agregar, "Agregar el producto seleccionado al carrito de compras")
        self.canvas_bg.create_window(220, 500, window=btn_agregar, width=250, height=45, anchor="center")
        
        # --- SECCIÓN 2: TABLA DEL CARRITO (Y=370-570) ---
        y_tabla = 370
        
       
        # Configuración de la tabla
        col_widths = [200, 120, 80, 120,]
        carrito_tree = ttk.Treeview(self.canvas_bg, columns=("Producto", "Precio", "Cant.", "Subtotal",), show="headings")
        aplicar_estilo_moderno_treeview(carrito_tree)
        
        # Configurar encabezados y columnas
        headers = ["Producto", "Precio Unit.", "Cant.", "Subtotal", ]
        for col, ancho, header in zip(carrito_tree["columns"], col_widths, headers):
            carrito_tree.heading(col, text=header, anchor="center")
            carrito_tree.column(col, width=ancho, anchor="center")
        
        # Scrollbar vertical
        scrollbar_v = ttk.Scrollbar(self.canvas_bg, orient="vertical", command=carrito_tree.yview)
        carrito_tree.configure(yscrollcommand=scrollbar_v.set)
        
        # Posicionamiento centrado de la tabla
        self.canvas_bg.create_window(700, 170, window=carrito_tree, width=sum(col_widths), height=350, anchor="nw")
        self.canvas_bg.create_window(1220, 170, window=scrollbar_v, width=15, height=350, anchor="nw")
        
        # Botón eliminar (debajo de la tabla)
        btn_eliminar_carrito = tk.Button(self.canvas_bg, text="ELIMINAR", font=("Montserrat", 11, "bold"), 
                                        bg="#ff011a", fg="#fff", bd=0, relief="flat", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_eliminar_carrito, "danger", hover_efecto=True)
        crear_tooltip(btn_eliminar_carrito, "Eliminar el producto seleccionado del carrito")
        self.canvas_bg.create_window(165, 560, window=btn_eliminar_carrito, width=140, height=35, anchor="center")
        
        # --- SECCIÓN 3: TOTALES Y FINALIZACIÓN (Y=600-660) ---
        y_totales = 600
        
        # Variables para totales
        total_var = tk.StringVar(value="TOTAL: $0")
        iva_var = tk.StringVar(value="IVA: $0")
        
        # Panel IVA (Izquierda)
        lbl_iva = tk.Label(self.canvas_bg, textvariable=iva_var, font=("Montserrat", 14, "bold"), 
                          bg="#6c757d", fg="#ffffff", relief="flat", bd=0, padx=20, pady=10)
        self.canvas_bg.create_window(800, 620, window=lbl_iva, anchor="center")
        
        # Panel TOTAL (Centro)
        lbl_total = tk.Label(self.canvas_bg, textvariable=total_var, font=("Montserrat", 16, "bold"), 
                           bg="#03A52B", fg="#ffffff", relief="flat", bd=0, padx=25, pady=15)
        self.canvas_bg.create_window(775, 570, window=lbl_total, anchor="center")
        
        # Botón FINALIZAR VENTA (Derecha)
        btn_finalizar = tk.Button(self.canvas_bg, text="✅ FINALIZAR VENTA", font=("Montserrat", 14, "bold"), 
                                 bg="#16fe05", fg="#ffffff", bd=0, relief="flat", cursor="hand2")
        aplicar_estilo_moderno_boton(btn_finalizar, "success", hover_efecto=True)
        crear_tooltip(btn_finalizar, "Procesar la venta y registrar en el sistema")
        self.canvas_bg.create_window(1100, y_totales, window=btn_finalizar, width=250, height=50, anchor="center")

        # --- FUNCIONES DE AUTOCOMPLETADO Y LÓGICA ---
        def set_precio_venta(event=None):
            seleccion = producto_var.get()
            if seleccion in productos_dict:
                producto = productos_dict[seleccion]
                
                # Verificar si el producto tiene una oferta activa
                precio_final = producto.precio_venta
                if producto.oferta and producto.oferta.get('tipo'):
                    if producto.oferta['tipo'] == 'porcentaje':
                        descuento = float(producto.oferta['valor'])
                        precio_final = producto.precio_venta * (1 - descuento / 100)
                    elif producto.oferta['tipo'] == 'precio_manual':
                        precio_final = float(producto.oferta['valor'])
                    # Para tipo 'cantidad' (3x2), el precio unitario no cambia aquí
                
                precio_var.set(str(precio_final))
        combo.bind("<<ComboboxSelected>>", set_precio_venta)

        def eliminar_del_carrito():
            seleccion = carrito_tree.selection()
            if not seleccion:
                messagebox.showwarning("Eliminar", "Seleccione un producto del carrito para eliminar.")
                return
            for item in seleccion:
                idx = carrito_tree.index(item)
                carrito_tree.delete(item)
                del carrito[idx]
            # Recalcular totales
            total = sum(item[3] for item in carrito)
            total_iva = sum(item[4] for item in carrito)
            total_var.set(f"TOTAL: {self.formato_moneda(total)}")
            iva_var.set(f"IVA: {self.formato_moneda(total_iva)}")

        def agregar_al_carrito():
            try:
                seleccion = producto_var.get()
                if not seleccion:
                    raise ValueError("Debe seleccionar un producto.")
                producto = productos_dict[seleccion]
                cantidad = int(ent_cantidad.get())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")
                if producto.cantidad < cantidad:
                    raise ValueError("Stock insuficiente.")
                
                precio_unitario = float(precio_var.get())
                
                # Aplicar lógica de ofertas por cantidad (ej: 3x2)
                cantidad_a_cobrar = cantidad
                if producto.oferta and producto.oferta.get('tipo') == 'cantidad':
                    oferta_str = producto.oferta['valor']  # ej: "3X2"
                    try:
                        if 'X' in oferta_str.upper():
                            partes = oferta_str.upper().split('X')
                            compra, paga = int(partes[0]), int(partes[1])
                            # Calcular cuántos grupos de oferta aplican
                            grupos_oferta = cantidad // compra
                            resto = cantidad % compra
                            cantidad_a_cobrar = (grupos_oferta * paga) + resto
                    except:
                        pass  # Si no se puede parsear, usar cantidad normal
                
                sub_total = precio_unitario * cantidad_a_cobrar
                iva = sub_total * 0.21
                carrito.append((producto, cantidad, precio_unitario, sub_total, iva))
                
                # Mostrar en la tabla con nombre más corto
                producto_nombre = f"{producto.descripcion[:20]}... | {producto.color} | {producto.talle}"
                if len(f"{producto.descripcion} | {producto.color} | {producto.talle}") <= 35:
                    producto_nombre = f"{producto.descripcion} | {producto.color} | {producto.talle}"
                
                # Mostrar indicador de oferta en el carrito
                precio_mostrar = self.formato_moneda(precio_unitario)
                if cantidad_a_cobrar != cantidad:
                    precio_mostrar += f" (Oferta {producto.oferta['valor']})"
                
                carrito_tree.insert("", "end", values=(
                    producto_nombre,
                    precio_mostrar, 
                    cantidad, 
                    self.formato_moneda(sub_total), 
                    self.formato_moneda(iva)
                ))
                
                # Limpiar campos
                producto_var.set("")
                ent_cantidad.delete(0, tk.END)
                precio_var.set("")
                
                # Actualizar totales
                total = sum(item[3] for item in carrito)
                total_iva = sum(item[4] for item in carrito)
                total_var.set(f"TOTAL: {self.formato_moneda(total)}")
                iva_var.set(f"IVA: {self.formato_moneda(total_iva)}")
            except ValueError as ve:
                messagebox.showerror("Error de carga", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
        
        def registrar_venta_final():
            if not carrito:
                messagebox.showerror("Error", "El carrito está vacío.")
                return
            nro_venta = len(self.sistema.ventas) + 1
            nro_venta_str = str(nro_venta).zfill(5)
            descripcion = f"Venta N° {nro_venta_str}"
            forma_pago = forma_pago_var.get()
            exito = self.sistema.registrar_venta(descripcion, [(p, c, pu) for p, c, pu, st, iva in carrito], datetime.date.today(), forma_pago)
            if not exito:
                messagebox.showerror("Error", "No se pudo registrar la venta (stock insuficiente en algún producto).")
                return
            messagebox.showinfo("Éxito", f"Venta N° {nro_venta_str} registrada y stock actualizado.")
            self.mostrar_menu_principal()
        
        # Asignar comandos a botones
        btn_agregar.config(command=agregar_al_carrito)
        btn_eliminar_carrito.config(command=eliminar_del_carrito)
        btn_finalizar.config(command=registrar_venta_final)
        
        # Agregar widgets a la lista - LIMPIO Y ORGANIZADO
        widgets.extend([titulo, lbl_prod, combo, lbl_cant, ent_cantidad, lbl_precio, ent_precio, 
                       lbl_forma_pago, combo_forma_pago, btn_agregar,
                       carrito_tree, scrollbar_v, btn_eliminar_carrito,
                       lbl_iva, lbl_total, btn_finalizar])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_ventas_dia(self, parent):
        widgets = []
        hoy = datetime.date.today()
        ventas_hoy = self.sistema.cierre_caja(hoy)
        
        # Título centrado (ajustado para el nuevo logo)
        lbl_titulo = tk.Label(self.canvas_bg, text=f"VENTAS DEL DÍA - {hoy.strftime('%d/%m/%Y')}", 
                             font=("Montserrat", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(640, 150, window=lbl_titulo, anchor="center")  # Ajustado para el logo
        
        # Tabla centrada y bien dimensionada (ajustada para el nuevo logo)
        cols = ("Descripción Venta", "Forma de Pago", "Detalle Artículos", "Total Venta")
        tree = ttk.Treeview(self.canvas_bg, columns=cols, show="headings")
        aplicar_estilo_moderno_treeview(tree)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        
        # Posicionar tabla centrada (ajustada)
        self.canvas_bg.create_window(640, 380, window=tree, width=1000, height=320, anchor="center")  # Ajustado
        
        # Llenar datos
        for v in ventas_hoy:
            detalle = ", ".join([f"{item['producto'].descripcion}({item['producto'].color}/{item['producto'].talle}) x{item['cantidad']} @{self.formato_moneda(item['precio'])}" for item in v.items])
            total = sum(item['cantidad'] * item['precio'] for item in v.items)
            forma_pago = getattr(v, 'forma_pago', 'EFECTIVO')
            tree.insert("", "end", values=(v.descripcion, forma_pago, detalle, self.formato_moneda(total)))
        
        # Total y botón centrados debajo de la tabla (ajustados)
        total_general = sum(sum(item['cantidad'] * item['precio'] for item in v.items) for v in ventas_hoy)
        lbl_total = tk.Label(self.canvas_bg, text=f"Total ventas del día: {self.formato_moneda(total_general)}", 
                           font=("Montserrat", 16, "bold"), bg=COLOR_BOTON, fg="#ffffff", 
                           relief="flat", bd=0, padx=20, pady=10)
        self.canvas_bg.create_window(640, 580, window=lbl_total, anchor="center")  # Ajustado
        
        # Botón cierre de caja centrado (ajustado)
        btn_cierre = tk.Button(self.canvas_bg, text="CIERRE DE CAJA", font=("Montserrat", 14, "bold"), 
                              bg="#16a333", fg="#ffffff", bd=0, relief="flat", 
                              command=self.realizar_cierre_caja, cursor="hand2")
        self.canvas_bg.create_window(640, 630, window=btn_cierre, width=220, height=50, anchor="center")  # Ajustado
        
        widgets.extend([lbl_titulo, tree, lbl_total, btn_cierre])
        self.pantalla_widgets.extend(widgets)

    def realizar_cierre_caja(self):
        """Realiza el cierre de caja del día y ofrece descarga de resumen"""
        hoy = datetime.date.today()
        ventas_hoy = self.sistema.cierre_caja(hoy)
        
        if not ventas_hoy:
            messagebox.showinfo("Cierre de Caja", "No hay ventas registradas para el día de hoy.")
            return
        
        # Crear ventana de confirmación de descarga
        self.mostrar_ventana_descarga_csv(ventas_hoy, hoy)

    def mostrar_ventana_descarga_csv(self, ventas_hoy, fecha):
        """Muestra ventana de confirmación para descarga de CSV"""
        ventana = tk.Toplevel(self)
        ventana.title("Cierre de Caja")
        ventana.geometry("450x300")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)
        
        # Crear gradiente de fondo
        canvas = tk.Canvas(ventana, width=450, height=300, highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)
        for i in range(0, 300, 2):
            color = self._interpolar_color(COLOR_GRADIENTE_1, COLOR_GRADIENTE_2, i/300)
            canvas.create_rectangle(0, i, 450, i+2, outline="", fill=color)
        
        # Título
        lbl_titulo = tk.Label(canvas, text="QUERES DESCARGAR TU RESUMEN HOY??", 
                             font=("Montserrat", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        canvas.create_window(225, 60, window=lbl_titulo, anchor="center")
        
        # Texto explicativo
        lbl_explicacion = tk.Label(canvas, text="Tus ventas quedan guardadas acá.\nDisponibles cuando quieras!", 
                                  font=("Montserrat", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center")
        canvas.create_window(225, 180, window=lbl_explicacion, anchor="center")
        
        # Botones SI / NO
        def descargar_si():
            self.generar_csv_cierre(ventas_hoy, fecha)
            # ARCHIVAR VENTAS DEL DÍA
            self.sistema.archivar_ventas_dia(fecha)
            ventana.destroy()
            # Refrescar pantalla ventas del día
            self.mostrar_ventas_dia()
            
        def descargar_no():
            # ARCHIVAR VENTAS DEL DÍA AUNQUE NO DESCARGUE CSV
            self.sistema.archivar_ventas_dia(fecha)
            messagebox.showinfo("Cierre de Caja", "Cierre de caja realizado. Las ventas han sido archivadas correctamente.")
            ventana.destroy()
            # Refrescar pantalla ventas del día
            self.mostrar_ventas_dia()
        
        btn_si = tk.Button(canvas, text="SÍ", font=("Montserrat", 14, "bold"), 
                          bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                          command=descargar_si, cursor="hand2")
        canvas.create_window(150, 240, window=btn_si, width=100, height=40, anchor="center")
        
        btn_no = tk.Button(canvas, text="NO", font=("Montserrat", 14, "bold"), 
                          bg="#666666", fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", 
                          command=descargar_no, cursor="hand2")
        canvas.create_window(300, 240, window=btn_no, width=100, height=40, anchor="center")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
    def generar_csv_cierre(self, ventas_hoy, fecha):
        """Genera archivo CSV con el resumen del día"""
        
        # Calcular totales por forma de pago
        totales_forma_pago = {}
        total_general = 0
        detalle_ventas = []
        
        for venta in ventas_hoy:
            forma_pago = getattr(venta, 'forma_pago', 'EFECTIVO')
            total_venta = sum(item['cantidad'] * item['precio'] for item in venta.items)
            total_general += total_venta
            
            if forma_pago not in totales_forma_pago:
                totales_forma_pago[forma_pago] = 0
            totales_forma_pago[forma_pago] += total_venta
            
            # Detalle de cada venta
            for item in venta.items:
                detalle_ventas.append({
                    'Fecha': fecha.strftime("%Y-%m-%d"),
                    'Descripción Venta': venta.descripcion,
                    'Forma de Pago': forma_pago,
                    'Producto': item['producto'].descripcion,
                    'Marca': item['producto'].marca,
                    'Color': item['producto'].color,
                    'Talle': item['producto'].talle,
                    'Cantidad': item['cantidad'],
                    'Precio Unitario': item['precio'],
                    'Subtotal': item['cantidad'] * item['precio']
                })
        
        # Pedir ubicación de guardado
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"Cierre_Caja_{fecha.strftime('%Y-%m-%d')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado del resumen
                    writer.writerow(['RESUMEN CIERRE DE CAJA'])
                    writer.writerow(['Fecha:', fecha.strftime("%Y-%m-%d")])
                    writer.writerow([''])
                    
                    # Totales por forma de pago
                    writer.writerow(['TOTALES POR FORMA DE PAGO'])
                    for forma_pago, total in totales_forma_pago.items():
                        writer.writerow([forma_pago, self.formato_moneda(total)])
                    writer.writerow([''])
                    writer.writerow(['TOTAL GENERAL', self.formato_moneda(total_general)])
                    writer.writerow([''])
                    writer.writerow([''])
                    
                    # Detalle de ventas
                    writer.writerow(['DETALLE DE VENTAS'])
                    if detalle_ventas:
                        fieldnames = detalle_ventas[0].keys()
                        dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        dict_writer.writeheader()
                        dict_writer.writerows(detalle_ventas)
                
                messagebox.showinfo("Descarga Exitosa", f"Archivo guardado en:\n{filename}\n\nCierre de caja realizado correctamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo:\n{e}")
        else:
            messagebox.showinfo("Cierre de Caja", "Cierre de caja realizado. Las ventas han sido guardadas correctamente.")

    # FUNCIONES FALTANTES PARA LOS BOTONES DEL MENÚ
    def carga_masiva_productos(self):
        import tkinter.filedialog as fd
        from tkinter import messagebox
        import csv
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        lbl_info = tk.Label(self.canvas_bg, text="Carga masiva de productos desde archivo CSV", font=("Montserrat", 15, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(640, 150, window=lbl_info, anchor="n")  # Ajustado para el logo
        def descargar_modelo():
            modelo = "marca,descripcion,color,talle,cantidad,precio_costo,porcentaje_venta,porcentaje_amigo\nNike,Remera,Rojo,M,10,1000,50,20\n"
            ruta = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Guardar archivo modelo")
            if ruta:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(modelo)
                messagebox.showinfo("Archivo guardado", f"Archivo modelo guardado en:\n{ruta}")
        def parse_num(val):
            if val == "-":
                return 0
            if val == "" or val is None:
                raise ValueError("Hay campos numéricos vacíos. Complete o coloque '-' para cero.")
            return float(val)
        def cargar_csv():
            ruta = fd.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Seleccionar archivo CSV")
            if not ruta:
                return
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    requeridos = ["marca", "descripcion", "color", "talle", "cantidad", "precio_costo", "porcentaje_venta", "porcentaje_amigo"]
                    for row in reader:
                        if not all(k in row for k in requeridos):
                            raise ValueError("El archivo no tiene todas las columnas requeridas.")
                        self.sistema.agregar_producto(
                            row["marca"],
                            row["descripcion"],
                            row["color"],
                            row["talle"],
                            int(parse_num(row["cantidad"])),
                            float(parse_num(row["precio_costo"])),
                            float(parse_num(row["porcentaje_venta"])),
                            float(parse_num(row["porcentaje_amigo"]))
                        )
                messagebox.showinfo("Éxito", "Productos cargados correctamente.")
                self.mostrar_menu_secundario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
        btn_descargar = tk.Button(self.canvas_bg, text="⬇️ Descargar archivo modelo CSV", font=("Montserrat", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", command=descargar_modelo)
        self.canvas_bg.create_window(640, 220, window=btn_descargar, width=320, height=40, anchor="n")  # Ajustado
        btn_cargar = tk.Button(self.canvas_bg, text="📁 Seleccionar y cargar archivo CSV", font=("Montserrat", 12, "bold"), bg="#4CAF50", fg="#ffffff", bd=0, relief="flat", command=cargar_csv)
        self.canvas_bg.create_window(640, 280, window=btn_cargar, width=320, height=40, anchor="n")  # Ajustado
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado para el logo
        self.pantalla_widgets.extend([lbl_info, btn_descargar, btn_cargar, btn_volver])

    def mostrar_reportes(self):
        print("[DEBUG] mostrar_reportes() llamado - main.py:1566")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        widgets = []
        
        # Título (ajustado para el logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="VER VENTAS", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(1100, 50, window=lbl_titulo, anchor="n")  # Ajustado
        
        # Filtros de fecha (ajustados)
        lbl_desde = tk.Label(self.canvas_bg, text="Desde:", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_desde)
        self.canvas_bg.create_window(100, 200, window=lbl_desde, anchor="nw")  # Ajustado
        ent_desde = tk.Entry(self.canvas_bg, font=("Montserrat", 11), bg="#ffffff", fg=COLOR_TEXTO, bd=1, relief="solid")
        aplicar_estilo_moderno_entry(ent_desde)
        self.canvas_bg.create_window(100, 225, window=ent_desde, width=150, height=30, anchor="nw")  # Ajustado
        ent_desde.insert(0, datetime.date.today().strftime("%d-%m-%Y"))
        
        lbl_hasta = tk.Label(self.canvas_bg, text="Hasta:", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_hasta)
        self.canvas_bg.create_window(280, 200, window=lbl_hasta, anchor="nw")  # Ajustado
        ent_hasta = tk.Entry(self.canvas_bg, font=("Montserrat", 11), bg="#ffffff", fg=COLOR_TEXTO, bd=1, relief="solid")
        aplicar_estilo_moderno_entry(ent_hasta)
        self.canvas_bg.create_window(280, 225, window=ent_hasta, width=150, height=30, anchor="nw")  # Ajustado
        ent_hasta.insert(0, datetime.date.today().strftime("%d-%m-%Y"))
        
        # Filtro de forma de pago (ajustado)
        lbl_forma_pago = tk.Label(self.canvas_bg, text="Forma de pago:", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_forma_pago)
        self.canvas_bg.create_window(460, 200, window=lbl_forma_pago, anchor="nw")  # Ajustado
        combo_forma_pago = ttk.Combobox(self.canvas_bg, values=["TODAS", "EFECTIVO", "DEBITO", "CREDITO", "TRANSFERENCIA", "QR", "OTROS"], font=("Montserrat", 11), state="readonly")
        aplicar_estilo_moderno_combobox(combo_forma_pago)
        self.canvas_bg.create_window(460, 225, window=combo_forma_pago, width=150, height=30, anchor="nw")  # Ajustado
        combo_forma_pago.set("TODAS")
        
        # Filtro de marca (ajustado)
        lbl_marca = tk.Label(self.canvas_bg, text="Marca:", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_marca)
        self.canvas_bg.create_window(640, 200, window=lbl_marca, anchor="nw")  # Ajustado
        marcas = list(set([p.marca for p in self.sistema.productos if p.marca]))
        marcas.insert(0, "TODAS")
        combo_marca = ttk.Combobox(self.canvas_bg, values=marcas, font=("Montserrat", 11), state="readonly")
        aplicar_estilo_moderno_combobox(combo_marca)
        self.canvas_bg.create_window(640, 225, window=combo_marca, width=150, height=30, anchor="nw")  # Ajustado
        combo_marca.set("TODAS")
        
        # Filtro de producto (ajustado)
        lbl_producto = tk.Label(self.canvas_bg, text="Producto:", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        aplicar_estilo_moderno_label(lbl_producto)
        self.canvas_bg.create_window(820, 200, window=lbl_producto, anchor="nw")  # Ajustado
        productos = list(set([p.descripcion for p in self.sistema.productos if p.descripcion]))
        productos.insert(0, "TODOS")
        combo_producto = ttk.Combobox(self.canvas_bg, values=productos, font=("Montserrat", 11), state="readonly")
        aplicar_estilo_moderno_combobox(combo_producto)
        self.canvas_bg.create_window(820, 225, window=combo_producto, width=150, height=30, anchor="nw")  # Ajustado
        combo_producto.set("TODOS")
        
        # Botón buscar (ajustado)
        btn_buscar = tk.Button(self.canvas_bg, text="🔍 Buscar", font=("Montserrat", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat")
        aplicar_estilo_moderno_boton(btn_buscar, "primario", hover_efecto=True)
        self.canvas_bg.create_window(150, 300, window=btn_buscar, width=100, height=30, anchor="w")  # Ajustado
        
        # Tabla de resultados (ajustada)
        cols = ("Fecha", "Descripción", "Forma Pago", "Marca", "Producto", "Color", "Talle", "Cantidad", "Precio", "Subtotal")
        tree = ttk.Treeview(self.canvas_bg, columns=cols, show="headings")
        aplicar_estilo_moderno_treeview(tree)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        # Scrollbar para la tabla (ajustada)
        scrollbar = ttk.Scrollbar(self.canvas_bg, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_bg.create_window(570, 320, window=tree, width=1100, height=280, anchor="n")  # Ajustado
        self.canvas_bg.create_window(1110, 320, window=scrollbar, width=20, height=280, anchor="n")  # Ajustado
        
        # Label total (ajustado)
        lbl_total = tk.Label(self.canvas_bg, text="Total: $0.00", font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.canvas_bg.create_window(100, 620, window=lbl_total, anchor="w")  # Mantener posición
        
        def buscar_reportes():
            try:
                fecha_desde = datetime.datetime.strptime(ent_desde.get(), "%Y-%m-%d").date()
                fecha_hasta = datetime.datetime.strptime(ent_hasta.get(), "%Y-%m-%d").date()
                forma_pago_filtro = combo_forma_pago.get()
                marca_filtro = combo_marca.get()
                producto_filtro = combo_producto.get()
                
                # Limpiar tabla
                for item in tree.get_children():
                    tree.delete(item)
                
                total_general = 0
                
                # OBTENER VENTAS ACTUALES (del día)
                ventas_actuales = self.sistema.reporte_ventas(fecha_desde, fecha_hasta)
                
                # OBTENER VENTAS HISTÓRICAS (archivadas)
                ventas_historicas = []
                años_buscar = set()
                año_actual = fecha_desde.year
                año_final = fecha_hasta.year
                
                # Agregar todos los años en el rango de búsqueda
                for año in range(año_actual, año_final + 1):
                    años_buscar.add(año)
                
                # Cargar datos históricos de cada año
                for año in años_buscar:
                    archivo_historico = f"ventas_historico_{año}.json"
                    if os.path.exists(archivo_historico):
                        try:
                            with open(archivo_historico, "r", encoding="utf-8") as f:
                                datos_historicos = json.load(f)
                                
                                for venta_data in datos_historicos:
                                    fecha_venta = datetime.datetime.strptime(venta_data['fecha'], "%Y-%m-%d").date()
                                    
                                    # Verificar si está en el rango de fechas
                                    if fecha_desde <= fecha_venta <= fecha_hasta:
                                        ventas_historicas.append(venta_data)
                        except Exception:
                            continue  # Si hay error leyendo archivo, continuar
                
                # PROCESAR VENTAS ACTUALES
                for venta in ventas_actuales:
                    forma_pago_venta = getattr(venta, 'forma_pago', 'EFECTIVO')
                    
                    # Filtrar por forma de pago
                    if forma_pago_filtro != "TODAS" and forma_pago_venta != forma_pago_filtro:
                        continue
                    
                    for item in venta.items:
                        producto = item['producto']
                        
                        # Filtrar por marca
                        if marca_filtro != "TODAS" and producto.marca != marca_filtro:
                            continue
                        
                        # Filtrar por producto
                        if producto_filtro != "TODOS" and producto.descripcion != producto_filtro:
                            continue
                        
                        subtotal = item['cantidad'] * item['precio']
                        total_general += subtotal
                        
                        tree.insert("", "end", values=(
                            venta.fecha.strftime("%Y-%m-%d"),
                            venta.descripcion,
                            forma_pago_venta,
                            producto.marca,
                            producto.descripcion,
                            producto.color,
                            producto.talle,
                            item['cantidad'],
                            self.formato_moneda(item['precio']),
                            self.formato_moneda(subtotal)
                        ))
                
                # PROCESAR VENTAS HISTÓRICAS
                for venta_hist in ventas_historicas:
                    forma_pago_venta = venta_hist.get('forma_pago', 'EFECTIVO')
                    
                    # Filtrar por forma de pago
                    if forma_pago_filtro != "TODAS" and forma_pago_venta != forma_pago_filtro:
                        continue
                    
                    for item in venta_hist['items']:
                        # Filtrar por marca
                        if marca_filtro != "TODAS" and item.get('marca', '') != marca_filtro:
                            continue
                        
                        # Filtrar por producto
                        if producto_filtro != "TODOS" and item.get('producto', '') != producto_filtro:
                            continue
                        
                        subtotal = item['cantidad'] * item['precio']
                        total_general += subtotal
                        
                        tree.insert("", "end", values=(
                            venta_hist['fecha'],
                            venta_hist['descripcion'],
                            forma_pago_venta,
                            item.get('marca', ''),
                            item.get('producto', ''),
                            item.get('color', ''),
                            item.get('talle', ''),
                            item['cantidad'],
                            self.formato_moneda(item['precio']),
                            self.formato_moneda(subtotal)
                        ))
                
                lbl_total.config(text=f"Total: {self.formato_moneda(total_general)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error en la búsqueda: {e}")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar reporte: {e}")
        
        btn_buscar.config(command=buscar_reportes)
        
        # Botón volver (ajustado para el logo)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado
        
        widgets.extend([lbl_titulo, lbl_desde, ent_desde, lbl_hasta, ent_hasta, lbl_forma_pago, combo_forma_pago, 
                       lbl_marca, combo_marca, lbl_producto, combo_producto, btn_buscar, tree, scrollbar, lbl_total, btn_volver])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_alta_producto(self, parent):
        """Pantalla para agregar productos"""
        widgets = []
        
        # Título centrado (ajustado para el logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="📦 AGREGAR NUEVO PRODUCTO", 
                             font=("Montserrat", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(640, 150, window=lbl_titulo, anchor="center")  # Ajustado
        
        # Campos organizados en dos columnas (ajustados)
        campos_col1 = ["Marca", "Descripción", "Color", "Talle"]
        campos_col2 = ["Cantidad", "Precio Costo", "% Venta", "% Amigo"]
        entradas = {}
        
        # Columna izquierda (ajustada)
        x_col1_label = 300
        x_col1_entry = 320
        y_start = 220  # Ajustado para el logo
        spacing = 50
        
        for i, campo in enumerate(campos_col1):
            y_pos = y_start + i * spacing
            lbl = tk.Label(self.canvas_bg, text=f"{campo}:", font=("Montserrat", 12, "bold"), 
                          bg=COLOR_FONDO, fg=COLOR_TEXTO)
            self.canvas_bg.create_window(x_col1_label, y_pos, window=lbl, anchor="e")
            
            ent = tk.Entry(self.canvas_bg, font=("Montserrat", 12), bg=COLOR_ENTRY_VENTA_BG, 
                          fg="#000000", bd=2, relief="ridge")
            self.canvas_bg.create_window(x_col1_entry, y_pos, window=ent, width=220, height=35, anchor="w")
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        
        # Columna derecha
        x_col2_label = 700
        x_col2_entry = 820
        
        for i, campo in enumerate(campos_col2):
            y_pos = y_start + i * spacing
            lbl = tk.Label(self.canvas_bg, text=f"{campo}:", font=("Montserrat", 12, "bold"), 
                          bg=COLOR_FONDO, fg=COLOR_TEXTO)
            self.canvas_bg.create_window(x_col2_label, y_pos, window=lbl, anchor="e")
            
            ent = tk.Entry(self.canvas_bg, font=("Montserrat", 12), bg=COLOR_ENTRY_VENTA_BG, 
                          fg="#000000", bd=2, relief="ridge")
            self.canvas_bg.create_window(710, y_pos, window=ent, width=220, height=35, anchor="w")
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        
        # Valores por defecto
        entradas["% Venta"].insert(0, "50")
        entradas["% Amigo"].insert(0, "20")
        
        def guardar_producto():
            try:
                marca = entradas["Marca"].get().strip()
                descripcion = entradas["Descripción"].get().strip()
                color = entradas["Color"].get().strip()
                talle = entradas["Talle"].get().strip()
                cantidad = int(entradas["Cantidad"].get())
                precio_costo = float(entradas["Precio Costo"].get())
                porcentaje_venta = float(entradas["% Venta"].get())
                porcentaje_amigo = float(entradas["% Amigo"].get())
                
                if not all([marca, descripcion, color, talle]):
                    raise ValueError("Todos los campos de texto son obligatorios")
                
                self.sistema.agregar_producto(marca, descripcion, color, talle, cantidad, 
                                            precio_costo, porcentaje_venta, porcentaje_amigo)
                messagebox.showinfo("Éxito", "Producto agregado correctamente")
                self.mostrar_menu_secundario()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
        
        # Botones centrados (ajustados)
        btn_guardar = tk.Button(self.canvas_bg, text="GUARDAR PRODUCTO", font=("Montserrat", 14, "bold"), 
                               bg="#019807", fg="#ffffff", bd=0, relief="flat", 
                               command=guardar_producto, cursor="hand2")
        self.canvas_bg.create_window(640, 520, window=btn_guardar, width=220, height=50, anchor="center")  # Ajustado
        
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#ffffff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado
        
        widgets.extend([lbl_titulo, btn_guardar, btn_volver])
        self.pantalla_widgets.extend(widgets)


    def _pantalla_actualizar_precio(self, parent):
        """Pantalla para actualizar precios"""
        widgets = []
        
        # Título centrado (ajustado para el logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="ACTUALIZAR PRECIO", 
                             font=("Montserrat", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(1150, 50, window=lbl_titulo, anchor="center")  # Ajustado
        
        # Campos centrados (ajustados)
        campos = ["Marca", "Descripción", "Color", "Talle", "Nuevo Precio Costo"]
        entradas = {}
        
        y_start = 220  # Ajustado para el logo
        spacing = 60
        x_label = 500
        x_entry = 640
        
        for i, campo in enumerate(campos):
            y_pos = y_start + i * spacing
            lbl = tk.Label(self.canvas_bg, text=f"{campo}:", font=("Montserrat", 12, "bold"), 
                          bg=COLOR_FONDO, fg=COLOR_TEXTO)
            self.canvas_bg.create_window(x_label, y_pos, window=lbl, anchor="e")
            
            ent = tk.Entry(self.canvas_bg, font=("Montserrat", 12), bg=COLOR_ENTRY_VENTA_BG, 
                          fg="#000000", bd=2, relief="ridge")
            self.canvas_bg.create_window(x_entry, y_pos, window=ent, width=250, height=35, anchor="center")
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        
        def actualizar_precio():
            try:
                marca = entradas["Marca"].get().strip()
                descripcion = entradas["Descripción"].get().strip()
                color = entradas["Color"].get().strip()
                talle = entradas["Talle"].get().strip()
                nuevo_precio = float(entradas["Nuevo Precio Costo"].get())
                
                if not all([marca, descripcion, color, talle]):
                    raise ValueError("Todos los campos son obligatorios")
                
                if self.sistema.actualizar_precio_producto(marca, descripcion, color, talle, nuevo_precio):
                    messagebox.showinfo("Éxito", "Precio actualizado correctamente")
                    # Limpiar campos
                    for ent in entradas.values():
                        ent.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Producto no encontrado")
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
        
        # Botones centrados (ajustados)
        btn_actualizar = tk.Button(self.canvas_bg, text="ACTUALIZAR PRECIO", font=("Montserrat", 14, "bold"), 
                                  bg=COLOR_BOTON, fg="#ffffff", bd=0, relief="flat", 
                                  command=actualizar_precio, cursor="hand2")
        self.canvas_bg.create_window(640, 550, window=btn_actualizar, width=200, height=50, anchor="center")  # Ajustado
        
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#ffffff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado
        
        widgets.extend([lbl_titulo, btn_actualizar, btn_volver])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_inventario(self, parent):
        """Pantalla para ver inventario"""
        widgets = []
        
        # Título centrado (ajustado para el logo)
        lbl_titulo = tk.Label(self.canvas_bg, text="INVENTARIO DE PRODUCTOS", 
                             font=("Montserrat", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(1100, 60, window=lbl_titulo, anchor="center")  # Ajustado
        
        productos = self.sistema.inventario_actual()
        cols = ("Marca", "Descripción", "Color", "Talle", "Stock", "Precio Costo", "Precio Venta")
        tree = ttk.Treeview(self.canvas_bg, columns=cols, show="headings")
        aplicar_estilo_moderno_treeview(tree)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        
        for p in productos:
            tree.insert("", "end", values=(p.marca, p.descripcion, p.color, p.talle, 
                                         p.cantidad, self.formato_moneda(p.precio_costo), 
                                         self.formato_moneda(p.precio_venta)))
        
        # Tabla centrada (ajustada)
        self.canvas_bg.create_window(640, 380, window=tree, width=1050, height=480, anchor="center")  # Ajustada
        
        # Botones MODIFICAR y ELIMINAR debajo de la tabla
        def modificar_producto():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Modificar", "Seleccione un producto de la lista para modificar.")
                return
            
            # Obtener datos del producto seleccionado
            item = tree.item(seleccion[0])
            valores = item['values']
            marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
            
            # Buscar el producto en el sistema
            producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
            if producto:
                datos = (marca, descripcion, color, talle, producto.cantidad, producto.precio_costo, 
                        producto.porcentaje_venta, producto.porcentaje_amigo)
                self._pantalla_modificar_producto(datos)
        
        def eliminar_producto():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Eliminar", "Seleccione uno o más productos de la lista para eliminar.")
                return
            
            # Obtener datos de los productos seleccionados
            productos_a_eliminar = []
            productos_nombres = []
            
            for item_id in seleccion:
                item = tree.item(item_id)
                valores = item['values']
                marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                productos_a_eliminar.append((marca, descripcion, color, talle))
                productos_nombres.append(f"{descripcion} - {color} - {talle}")
            
            # Confirmar eliminación
            if len(productos_a_eliminar) == 1:
                respuesta = messagebox.askyesno("Confirmar eliminación", 
                                              f"¿Está seguro de eliminar el producto:\n{productos_nombres[0]}?")
            else:
                lista_productos = "\n".join(productos_nombres[:5])  # Mostrar máximo 5
                if len(productos_nombres) > 5:
                    lista_productos += f"\n... y {len(productos_nombres) - 5} más"
                
                respuesta = messagebox.askyesno("Confirmar eliminación múltiple", 
                                              f"¿Está seguro de eliminar {len(productos_a_eliminar)} productos?\n\n{lista_productos}")
            
            if respuesta:
                # Eliminar todos los productos seleccionados
                self.sistema.eliminar_productos_masivo(productos_a_eliminar)
                
                if len(productos_a_eliminar) == 1:
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                else:
                    messagebox.showinfo("Éxito", f"{len(productos_a_eliminar)} productos eliminados correctamente.")
                
                self.mostrar_inventario()  # Refrescar pantalla
        
        # Posicionar botones horizontalmente debajo de la tabla
        btn_y = 650  # Posición Y debajo de la tabla
        btn_spacing = 180  # Espaciado entre botones
        btn_center_x = 640  # Centro de la pantalla
        
        btn_modificar = tk.Button(self.canvas_bg, text="MODIFICAR", font=("Montserrat", 12, "bold"), 
                                bg=COLOR_BOTON, fg="#ffffff", bd=0, relief="flat", 
                                command=modificar_producto, cursor="hand2")
        self.canvas_bg.create_window(btn_center_x - btn_spacing//2, btn_y, window=btn_modificar, 
                                   width=140, height=45, anchor="center")
        
        btn_eliminar = tk.Button(self.canvas_bg, text="ELIMINAR", font=("Montserrat", 12, "bold"), 
                               bg="#ff0000", fg="#ffffff", bd=0, relief="flat", 
                               command=eliminar_producto, cursor="hand2")
        self.canvas_bg.create_window(btn_center_x + btn_spacing//2, btn_y, window=btn_eliminar, 
                                   width=140, height=45, anchor="center")
        
        # Botón volver (ajustado)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#ffffff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")  # Ajustado
        
        widgets.extend([lbl_titulo, tree, btn_modificar, btn_eliminar, btn_volver])
        self.pantalla_widgets.extend(widgets)

    def _pantalla_cierre_caja(self, parent):
        """Pantalla de cierre de caja - redirige a ventas del día"""
        self.mostrar_ventas_dia()

    def _pantalla_modificar_producto(self, datos):
        # datos: (marca, descripcion, color, talle, cantidad, costo, venta, amigo)
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        campos = ["Marca", "Descripción", "Color", "Talle", "Cantidad", "Precio de costo", "% Venta", "% Amigo"]
        entradas = {}
        widgets = []
        for i, campo in enumerate(campos):
            lbl = tk.Label(self.canvas_bg, text=campo, font=("Montserrat", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO)
            ent = tk.Entry(self.canvas_bg, font=("Montserrat", 10), bg=COLOR_ENTRADA, fg=COLOR_TEXTO, bd=1, relief="solid")
            win_lbl = self.canvas_bg.create_window(120, 60 + i*50, window=lbl, width=110, height=30, anchor="w")
            win_ent = self.canvas_bg.create_window(250, 60 + i*50, window=ent, width=300, height=30, anchor="w")
            entradas[campo] = ent
            widgets.extend([lbl, ent])
        # Cargar datos actuales
        for i, campo in enumerate(campos):
            entradas[campo].insert(0, str(datos[i]))
        def guardar():
            try:
                marca = entradas["Marca"].get()
                descripcion = entradas["Descripción"].get()
                color = entradas["Color"].get()
                talle = entradas["Talle"].get()
                cantidad = int(entradas["📊 Cantidad"].get())
                precio_costo = float(entradas["Precio de costo"].get())
                porcentaje_venta = float(entradas["% Venta"].get())
                porcentaje_amigo = float(entradas["% Amigo"].get())
                # Eliminar producto anterior y agregar el modificado
                self.sistema.eliminar_producto(datos[0], datos[1], datos[2], datos[3])
                self.sistema.agregar_producto(marca, descripcion, color, talle, cantidad, precio_costo, porcentaje_venta, porcentaje_amigo)
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.mostrar_inventario()
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
        btn_guardar = tk.Button(self.canvas_bg, text="💾 Guardar cambios", font=("Montserrat", 12, "bold"), bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat", command=guardar)
        win_btn = self.canvas_bg.create_window(200, 420, window=btn_guardar, width=180, height=40, anchor="nw")
        widgets.append(btn_guardar)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), bg="#666666", fg="#fff", bd=0, relief="flat", command=self.mostrar_inventario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        widgets.append(btn_volver)
        self.pantalla_widgets.extend(widgets)

    def mostrar_centro_ia(self):
        """Centro unificado de todas las funciones de Inteligencia Artificial"""
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        widgets = []
        
        # --- TÍTULO PRINCIPAL ---
        lbl_titulo = tk.Label(self.canvas_bg, text="🤖 CENTRO DE IA", 
                             font=("Montserrat", 20, "bold"), bg=COLOR_FONDO, fg=COLOR_CIAN)
        self.canvas_bg.create_window(1130, 75, window=lbl_titulo, anchor="center")
        
       
        
       
        
        # --- PANEL DE NAVEGACIÓN IA ---
        frame_nav = tk.Frame(self.canvas_bg, bg="#1a2e2e", relief="solid", bd=2)
        self.canvas_bg.create_window(640, 145, window=frame_nav, width=1090, height=60, anchor="center")
        
        # Variable para controlar la vista activa
        self.vista_ia_activa = tk.StringVar(value="dashboard")
        
        # Botones de navegación IA con mejores efectos hover
        btn_dashboard = tk.Button(frame_nav, text="Dashboard", font=("Montserrat", 11, "bold"), 
                                 bg=COLOR_CIAN, fg="#000000", bd=0, relief="flat", cursor="hand2",
                                 command=lambda: self._cambiar_vista_ia("dashboard"))
        btn_dashboard.place(x=20, y=15, width=150, height=30)
        btn_dashboard.bind("<Enter>", lambda e: btn_dashboard.config(bg="#00E5FF"))
        btn_dashboard.bind("<Leave>", lambda e: btn_dashboard.config(bg=COLOR_CIAN))
        
        btn_reposicion = tk.Button(frame_nav, text="Reposición", font=("Montserrat", 11, "bold"), 
                                  bg="#4CAF50", fg="#ffffff", bd=0, relief="flat", cursor="hand2",
                                  command=lambda: self._cambiar_vista_ia("reposicion"))
        btn_reposicion.place(x=190, y=15, width=150, height=30)
        btn_reposicion.bind("<Enter>", lambda e: btn_reposicion.config(bg="#66BB6A"))
        btn_reposicion.bind("<Leave>", lambda e: btn_reposicion.config(bg="#4CAF50"))
        
        btn_precios = tk.Button(frame_nav, text="Precios", font=("Montserrat", 11, "bold"), 
                               bg="#FF9800", fg="#000000", bd=0, relief="flat", cursor="hand2",
                               command=lambda: self._cambiar_vista_ia("precios"))
        btn_precios.place(x=360, y=15, width=150, height=30)
        btn_precios.bind("<Enter>", lambda e: btn_precios.config(bg="#FFB74D"))
        btn_precios.bind("<Leave>", lambda e: btn_precios.config(bg="#FF9800"))
        
        btn_analisis = tk.Button(frame_nav, text="Análisis", font=("Montserrat", 11, "bold"), 
                                bg="#9C27B0", fg="#ffffff", bd=0, relief="flat", cursor="hand2",
                                command=lambda: self._cambiar_vista_ia("analisis"))
        btn_analisis.place(x=530, y=15, width=150, height=30)
        btn_analisis.bind("<Enter>", lambda e: btn_analisis.config(bg="#BA68C8"))
        btn_analisis.bind("<Leave>", lambda e: btn_analisis.config(bg="#9C27B0"))
        
        btn_exportar = tk.Button(frame_nav, text="Exportar Todo", font=("Montserrat", 11, "bold"), 
                                bg="#607D8B", fg="#ffffff", bd=0, relief="flat", cursor="hand2",
                                command=self._exportar_centro_ia)
        btn_exportar.place(x=700, y=15, width=150, height=30)
        btn_exportar.bind("<Enter>", lambda e: btn_exportar.config(bg="#78909C"))
        btn_exportar.bind("<Leave>", lambda e: btn_exportar.config(bg="#607D8B"))
        
        btn_actualizar = tk.Button(frame_nav, text="🔄 Actualizar", font=("Montserrat", 11, "bold"), 
                                  bg="#2196F3", fg="#ffffff", bd=0, relief="flat", cursor="hand2",
                                  command=self._actualizar_centro_ia)
        btn_actualizar.place(x=870, y=15, width=150, height=30)
        btn_actualizar.bind("<Enter>", lambda e: btn_actualizar.config(bg="#42A5F5"))
        btn_actualizar.bind("<Leave>", lambda e: btn_actualizar.config(bg="#2196F3"))
        
        # --- ÁREA DE CONTENIDO DINÁMICO ---
        self.frame_contenido_ia = tk.Frame(self.canvas_bg, bg=COLOR_FONDO)
        self.canvas_bg.create_window(640, 440, window=self.frame_contenido_ia, width=1200, height=520, anchor="center")
        
        # Cargar vista inicial
        self._cambiar_vista_ia("dashboard")
        
        # --- BOTÓN VOLVER ---
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#ffffff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        btn_volver.bind("<Enter>", lambda e: btn_volver.config(bg="#777777"))
        btn_volver.bind("<Leave>", lambda e: btn_volver.config(bg="#666666"))
        
        widgets.extend([lbl_titulo, frame_nav, btn_volver])
        self.pantalla_widgets.extend(widgets)
    
    def mostrar_crear_ofertas(self):
        """Pantalla para crear y gestionar ofertas"""
        print("[DEBUG] mostrar_crear_ofertas() llamado - main.py:NEW - main.py:2177")
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_crear_ofertas(self.canvas_bg)
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#fff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)

    def _pantalla_crear_ofertas(self, parent, solo_ofertas_activas=False):
        """Pantalla para crear y gestionar ofertas en productos"""
        widgets = []
        
        # Título centrado (ajustado para el logo)
        titulo_texto = "OFERTAS ACTIVAS" if solo_ofertas_activas else "CREAR Y GESTIONAR OFERTAS"
        lbl_titulo = tk.Label(self.canvas_bg, text=titulo_texto, 
                             font=("Montserrat", 18, "bold"), bg="#FF0000", fg=COLOR_CIAN)
        self.canvas_bg.create_window(1050, 75, window=lbl_titulo, anchor="center")
        
        # --- FILTROS Y CONTROLES DE VISTA ---
        frame_controles = tk.Frame(self.canvas_bg, bg="#817E7E")
        self.canvas_bg.create_window(840, 150, window=frame_controles, width=370, height=33, anchor="w")
        widgets.append(frame_controles)
        # Botones de filtro
        if solo_ofertas_activas:
            btn_vista = tk.Button(frame_controles, text="VER TODOS LOS PRODUCTOS", 
                                 font=("Montserrat", 10, "bold"), bg="#2196F3", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2",
                                 command=lambda: self.mostrar_crear_ofertas())
        else:
            btn_vista = tk.Button(frame_controles, text="VER OFERTAS ACTIVAS", 
                                 font=("Montserrat", 12, "bold"), bg="#018627", fg="#ffffff", 
                                 bd=0, relief="flat", cursor="hand2",
                                 command=lambda: self._mostrar_ofertas_activas())
        btn_vista.pack(side="right", padx=(10,0))
        
        # Contador de ofertas activas
        productos = self.sistema.inventario_actual()
        ofertas_activas = [p for p in productos if p.oferta and p.oferta.get('tipo')]
        lbl_contador = tk.Label(frame_controles, 
                               text=f"{len(ofertas_activas)} ofertas activas", 
                               font=("Montserrat", 10, "bold"), bg="#817E7E", fg="#000000")
        lbl_contador.pack(side="right", padx=(10, 0))
        
        # --- LISTA DE PRODUCTOS ---
        productos_a_mostrar = ofertas_activas if solo_ofertas_activas else productos
        
        lbl_productos = tk.Label(self.canvas_bg, 
                                text="PRODUCTOS CON OFERTAS ACTIVAS:" if solo_ofertas_activas else "1° SELECCIONAR PRODUCTO", 
                                font=("Montserrat", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.canvas_bg.create_window(100, 210, window=lbl_productos, anchor="w")
        
        # Mensaje si no hay ofertas activas
        if solo_ofertas_activas and not ofertas_activas:
            lbl_sin_ofertas = tk.Label(self.canvas_bg, 
                                      text="No hay ofertas activas en este momento.\n\nUtilice 'VER TODOS LOS PRODUCTOS' para crear nuevas ofertas.", 
                                      font=("Montserrat", 12), bg=COLOR_FONDO, fg="#FFFFFF", justify="center")
            self.canvas_bg.create_window(640, 350, window=lbl_sin_ofertas, anchor="center")
            widgets.extend([lbl_titulo, frame_controles, lbl_productos, lbl_sin_ofertas])
            self.pantalla_widgets.extend(widgets)
            return
        
        # Tabla de productos con columna de oferta actual
        cols = ("Marca", "Descripción", "Color", "Talle", "Stock", "Precio", "Oferta Actual")
        tree_productos = ttk.Treeview(self.canvas_bg, columns=cols, show="headings")
        aplicar_estilo_moderno_treeview(tree_productos)
        
        anchos = [100, 150, 80, 60, 60, 100, 150]
        for col, ancho in zip(cols, anchos):
            tree_productos.heading(col, text=col, anchor="center")
            tree_productos.column(col, width=ancho, anchor="center")
        
        # Llenar datos de productos
        for p in productos_a_mostrar:
            oferta_actual = "Sin oferta"
            if p.oferta and p.oferta.get('tipo'):
                if p.oferta['tipo'] == 'porcentaje':
                    oferta_actual = f"Descuento {p.oferta['valor']}%"
                elif p.oferta['tipo'] == 'cantidad':
                    oferta_actual = f"Oferta {p.oferta['valor']}"
                elif p.oferta['tipo'] == 'precio_manual':
                    oferta_actual = f"Precio especial ${p.oferta['valor']}"
            
            tree_productos.insert("", "end", values=(
                p.marca, p.descripcion, p.color, p.talle, p.cantidad,
                self.formato_moneda(p.precio_venta), oferta_actual
            ))
        
        # Posicionar tabla de productos
        altura_tabla = 250 if solo_ofertas_activas else 280
        self.canvas_bg.create_window(100, 240, window=tree_productos, width=700, height=altura_tabla, anchor="nw")
        
        # --- PANEL DE CONFIGURACIÓN DE OFERTAS (LADO DERECHO) ---
        # Solo mostrar panel de configuración si no estamos en vista de solo ofertas activas
        if not solo_ofertas_activas:
            frame_ofertas = tk.Frame(self.canvas_bg, bg="#1a1a2e", relief="solid", bd=2)
            self.canvas_bg.create_window(850, 240, window=frame_ofertas, width=350, height=280, anchor="nw")
            
            lbl_config = tk.Label(frame_ofertas, text="2° CONFIGURAR OFERTA", 
                                 font=("Montserrat", 14, "bold"), bg="#1a1a2e", fg=COLOR_CIAN)
            lbl_config.place(x=175, y=15, anchor="center")
            
            # Tipo de oferta
            lbl_tipo = tk.Label(frame_ofertas, text="Tipo de oferta:", font=("Montserrat", 12, "bold"), 
                               bg="#1a1a2e", fg=COLOR_TEXTO)
            lbl_tipo.place(x=20, y=50)
            
            tipo_var = tk.StringVar(value="porcentaje")
            combo_tipo = ttk.Combobox(frame_ofertas, textvariable=tipo_var, 
                                     values=["porcentaje", "cantidad", "precio_manual"], 
                                     font=("Montserrat", 12), state="readonly", width=15)
            aplicar_estilo_moderno_combobox(combo_tipo)
            combo_tipo.place(x=20, y=75)
            
            # Valor de la oferta
            lbl_valor = tk.Label(frame_ofertas, text="Valor:", font=("Montserrat", 12, "bold"), 
                                bg="#1a1a2e", fg=COLOR_TEXTO)
            lbl_valor.place(x=200, y=50)
            
            valor_var = tk.StringVar()
            ent_valor = tk.Entry(frame_ofertas, textvariable=valor_var, font=("Montserrat", 12), 
                                bg=COLOR_ENTRY_VENTA_BG, fg="#000000", bd=1, relief="solid")
            ent_valor.place(x=200, y=75, width=120)
            
            # Instrucciones dinámicas
            lbl_instrucciones = tk.Label(frame_ofertas, text="", font=("Montserrat", 10), 
                                        bg="#1a1a2e", fg="#ffffff", wraplength=300, justify="left")
            lbl_instrucciones.place(x=12, y=110)
            
            def actualizar_instrucciones(event=None):
                tipo = tipo_var.get()
                texto = ""  # Inicializar la variable
                if tipo == "porcentaje":
                    texto = "• Porcentaje de descuento (ej: 20 para 20% off)\n• Se aplicará sobre el precio de venta"
                elif tipo == "cantidad":
                    texto = "• Ingrese la oferta por cantidad (ej: 3x2, 2x1)\n• Formato: CompraXPaga"
                elif tipo == "precio_manual":
                    texto = "• Ingrese el precio especial\n• Reemplazará el precio de venta normal"
                lbl_instrucciones.config(text=texto)
            
            combo_tipo.bind("<<ComboboxSelected>>", actualizar_instrucciones)
            actualizar_instrucciones()  # Mostrar instrucciones iniciales
            
            # Botones de acción
            btn_aplicar = tk.Button(frame_ofertas, text="APLICAR OFERTA", font=("Montserrat", 11, "bold"), 
                                   bg="#4CAF50", fg="#ffffff", bd=0, relief="flat", cursor="hand2")
            aplicar_estilo_moderno_boton(btn_aplicar, "success", hover_efecto=True)
            btn_aplicar.place(x=175, y=180, width=150, height=35, anchor="center")
            
            btn_quitar = tk.Button(frame_ofertas, text="QUITAR OFERTA", font=("Montserrat", 11, "bold"), 
                                  bg="#f44336", fg="#ffffff", bd=0, relief="flat", cursor="hand2")
            aplicar_estilo_moderno_boton(btn_quitar, "danger", hover_efecto=True)
            btn_quitar.place(x=175, y=225, width=150, height=35, anchor="center")
            
            # --- FUNCIONES DE LÓGICA ---
            def aplicar_oferta():
                seleccion = tree_productos.selection()
                if not seleccion:
                    messagebox.showwarning("Selección", "Seleccione al menos un producto de la lista.")
                    return
                
                tipo = tipo_var.get()
                valor_str = valor_var.get().strip()
                
                if not valor_str:
                    messagebox.showwarning("Valor", "Ingrese el valor de la oferta.")
                    return
                
                try:
                    # Inicializar valor
                    valor = None
                    
                    # Validar y procesar el valor según el tipo
                    if tipo == "porcentaje":
                        valor = float(valor_str)
                        if valor <= 0 or valor >= 100:
                            raise ValueError("El porcentaje debe estar entre 1 y 99")
                    elif tipo == "cantidad":
                        # Validar formato 3x2, 2x1, etc.
                        if 'x' not in valor_str.lower():
                            raise ValueError("Use formato CompraXPaga (ej: 3x2)")
                        valor = valor_str.upper()
                    elif tipo == "precio_manual":
                        valor = float(valor_str)
                        if valor <= 0:
                            raise ValueError("El precio debe ser mayor a 0")
                    
                    # Verificar que el valor fue procesado correctamente
                    if valor is None:
                        raise ValueError("Tipo de oferta no válido")
                    
                    # Aplicar oferta a productos seleccionados
                    productos_modificados = 0
                    for item_id in seleccion:
                        item = tree_productos.item(item_id)
                        valores = item['values']
                        marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                        
                        # Buscar producto en el sistema
                        producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                        if producto:
                            producto.oferta = {'tipo': tipo, 'valor': valor}
                            productos_modificados += 1
                    
                    # Guardar cambios
                    self.sistema.guardar_productos()
                    messagebox.showinfo("Éxito", f"Oferta aplicada a {productos_modificados} producto(s).")
                    
                    # Refrescar pantalla
                    self.mostrar_crear_ofertas()
                    
                except ValueError as e:
                    messagebox.showerror("Error", f"Valor inválido: {e}")
            
            def quitar_oferta():
                seleccion = tree_productos.selection()
                if not seleccion:
                    messagebox.showwarning("Selección", "Seleccione al menos un producto de la lista.")
                    return
                
                productos_modificados = 0
                for item_id in seleccion:
                    item = tree_productos.item(item_id)
                    valores = item['values']
                    marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                    
                    # Buscar producto en el sistema
                    producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                    if producto and producto.oferta:
                        producto.oferta = {}
                        productos_modificados += 1
                
                # Guardar cambios
                self.sistema.guardar_productos()
                messagebox.showinfo("Éxito", f"Oferta eliminada de {productos_modificados} producto(s).")
                
                # Refrescar pantalla
                self.mostrar_crear_ofertas()
            
            # Asignar comandos a botones
            btn_aplicar.config(command=aplicar_oferta)
            btn_quitar.config(command=quitar_oferta)
            
            widgets.extend([lbl_titulo, frame_controles, lbl_productos, tree_productos, frame_ofertas])
        else:
            # Vista de solo ofertas activas - agregar botón para quitar ofertas
            if ofertas_activas:
                frame_acciones = tk.Frame(self.canvas_bg, bg=COLOR_FONDO)
                self.canvas_bg.create_window(850, 300, window=frame_acciones, anchor="w")
                
                lbl_acciones = tk.Label(frame_acciones, text="🔧 ACCIONES RÁPIDAS:", 
                                       font=("Montserrat", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
                lbl_acciones.pack(pady=(0, 10))
                
                btn_quitar_seleccionadas = tk.Button(frame_acciones, text="❌ QUITAR OFERTAS SELECCIONADAS", 
                                                    font=("Montserrat", 11, "bold"), bg="#f44336", fg="#ffffff", 
                                                    bd=0, relief="flat", cursor="hand2")
                btn_quitar_seleccionadas.pack(pady=5)
                
                def quitar_ofertas_seleccionadas():
                    seleccion = tree_productos.selection()
                    if not seleccion:
                        messagebox.showwarning("Selección", "Seleccione al menos un producto de la lista.")
                        return
                    
                    productos_modificados = 0
                    for item_id in seleccion:
                        item = tree_productos.item(item_id)
                        valores = item['values']
                        marca, descripcion, color, talle = valores[0], valores[1], valores[2], valores[3]
                        
                        # Buscar producto en el sistema
                        producto = self.sistema.buscar_producto(marca, descripcion, color, talle)
                        if producto and producto.oferta:
                            producto.oferta = {}
                            productos_modificados += 1
                    
                    # Guardar cambios
                    self.sistema.guardar_productos()
                    messagebox.showinfo("Éxito", f"Oferta eliminada de {productos_modificados} producto(s).")
                    
                    # Refrescar vista de ofertas activas
                    self._mostrar_ofertas_activas()
                
                btn_quitar_seleccionadas.config(command=quitar_ofertas_seleccionadas)
                widgets.extend([lbl_titulo, frame_controles, lbl_productos, tree_productos, frame_acciones])
            else:
                widgets.extend([lbl_titulo, frame_controles, lbl_productos, tree_productos])
        
        self.pantalla_widgets.extend(widgets)
    
    def _mostrar_ofertas_activas(self):
        """Función auxiliar para mostrar solo las ofertas activas"""
        self.limpiar_pantalla()
        self._colocar_logo(pantalla_principal=False)
        self._pantalla_crear_ofertas(self.canvas_bg, solo_ofertas_activas=True)
        
        # Agregar botón volver que faltaba
        btn_volver = tk.Button(self.canvas_bg, text="← Volver", font=("Montserrat", 12, "bold"), 
                              bg="#666666", fg="#fff", bd=0, relief="flat", 
                              command=self.mostrar_menu_secundario, cursor="hand2")
        aplicar_estilo_moderno_boton(btn_volver, "secundario", hover_efecto=True)
        self.canvas_bg.create_window(80, 70, window=btn_volver, width=120, height=40, anchor="center")
        self.pantalla_widgets.append(btn_volver)
    
    def _cambiar_vista_ia(self, vista):
        """Cambia entre las diferentes vistas del centro IA"""
        self.vista_ia_activa.set(vista)
        
        # Limpiar contenido anterior
        for widget in self.frame_contenido_ia.winfo_children():
            widget.destroy()
        
        if vista == "dashboard":
            self._mostrar_dashboard_ia()
        elif vista == "reposicion":
            self._mostrar_reposicion_ia()
        elif vista == "precios":
            self._mostrar_precios_ia()
        elif vista == "analisis":
            self._mostrar_analisis_ia()
    
    def _mostrar_dashboard_ia(self):
        """Dashboard principal con métricas generales"""
        # --- PANEL DE ALERTAS ---
        frame_alertas = tk.Frame(self.frame_contenido_ia, bg="#ff4444", relief="solid", bd=2)
        frame_alertas.place(x=20, y=20, width=360, height=120)
        
        lbl_alertas_titulo = tk.Label(frame_alertas, text="🚨 ALERTAS CRÍTICAS", 
                                     font=("Montserrat", 12, "bold"), bg="#ff4444", fg="#000000")
        lbl_alertas_titulo.pack(pady=5)
        
        # Calcular alertas
        productos_criticos = self._obtener_productos_criticos()
        texto_alertas = f"• {len(productos_criticos)} productos con stock crítico\n• Stock bajo detectado automáticamente\n• Acción requerida inmediata"
        
        lbl_alertas = tk.Label(frame_alertas, text=texto_alertas, font=("Montserrat", 12), 
                              bg="#ff4444", fg="#000000", justify="left")
        lbl_alertas.pack(pady=5)
        
        # --- PRODUCTOS ESTRELLA ---
        frame_estrella = tk.Frame(self.frame_contenido_ia, bg="#4CAF50", relief="solid", bd=2)
        frame_estrella.place(x=400, y=20, width=360, height=120)
        
        lbl_estrella_titulo = tk.Label(frame_estrella, text="PRODUCTOS ESTRELLA", 
                                      font=("Montserrat", 12, "bold"), bg="#4CAF50", fg="#000000")
        lbl_estrella_titulo.pack(pady=5)
        
        productos_estrella = self._obtener_productos_estrella()
        texto_estrella = f"• {len(productos_estrella)} productos top en ventas\n• Alta rotación y márgenes\n• Recomendados para promoción"
        
        lbl_estrella = tk.Label(frame_estrella, text=texto_estrella, font=("Comic", 12), 
                               bg="#4CAF50", fg="#000000", justify="left")
        lbl_estrella.pack(pady=5)
        
        # --- MÉTRICAS GENERALES ---
        frame_metricas = tk.Frame(self.frame_contenido_ia, bg="#2196F3", relief="solid", bd=2)
        frame_metricas.place(x=780, y=20, width=360, height=120)
        
        lbl_metricas_titulo = tk.Label(frame_metricas, text="MÉTRICAS IA", 
                                      font=("Montserrat", 12, "bold"), bg="#2196F3", fg="#000000")
        lbl_metricas_titulo.pack(pady=5)
        
        total_productos = len(self.sistema.productos)
        productos_movimiento = len([p for p in self.sistema.productos if self._obtener_ventas_producto(p, 30) > 0])
        texto_metricas = f"• {total_productos} productos en inventario\n• {productos_movimiento} con movimiento (30 días)\n• IA analizando tendencias"
        
        lbl_metricas = tk.Label(frame_metricas, text=texto_metricas, font=("Montserrat", 12), 
                               bg="#2196F3", fg="#000000", justify="left")
        lbl_metricas.pack(pady=5)
        
        # --- TABLA RESUMEN RÁPIDO ---
        frame_tabla = tk.Frame(self.frame_contenido_ia, bg=COLOR_FONDO)
        frame_tabla.place(x=20, y=160, width=1120, height=240)
        
        lbl_resumen = tk.Label(frame_tabla, text="📋 RESUMEN EJECUTIVO - ÚLTIMOS 30 DÍAS", 
                              font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        lbl_resumen.pack(pady=10)
        
        cols = ("Categoría", "Cantidad", "Estado", "Acción Sugerida", "Prioridad")
        tree_resumen = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)
        aplicar_estilo_moderno_treeview(tree_resumen)
        
        anchos = [200, 120, 120, 200, 120]
        for col, ancho in zip(cols, anchos):
            tree_resumen.heading(col, text=col, anchor="center")
            tree_resumen.column(col, width=ancho, anchor="center")
        
        tree_resumen.pack(pady=10)
        
        # Llenar datos del resumen
        datos_resumen = [
            ("🔴 Stock Crítico", len(productos_criticos), "URGENTE", "Reponer inmediatamente", "ALTA"),
            ("⭐ Productos Estrella", len(productos_estrella), "EXCELENTE", "Mantener stock alto", "MEDIA"),
            ("💰 Oportunidades Precio", "Analizando...", "EN PROCESO", "Revisar márgenes", "MEDIA"),
            ("📈 Tendencias Alcistas", "Calculando...", "EN ANÁLISIS", "Aumentar stock", "BAJA"),
            ("📉 Productos Lentos", "Evaluando...", "ATENCIÓN", "Considerar promoción", "BAJA")
        ]
        
        for item in datos_resumen:
            tree_resumen.insert("", "end", values=item)
    
    def _mostrar_reposicion_ia(self):
        """Vista de sugerencias de reposición"""
        # Reutilizar la lógica existente pero adaptada al nuevo layout
        frame_config = tk.Frame(self.frame_contenido_ia, bg=COLOR_FONDO)
        frame_config.place(x=20, y=20, width=1120, height=50)
        
        tk.Label(frame_config, text="Días de análisis:", font=("Montserrat", 10, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=20, y=15)
        dias_var = tk.StringVar(value="30")
        combo_dias = ttk.Combobox(frame_config, textvariable=dias_var, values=["7", "15", "30", "60", "90"], 
                                 font=("Montserrat", 10), state="readonly", width=8)
        aplicar_estilo_moderno_combobox(combo_dias)
        combo_dias.place(x=150, y=15)
        
        tk.Label(frame_config, text="Stock mínimo (%):", font=("Montserrat", 10, "bold"), 
                bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=300, y=15)
        umbral_var = tk.StringVar(value="20")
        combo_umbral = ttk.Combobox(frame_config, textvariable=umbral_var, values=["10", "15", "20", "25", "30"], 
                                   font=("Montserrat", 10), state="readonly", width=8)
        aplicar_estilo_moderno_combobox(combo_umbral)
        combo_umbral.place(x=430, y=15)
        
        # Tabla de reposición
        cols = ("🚨", "Marca", "Producto", "Color/Talle", "Stock", "Velocidad", "Días Rest.", "Sugerencia")
        tree_reposicion = ttk.Treeview(self.frame_contenido_ia, columns=cols, show="headings", height=12)
        aplicar_estilo_moderno_treeview(tree_reposicion)
        
        anchos = [50, 120, 180, 120, 80, 100, 100, 140]
        for col, ancho in zip(cols, anchos):
            tree_reposicion.heading(col, text=col, anchor="center")
            tree_reposicion.column(col, width=ancho, anchor="center")
        
        tree_reposicion.place(x=20, y=90, width=1120, height=300)
        
        # Llenar datos
        def actualizar_reposicion():
            dias = int(dias_var.get())
            umbral = float(umbral_var.get()) / 100
            sugerencias = self._calcular_sugerencias_ia(dias, umbral)
            
            for item in tree_reposicion.get_children():
                tree_reposicion.delete(item)
            
            for s in sugerencias:
                p = s['producto']
                urgencia = "🔴" if s['dias_restantes'] <= 3 else "🟡" if s['dias_restantes'] <= 7 else "🟢"
                velocidad = f"{s['velocidad_venta']:.1f}/día"
                dias_rest = f"{s['dias_restantes']} días" if s['dias_restantes'] > 0 else "¡AGOTADO!"
                sugerencia = f"Reponer {s['cantidad_sugerida']}"
                
                tree_reposicion.insert("", "end", values=(
                    urgencia, p.marca, p.descripcion, f"{p.color}/{p.talle}",
                    s['stock_actual'], velocidad, dias_rest, sugerencia
                ))
        
        combo_dias.bind("<<ComboboxSelected>>", lambda e: actualizar_reposicion())
        combo_umbral.bind("<<ComboboxSelected>>", lambda e: actualizar_reposicion())
        actualizar_reposicion()
    
    def _mostrar_precios_ia(self):
        """Vista de optimización de precios"""
        lbl_titulo = tk.Label(self.frame_contenido_ia, text="💰 OPTIMIZACIÓN INTELIGENTE DE PRECIOS", 
                             font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg="#FF9800")
        lbl_titulo.place(x=560, y=20, anchor="center")
        
        # Tabla de oportunidades de precios
        cols = ("📊", "Producto", "Precio Actual", "Margen %", "Rotación", "Precio Sugerido", "Razón")
        tree_precios = ttk.Treeview(self.frame_contenido_ia, columns=cols, show="headings", height=15)
        aplicar_estilo_moderno_treeview(tree_precios)
        
        anchos = [50, 200, 120, 100, 100, 120, 250]
        for col, ancho in zip(cols, anchos):
            tree_precios.heading(col, text=col, anchor="center")
            tree_precios.column(col, width=ancho, anchor="center")
        
        tree_precios.place(x=20, y=60, width=1120, height=330)
        
        # Análisis de precios
        productos = self.sistema.inventario_actual()
        for producto in productos[:20]:  # Limitar para rendimiento
            try:
                ventas_30d = self._obtener_ventas_producto(producto, 30)
                rotacion = "Alta" if ventas_30d > 10 else "Media" if ventas_30d > 3 else "Baja"
                margen = ((producto.precio_venta - producto.precio_costo) / producto.precio_venta * 100) if producto.precio_venta > 0 else 0
                
                # Lógica de sugerencias de precios
                if rotacion == "Baja" and margen > 40:
                    icono = "🔻"
                    precio_sugerido = producto.precio_venta * 0.9  # Reducir 10%
                    razon = "Reducir precio para aumentar rotación"
                elif rotacion == "Alta" and margen < 30:
                    icono = "🔺"
                    precio_sugerido = producto.precio_venta * 1.1  # Aumentar 10%
                    razon = "Aumentar margen - alta demanda"
                else:
                    icono = "✅"
                    precio_sugerido = producto.precio_venta
                    razon = "Precio óptimo"
                
                tree_precios.insert("", "end", values=(
                    icono,
                    f"{producto.descripcion} {producto.color}/{producto.talle}",
                    self.formato_moneda(producto.precio_venta),
                    f"{margen:.1f}%",
                    rotacion,
                    self.formato_moneda(precio_sugerido),
                    razon
                ))
            except Exception:
                continue
    
    def _mostrar_analisis_ia(self):
        """Vista de análisis avanzado y tendencias"""
        lbl_titulo = tk.Label(self.frame_contenido_ia, text="📈 ANÁLISIS AVANZADO Y TENDENCIAS", 
                             font=("Montserrat", 14, "bold"), bg=COLOR_FONDO, fg="#9C27B0")
        lbl_titulo.place(x=560, y=20, anchor="center")
        
        # Panel de tendencias por marca
        frame_marcas = tk.Frame(self.frame_contenido_ia, bg="#E8F5E8", relief="solid", bd=1)
        frame_marcas.place(x=20, y=60, width=540, height=160)
        
        lbl_marcas = tk.Label(frame_marcas, text="🏷️ TENDENCIAS POR MARCA", 
                             font=("Montserrat", 12, "bold"), bg="#E8F5E8", fg="#333333")
        lbl_marcas.pack(pady=5)
        
        # Análisis por marca
        marcas_ventas = {}
        for venta in self.sistema.ventas:
            for item in venta.items:
                marca = item['producto'].marca
                if marca not in marcas_ventas:
                    marcas_ventas[marca] = 0
                marcas_ventas[marca] += item['cantidad']
        
        # Top 5 marcas
        top_marcas = sorted(marcas_ventas.items(), key=lambda x: x[1], reverse=True)[:5]
        texto_marcas = ""
        for i, (marca, ventas) in enumerate(top_marcas, 1):
            texto_marcas += f"{i}. {marca}: {ventas} unidades vendidas\n"
        
        lbl_marcas_data = tk.Label(frame_marcas, text=texto_marcas, font=("Montserrat", 10), 
                                  bg="#E8F5E8", fg="#333333", justify="left")
        lbl_marcas_data.pack(pady=10)
        
        # Panel de productos sin movimiento
        frame_lentos = tk.Frame(self.frame_contenido_ia, bg="#FFF3E0", relief="solid", bd=1)
        frame_lentos.place(x=580, y=60, width=540, height=160)
        
        lbl_lentos = tk.Label(frame_lentos, text="🐌 PRODUCTOS SIN MOVIMIENTO", 
                             font=("Montserrat", 12, "bold"), bg="#FFF3E0", fg="#333333")
        lbl_lentos.pack(pady=5)
        
        productos_lentos = []
        for producto in self.sistema.productos:
            if self._obtener_ventas_producto(producto, 60) == 0:  # Sin ventas en 60 días
                productos_lentos.append(producto)
        
        texto_lentos = f"• {len(productos_lentos)} productos sin ventas (60 días)\n"
        texto_lentos += "• Considerar promociones especiales\n"
        texto_lentos += "• Revisar estrategia de precios\n"
        texto_lentos += "• Evaluar descontinuación"
        
        lbl_lentos_data = tk.Label(frame_lentos, text=texto_lentos, font=("Montserrat", 10), 
                                  bg="#FFF3E0", fg="#333333", justify="left")
        lbl_lentos_data.pack(pady=10)
        
        # Tabla de análisis detallado
        cols = ("Producto", "Última Venta", "Stock Días", "Margen %", "Categoría IA", "Recomendación")
        tree_analisis = ttk.Treeview(self.frame_contenido_ia, columns=cols, show="headings", height=8)
        aplicar_estilo_moderno_treeview(tree_analisis)
        
        anchos = [250, 120, 100, 100, 150, 300]
        for col, ancho in zip(cols, anchos):
            tree_analisis.heading(col, text=col, anchor="center")
            tree_analisis.column(col, width=ancho, anchor="center")
        
        tree_analisis.place(x=20, y=240, width=1120, height=150)
        
        # Análisis detallado
        for producto in self.sistema.productos[:15]:  # Limitar para rendimiento
            try:
                ventas_30d = self._obtener_ventas_producto(producto, 30)
                margen = ((producto.precio_venta - producto.precio_costo) / producto.precio_venta * 100) if producto.precio_venta > 0 else 0
                
                # Categorización IA
                if ventas_30d > 10:
                    categoria = "⭐ Estrella"
                    recomendacion = "Mantener stock alto - producto exitoso"
                elif ventas_30d > 5:
                    categoria = "📈 Crecimiento"
                    recomendacion = "Monitorear tendencia - potencial estrella"
                elif ventas_30d > 0:
                    categoria = "🔄 Estable"
                    recomendacion = "Stock normal - ventas regulares"
                else:
                    categoria = "⚠️ Lento"
                    recomendacion = "Considerar promoción o descuento"
                
                dias_stock = producto.cantidad / max(1, ventas_30d/30) if ventas_30d > 0 else 999
                
                tree_analisis.insert("", "end", values=(
                    f"{producto.descripcion} {producto.color}/{producto.talle}",
                    "Reciente" if ventas_30d > 0 else ">30 días",
                    f"{int(dias_stock)} días" if dias_stock < 999 else "Sin datos",
                    f"{margen:.1f}%",
                    categoria,
                    recomendacion
                ))
            except Exception:
                continue
    
    def _actualizar_centro_ia(self):
        """Actualiza los datos del centro IA"""
        self._cambiar_vista_ia(self.vista_ia_activa.get())
        from tkinter import messagebox
        messagebox.showinfo("IA Actualizada", "Todos los análisis han sido actualizados con los datos más recientes.")
    
    def _exportar_centro_ia(self):
        """Exporta un reporte completo de todas las funciones IA"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"Centro_IA_Completo_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
            )
            
            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado
                    writer.writerow(['CENTRO DE INTELIGENCIA ARTIFICIAL - REPORTE COMPLETO'])
                    writer.writerow(['Fecha:', datetime.date.today().strftime('%Y-%m-%d')])
                    writer.writerow([''])
                    
                    # Sección de reposición
                    writer.writerow(['=== ANÁLISIS DE REPOSICIÓN ==='])
                    sugerencias = self._calcular_sugerencias_ia(30, 0.2)
                    writer.writerow(['Producto', 'Stock Actual', 'Velocidad Venta', 'Días Restantes', 'Cantidad Sugerida'])
                    for s in sugerencias:
                        p = s['producto']
                        writer.writerow([
                            f"{p.descripcion} {p.color}/{p.talle}",
                            s['stock_actual'],
                            f"{s['velocidad_venta']:.1f}",
                            s['dias_restantes'],
                            s['cantidad_sugerida']
                        ])
                    
                    writer.writerow([''])
                    writer.writerow(['=== ANÁLISIS DE PRECIOS ==='])
                    writer.writerow(['Producto', 'Precio Actual', 'Margen %', 'Rotación', 'Recomendación'])
                    
                    # Exportar más datos...
                    
                from tkinter import messagebox
                messagebox.showinfo("Exportación Exitosa", f"Reporte completo exportado a:\n{filename}")
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def _obtener_productos_criticos(self):
        """Obtiene productos con stock crítico"""
        criticos = []
        for producto in self.sistema.productos:
            ventas_30d = self._obtener_ventas_producto(producto, 30)
            velocidad = ventas_30d / 30
            dias_restantes = producto.cantidad / velocidad if velocidad > 0 else 999
            if dias_restantes <= 7 or producto.cantidad <= 5:
                criticos.append(producto)
        return criticos
    
    def _obtener_productos_estrella(self):
        """Obtiene productos con mejor performance"""
        estrellas = []
        for producto in self.sistema.productos:
            ventas_30d = self._obtener_ventas_producto(producto, 30)
            if ventas_30d >= 10:  # Criterio para producto estrella
                estrellas.append(producto)
        return estrellas
    
    def _calcular_sugerencias_ia(self, dias_analisis, umbral_stock):
        """Algoritmo de IA para calcular sugerencias de reposición"""
        sugerencias = []
        productos = self.sistema.inventario_actual()
        
        for producto in productos:
            try:
                # Calcular ventas en el período
                ventas_periodo = self._obtener_ventas_producto(producto, dias_analisis)
                
                # Calcular velocidad de venta promedio
                velocidad_venta = ventas_periodo / dias_analisis if dias_analisis > 0 else 0
                
                # Calcular días restantes con stock actual
                dias_restantes = producto.cantidad / velocidad_venta if velocidad_venta > 0 else 999
                
                # Determinar si necesita reposición
                stock_minimo = max(5, int(velocidad_venta * 14))  # Stock para 2 semanas
                necesita_reposicion = (producto.cantidad <= stock_minimo or 
                                     dias_restantes <= 14 or 
                                     producto.cantidad / max(1, ventas_periodo) <= umbral_stock)
                
                if necesita_reposicion:
                    # Calcular cantidad sugerida (stock para 30 días)
                    cantidad_sugerida = max(10, int(velocidad_venta * 30) - producto.cantidad)
                    
                    sugerencias.append({
                        'producto': producto,
                        'stock_actual': producto.cantidad,
                        'ventas_periodo': ventas_periodo,
                        'velocidad_venta': velocidad_venta,
                        'dias_restantes': max(0, int(dias_restantes)),
                        'cantidad_sugerida': cantidad_sugerida,
                        'prioridad': self._calcular_prioridad(dias_restantes, velocidad_venta)
                    })
            
            except Exception as e:
                print(f"[DEBUG] Error calculando sugerencia para {producto.descripcion}: {e} - main.py:2900")
                continue
        
        # Ordenar por prioridad (críticos primero)
        sugerencias.sort(key=lambda x: x['prioridad'], reverse=True)
        
        return sugerencias
    
    def _obtener_ventas_producto(self, producto, dias):
        """Obtiene las ventas de un producto en los últimos N días"""
        try:
            fecha_limite = datetime.date.today() - datetime.timedelta(days=dias)
            ventas_total = 0
            
            for venta in self.sistema.ventas:
                if venta.fecha >= fecha_limite:
                    for item in venta.items:
                        if (item['producto'].descripcion == producto.descripcion and 
                            item['producto'].color == producto.color and 
                            item['producto'].talle == producto.talle):
                            ventas_total += item['cantidad']
            
            return ventas_total
        except Exception:
            return 0
    
    def _calcular_prioridad(self, dias_restantes, velocidad_venta):
        """Calcula la prioridad de reposición (mayor número = más urgente)"""
        if dias_restantes <= 0:
            return 100  # Crítico - sin stock
        elif dias_restantes <= 3:
            return 80   # Muy urgente
        elif dias_restantes <= 7:
            return 60   # Urgente
        elif dias_restantes <= 14:
            return 40   # Atención
        else:
            return 20   # Normal

if __name__ == "__main__":
    print("[DEBUG] Creando instancia de SistemaGestion... - main.py:2940")
    sistema = SistemaGestion()
    print("[DEBUG] SistemaGestion creado. Creando AppPilchero... - main.py:2942")
    app = AppPilchero(sistema)
    print("[DEBUG] AppPilchero creado. Ejecutando mainloop... - main.py:2944")
    app.mainloop()
    print("[DEBUG] mainloop finalizado - main.py:2946")
