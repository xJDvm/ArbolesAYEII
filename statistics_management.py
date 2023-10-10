import json
import tkinter as tk
import tkinter.ttk as ttk

# Importar el arreglo de facturas JSON
with open("facturas.json", "r") as f:
    facturas = json.load(f)

# Función para crear un árbol binario de búsqueda a partir de un arreglo de facturas


def crear_arbol_binario(facturas, hotel_name):
    if not facturas:
        return None

    facturas[hotel_name].sort(key=lambda factura: factura["NumeroFactura"])

    nodo_raiz = Nodo(facturas[hotel_name][0])
    for factura in facturas[hotel_name][1:]:
        nodo_raiz.insertar(factura)

    return nodo_raiz

# Clase Nodo para representar un nodo de un árbol binario


class Nodo:
    def __init__(self, factura):
        self.factura = factura
        self.izquierdo = None
        self.derecho = None

    def insertar(self, factura):
        if factura["NumeroFactura"] < self.factura["NumeroFactura"]:
            if self.izquierdo is None:
                self.izquierdo = Nodo(factura)
            else:
                self.izquierdo.insertar(factura)
        else:
            if self.derecho is None:
                self.derecho = Nodo(factura)
            else:
                self.derecho.insertar(factura)

# Función para realizar el recorrido en postorden de un árbol binario


def recorrido_postorden(nodo):
    if nodo is not None:
        recorrido_postorden(nodo.izquierdo)
        recorrido_postorden(nodo.derecho)
        return nodo.factura

# Función para mostrar la ventana con la lista de facturas
class StatisticsUI:
    def __init__(self, root, hotel_name):
        self.root = root
        self.hotel_name = hotel_name
        self.root.title(f"Estadísticas - {self.hotel_name}")

        # Importar el arreglo de facturas JSON
        with open("facturas.json", "r") as f:
            self.facturas = json.load(f)

        # Crear un cuadro de texto para mostrar las estadísticas
        self.stats_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
        self.stats_text.pack(padx=20, pady=10)

        # Crear el botón para mostrar las estadísticas
        self.show_stats_button = ttk.Button(root, text="Mostrar Estadísticas", command=self.mostrar_estadisticas)
        self.show_stats_button.pack(pady=10)

    def mostrar_estadisticas(self):
        # Obtener la cantidad de reservaciones realizadas
        num_reservaciones = len(self.facturas.get(self.hotel_name, []))

        # Obtener la cantidad de dinero facturado
        total_facturado = sum(factura.get("Precio", 0) for factura in self.facturas.get(self.hotel_name, []))

        # Mostrar las estadísticas en el cuadro de texto
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, f"Reservaciones realizadas: {num_reservaciones}\n")
        self.stats_text.insert(tk.END, f"Cantidad de dinero facturado: {total_facturado}\n")

# Mapeo de archivos de empleados por hotel
hotel_file_mapping = {
    "Hotel Maravilla": "hotela.txt",
    "Hotel Luxury": "hotelb.txt",
    "Hotel Cali": "hotelc.txt",
    "Hotel Banana": "hoteld.txt",
}

# Prueba para verificar el funcionamiento independiente del archivo
if __name__ == "__main__":
    root = tk.Tk()
    app = StatisticsUI(root, "Hotel Maravilla")
    root.mainloop()