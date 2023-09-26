import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkcalendar import DateEntry
from tkinter import scrolledtext
from billing_management import BillingManager, Factura

class BillingUI:
    def __init__(self, root, hotel_name):
        self.root = root
        self.hotel_name = hotel_name
        self.billing_manager = BillingManager()
        self.billing_manager.cargar_facturas_desde_json()  # Cargar facturas para todos los hoteles
        self.root.title(f"Facturación - {self.hotel_name}")

        self.create_widgets()
        self.load_facturas_to_table()

    def create_widgets(self):
        self.load_button = ttk.Button(self.root, text="Cargar Facturas", command=self.load_facturas_to_table)
        self.load_button.pack(pady=10)
        
        self.factura_frame = ttk.LabelFrame(self.root, text="Factura")
        self.factura_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.create_table()
        self.create_buttons()

    def create_table(self):
        columns = ("Número de Factura", "Fecha", "Cliente", "Método de Pago", "Estado de Pago", "Servicios Adicionales")
        self.table = ttk.Treeview(self.factura_frame, columns=columns, show="headings")
        self.table.heading("Número de Factura", text="Número de Factura")
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Cliente", text="Cliente")
        self.table.heading("Método de Pago", text="Método de Pago")
        self.table.heading("Estado de Pago", text="Estado de Pago")
        self.table.heading("Servicios Adicionales", text="Servicios Adicionales")
        
        for col in columns:
            self.table.column(col, width=120, anchor="center")
        
        self.table.pack(fill="both", expand=True)
        
        self.table.bind("<ButtonRelease-1>", self.on_table_click)
    
    def create_buttons(self):
        self.add_button = ttk.Button(self.root, text="Agregar Factura", command=self.add_factura)
        self.add_button.pack(pady=10)
        
        self.delete_button = ttk.Button(self.root, text="Eliminar Factura", command=self.delete_factura)
        self.delete_button.pack(pady=10)
        
        self.update_button = ttk.Button(self.root, text="Actualizar Tabla", command=self.load_facturas_to_table)
        self.update_button.pack(pady=10)
        
        self.save_button = ttk.Button(self.root, text="Guardar Facturas", command=self.save_facturas)
        self.save_button.pack(pady=10)

    def add_factura(self):
        # Crear una ventana secundaria para el formulario
        factura_window = tk.Toplevel(self.root)
        factura_window.title("Agregar Factura")
        
        # Crear un marco para el formulario
        form_frame = ttk.LabelFrame(factura_window, text="Nueva Factura")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Etiquetas y campos de entrada para el formulario
        numero_label = ttk.Label(form_frame, text="Número de Factura:")
        numero_label.grid(row=0, column=0, padx=5, pady=5)
        numero_entry = ttk.Entry(form_frame)
        numero_entry.grid(row=0, column=1, padx=5, pady=5)
        
        fecha_label = ttk.Label(form_frame, text="Fecha:")
        fecha_label.grid(row=1, column=0, padx=5, pady=5)
        fecha_entry = DateEntry(form_frame)
        fecha_entry.grid(row=1, column=1, padx=5, pady=5)
        
        cliente_label = ttk.Label(form_frame, text="Cliente:")
        cliente_label.grid(row=2, column=0, padx=5, pady=5)
        cliente_entry = ttk.Entry(form_frame)
        cliente_entry.grid(row=2, column=1, padx=5, pady=5)
        
        metodo_pago_label = ttk.Label(form_frame, text="Método de Pago:")
        metodo_pago_label.grid(row=3, column=0, padx=5, pady=5)
        metodo_pago_entry = ttk.Entry(form_frame)
        metodo_pago_entry.grid(row=3, column=1, padx=5, pady=5)
        
        estado_pago_label = ttk.Label(form_frame, text="Estado de Pago:")
        estado_pago_label.grid(row=4, column=0, padx=5, pady=5)
        estado_pago_entry = ttk.Entry(form_frame)
        estado_pago_entry.grid(row=4, column=1, padx=5, pady=5)
        
        servicios_label = ttk.Label(form_frame, text="Servicios Adicionales:")
        servicios_label.grid(row=5, column=0, padx=5, pady=5)
        servicios_entry = scrolledtext.ScrolledText(form_frame, width=30, height=4)
        servicios_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Función para agregar la nueva factura
        def agregar_nueva_factura():
            numero = numero_entry.get()
            fecha = fecha_entry.get()
            cliente = cliente_entry.get()
            metodo_pago = metodo_pago_entry.get()
            estado_pago = estado_pago_entry.get()
            servicios_adicionales = servicios_entry.get("1.0", tk.END)
            
            if numero and fecha and cliente and metodo_pago and estado_pago:
                nueva_factura = Factura(numero, fecha, cliente, metodo_pago, estado_pago, servicios_adicionales)
                self.billing_manager.insert_factura(self.hotel_name, nueva_factura)
                self.load_facturas_to_table()
                factura_window.destroy()
                self.save_facturas()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
        
        # Botón para agregar la factura
        agregar_button = ttk.Button(form_frame, text="Agregar Factura", command=agregar_nueva_factura)
        agregar_button.grid(row=6, columnspan=2, padx=5, pady=10)
    
    def delete_factura(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una factura para eliminar.")
            return
        
        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta factura?")
        if confirmacion:
            numero_factura = self.table.item(selected_item, "values")[0]
            self.billing_manager.eliminar_factura(self.hotel_name, numero_factura)
            self.load_facturas_to_table()
            self.save_facturas()
            
    def load_facturas_to_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        facturas = self.billing_manager.get_facturas(self.hotel_name)
        for factura in facturas:
            self.table.insert("", "end", values=(factura.numero_factura, factura.fecha, factura.cliente,
                                                 factura.metodo_pago, factura.estado_pago, factura.servicios_adicionales))
    
    def save_facturas(self):
        self.billing_manager.guardar_facturas_en_json()
    
    def on_table_click(self, event):
        selected_item = self.table.selection()
        if selected_item:
            numero_factura = self.table.item(selected_item, "values")[0]
            factura = self.billing_manager.buscar_factura(self.hotel_name, numero_factura)
            if factura:
                self.show_factura_info(factura)
    
    def show_factura_info(self, factura):
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Detalles de la Factura - {factura.numero_factura}")
        
        info_frame = ttk.LabelFrame(info_window, text=f"Factura #{factura.numero_factura}")
        info_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=50, height=10)
        info_text.pack(padx=10, pady=10)
        
        info_text.insert("insert", f"Número de Factura: {factura.numero_factura}\n")
        info_text.insert("insert", f"Fecha: {factura.fecha}\n")
        info_text.insert("insert", f"Cliente: {factura.cliente}\n")
        info_text.insert("insert", f"Método de Pago: {factura.metodo_pago}\n")
        info_text.insert("insert", f"Estado de Pago: {factura.estado_pago}\n")
        info_text.insert("insert", f"Servicios Adicionales: {factura.servicios_adicionales}\n")
        
        info_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingUI(root, "Hotel Maravilla")
    root.mainloop()
