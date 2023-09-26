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


def mostrar_lista(hotel_name):
    # Crear la ventana
    ventana = tk.Toplevel()
    ventana.title("Lista de facturas")

    # Crear el árbol binario de búsqueda
    nodo_raiz = crear_arbol_binario(facturas, hotel_name)

    # Realizar el recorrido en postorden del árbol binario
    lista_facturas = recorrido_postorden(nodo_raiz)

    # Crear el árbol binario de búsqueda
    columnas = ["Número de factura", "Cliente", "Método de pago",
                "Estado de pago", "Servicios adicionales"]
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    tree.pack()
    # Agregar las cabeceras de la tabla
    for i in range(len(columnas)):
        tree.heading(i, text=columnas[i])
    # Agregar los datos a la tabla
    for factura in lista_facturas:
        print(factura)
        tree.insert('', 'end', values=(
            lista_facturas["NumeroFactura"], lista_facturas["Cliente"], lista_facturas["MetodoPago"], lista_facturas["EstadoPago"], lista_facturas["ServiciosAdicionales"]))
