import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Ventana:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos")
        self.root.geometry("1480x400")  # Ajustar la altura de la ventana
        self.root.resizable(True, True)  # Permitir que la ventana sea redimensionable

        # Colores
        self.bg_color = "#fafafa"
        self.label_color = "#34495e"
        self.entry_bg = "#ffffff"
        self.entry_fg = "#2c3e50"
        self.button_bg = "#a2d9ce"
        self.button_fg = "#2c3e50"
        self.button_hover = "#58d68d"

        # Configuración de color de fondo
        self.root.configure(bg=self.bg_color)

        # Conexión a la base de datos
        self.conn = sqlite3.connect('productos_crud.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio_unitario REAL,
            fecha_alta DATE,
            existencia INTEGER,
            unidad_medida TEXT)''')
        self.conn.commit()

        # Crear widgets
        self.create_widgets()

        # Mostrar los productos existentes
        self.mostrar_productos()

    def create_widgets(self):
        # Etiquetas y campos de entrada en una fila horizontal
        frame_formulario = tk.Frame(self.root, bg=self.bg_color)
        frame_formulario.pack(side=tk.TOP, padx=20, pady=20, fill=tk.X)

        # Usar grid para que se ajuste al tamaño de la ventana
        for i in range(12):
            frame_formulario.grid_columnconfigure(i, weight=1)

        # Fila 0, columnas 0 a 11 (campos en horizontal)
        labels = ["Nombre:", "Descripción:", "Precio Unitario:", "Fecha de Alta:", "Existencia:", "Unidad de Medida:"]
        self.entries = []

        # Especificar los tamaños deseados para cada Entry
        entry_sizes = [30, 50, 10, 15, 5, 10]  # Ancho para cada Entry

        for i, (label, size) in enumerate(zip(labels, entry_sizes)):
            tk.Label(frame_formulario, text=label, font=("Arial", 10), bg=self.bg_color, fg=self.label_color).grid(row=0, column=i*2, padx=5, pady=5, sticky="w")
            entry = tk.Entry(frame_formulario, font=("Arial", 10), bg=self.entry_bg, fg=self.entry_fg, width=size)  # Ajustar el ancho aquí
            entry.grid(row=0, column=i*2+1, padx=5, pady=5, sticky="ew")
            self.entries.append(entry)

        # Tabla de productos
        frame_tabla = tk.Frame(self.root, bg=self.bg_color)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.product_tree = ttk.Treeview(frame_tabla, columns=("id", "nombre", "descripcion", "precio", "fecha", "existencia", "unidad"), show="headings", height=10)
        self.product_tree.pack(fill=tk.BOTH, expand=True)

        # Encabezados
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("nombre", text="Nombre")
        self.product_tree.heading("descripcion", text="Descripción")
        self.product_tree.heading("precio", text="Precio Unitario")
        self.product_tree.heading("fecha", text="Fecha de Alta")
        self.product_tree.heading("existencia", text="Existencia")
        self.product_tree.heading("unidad", text="Unidad de Medida")

        # Ajustes de las columnas
        for col in ("id", "nombre", "descripcion", "precio", "fecha", "existencia", "unidad"):
            self.product_tree.column(col, anchor="center", width=120)  # Ajustar el ancho

        self.product_tree.bind("<ButtonRelease-1>", self.seleccionar_producto)
        self.product_tree.bind("<ButtonRelease-3>", self.deseleccionar_producto)  # Botón derecho para deseleccionar

        # Botones
        frame_botones = tk.Frame(self.root, bg=self.bg_color)
        frame_botones.pack(side=tk.BOTTOM, padx=20, pady=10, fill=tk.X)

        self.btn_agregar = self.create_button(frame_botones, "Agregar Producto", self.agregar_producto)
        self.btn_actualizar = self.create_button(frame_botones, "Actualizar Producto", self.actualizar_producto, bg="#f7dc6f")
        self.btn_eliminar = self.create_button(frame_botones, "Eliminar Producto", self.eliminar_producto, bg="#f1948a")
        self.btn_limpiar = self.create_button(frame_botones, "Limpiar Campos", self.limpiar_campos, bg="#bb8fce")

    def create_button(self, parent, text, command, bg=None):
        btn = tk.Button(parent, text=text, command=command, bg=bg or self.button_bg, fg=self.button_fg, font=("Arial", 10), width=15, relief=tk.FLAT, cursor="hand2")
        btn.pack(side=tk.LEFT, padx=5, pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.button_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg or self.button_bg))
        return btn

    def agregar_producto(self):
        # Validación y adición de producto
        nombre = self.entries[0].get()
        descripcion = self.entries[1].get()
        precio = self.entries[2].get()
        fecha = self.entries[3].get()
        existencia = self.entries[4].get()
        unidad = self.entries[5].get()

        if nombre == "" or descripcion == "" or precio == "" or fecha == "" or existencia == "" or unidad == "":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            self.cursor.execute('''INSERT INTO productos (nombre, descripcion, precio_unitario, fecha_alta, existencia, unidad_medida) VALUES (?, ?, ?, ?, ?, ?)''', (nombre, descripcion, float(precio), fecha, int(existencia), unidad))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.mostrar_productos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_productos(self):
        # Eliminar datos previos
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)

        # Obtener productos
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()

        for producto in productos:
            self.product_tree.insert("", tk.END, values=producto)

    def seleccionar_producto(self, event):
        # Obtener el ID del item donde se hizo clic
        item = self.product_tree.identify_row(event.y)
        
        if item:  # Si se hizo clic en un registro
            producto = self.product_tree.item(item, "values")
            if producto:
                for entry, value in zip(self.entries, producto[1:]):
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, value)
        else:  # Si se hizo clic en el área del Treeview sin un registro
            self.product_tree.selection_remove(self.product_tree.selection()) # Remueve la seleccion
            self.limpiar_campos()  # Limpiar los campos de entrada
    
    def deseleccionar_producto(self, event):
        # Limpiar los campos si se hace clic en el área vacía
        if not self.product_tree.identify_row(event.y):  # Si no hay un item seleccionado
            self.limpiar_campos()  # Llamar a la función para limpiar campos
                
    def actualizar_producto(self):
        # Actualizar los datos del producto
        item = self.product_tree.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para actualizar.")
            return

        producto = self.product_tree.item(item, "values")
        id_producto = producto[0]

        nombre = self.entries[0].get()
        descripcion = self.entries[1].get()
        precio = self.entries[2].get()
        fecha = self.entries[3].get()
        existencia = self.entries[4].get()
        unidad = self.entries[5].get()

        if nombre == "" or descripcion == "" or precio == "" or fecha == "" or existencia == "" or unidad == "":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            self.cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, precio_unitario = ?, fecha_alta = ?, existencia = ?, unidad_medida = ? WHERE id = ?''', (nombre, descripcion, float(precio), fecha, int(existencia), unidad, id_producto))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            self.mostrar_productos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        # Eliminar producto seleccionado
        item = self.product_tree.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para eliminar.")
            return

        producto = self.product_tree.item(item, "values")
        id_producto = producto[0]

        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?")
        if confirmacion:
            try:
                self.cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.mostrar_productos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        for entry in self.entries:
            entry.delete(0, tk.END)

    def __del__(self):
        # Cerrar la conexión a la base de datos al cerrar la ventana
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana(root)
    root.mainloop()
