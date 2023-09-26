from tkinter import *
from tkinter.ttk import *


class StatisticsUI(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Reporte de la Empresa")
        self.geometry("400x300")

        label = Label(self, text="Reporte de la Empresa", font=("Arial", 16))
        label.pack(pady=10)

        report_label = Label(self, text="Ventas: \$100,000")
        report_label.pack()

        profit_label = Label(self, text="Ganancias: \$50,000")
        profit_label.pack()
        self.cargar_tabla_facturacion()

    def cargar_tabla_facturacion(self):
        # Datos de facturacion
        datos = [
            ("Cliente 1", "Tarjeta de Crédito", "\$100"),
            ("Cliente 2", "Transferencia Bancaria", "\$200"),
            ("Cliente 3", "Efectivo", "\$50")
        ]
        # Crea el Treeview
        treeview = Treeview(self, columns=(
            "Nombre", "Método de Pago", "Total"))
        treeview.heading("#0", text="ID")
        treeview.heading("Nombre", text="Nombre")
        treeview.heading("Método de Pago", text="Método de Pago")
        treeview.heading("Total", text="Total")

        # Ajusta el ancho de la columna de ID
        treeview.column("#0", width=30, anchor="center")

        # Ajusta las columnas para que se ajusten automáticamente al contenido
        for column in ("Nombre", "Método de Pago", "Total"):
            treeview.column(column, width=100, anchor="center")
            treeview.heading(column, text=column)

        # Carga los datos en el Treeview
        for idx, dato in enumerate(datos):
            treeview.insert("", "end", text=str(idx + 1), values=dato)

        # Empaqueta el Treeview en la ventana
        treeview.pack()
