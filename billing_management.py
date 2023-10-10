import json

class Factura:
    def __init__(self, numero_factura, fecha, cliente, metodo_pago, estado_pago, servicios_adicionales, precio):
        self.numero_factura = numero_factura
        self.fecha = fecha
        self.cliente = cliente
        self.metodo_pago = metodo_pago
        self.estado_pago = estado_pago
        self.servicios_adicionales = servicios_adicionales
        self.precio = precio
    
    def to_dict(self):
        return {
            "NumeroFactura": self.numero_factura,
            "Fecha": self.fecha,
            "Cliente": self.cliente,
            "MetodoPago": self.metodo_pago,
            "EstadoPago": self.estado_pago,
            "ServiciosAdicionales": self.servicios_adicionales,
            "Precio": self.precio
        }

class NodoAVL:
    def __init__(self, factura):
        self.factura = factura
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVLTree:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))
        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))

        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def insert(self, factura):
        if not self.raiz:
            self.raiz = NodoAVL(factura)
        else:
            self.raiz = self._insert(self.raiz, factura)

    def _insert(self, nodo, factura):
        if not nodo:
            return NodoAVL(factura)

        if factura.numero_factura < nodo.factura.numero_factura:
            nodo.izquierda = self._insert(nodo.izquierda, factura)
        elif factura.numero_factura > nodo.factura.numero_factura:
            nodo.derecha = self._insert(nodo.derecha, factura)
        else:
            return nodo  # Factura duplicada

        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

        balance = self.balance(nodo)

        # Rotaciones
        if balance > 1:
            if factura.numero_factura < nodo.izquierda.factura.numero_factura:
                return self.rotar_derecha(nodo)
            else:
                nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
                return self.rotar_derecha(nodo)

        if balance < -1:
            if factura.numero_factura > nodo.derecha.factura.numero_factura:
                return self.rotar_izquierda(nodo)
            else:
                nodo.derecha = self.rotar_derecha(nodo.derecha)
                return self.rotar_izquierda(nodo)

        return nodo

    def eliminar(self, numero_factura):
        if not self.raiz:
            return self.raiz

        if numero_factura < self.raiz.factura.numero_factura:
            self.raiz.izquierda = self.eliminar(numero_factura)
        elif numero_factura > self.raiz.factura.numero_factura:
            self.raiz.derecha = self.eliminar(numero_factura)
        else:
            if not self.raiz.izquierda:
                temp = self.raiz.derecha
                self.raiz = None
                return temp
            elif not self.raiz.derecha:
                temp = self.raiz.izquierda
                self.raiz = None
                return temp

            temp = self.get_min_value_node(self.raiz.derecha)
            self.raiz.factura = temp.factura
            self.raiz.derecha = self.eliminar(temp.factura.numero_factura)

        if not self.raiz:
            return self.raiz

        self.raiz.altura = 1 + max(self.altura(self.raiz.izquierda), self.altura(self.raiz.derecha))
        balance = self.balance(self.raiz)

        if balance > 1:
            if self.balance(self.raiz.izquierda) >= 0:
                return self.rotar_derecha(self.raiz)
            else:
                self.raiz.izquierda = self.rotar_izquierda(self.raiz.izquierda)
                return self.rotar_derecha(self.raiz)

        if balance < -1:
            if self.balance(self.raiz.derecha) <= 0:
                return self.rotar_izquierda(self.raiz)
            else:
                self.raiz.derecha = self.rotar_derecha(self.raiz.derecha)
                return self.rotar_izquierda(self.raiz)

        return self.raiz

    def get_min_value_node(self, nodo):
        if nodo is None or not nodo.izquierda:
            return nodo
        return self.get_min_value_node(nodo.izquierda)

    def buscar(self, numero_factura):
        return self._buscar(self.raiz, numero_factura)

    def _buscar(self, nodo, numero_factura):
        if not nodo:
            return None
        if numero_factura < nodo.factura.numero_factura:
            return self._buscar(nodo.izquierda, numero_factura)
        elif numero_factura > nodo.factura.numero_factura:
            return self._buscar(nodo.derecha, numero_factura)
        else:
            return nodo.factura

    def inorder_traversal(self, nodo):
        if not nodo:
            return []
        return self.inorder_traversal(nodo.izquierda) + [nodo.factura] + self.inorder_traversal(nodo.derecha)

    def to_list(self):
        return self.inorder_traversal(self.raiz)

class BillingManager:
    def __init__(self):
        self.avl_trees = {}

    def cargar_facturas_desde_json(self):
        try:
            with open("facturas.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        for hotel, facturas_data in data.items():
            if hotel not in self.avl_trees:
                self.avl_trees[hotel] = AVLTree()
            
            for factura_data in facturas_data:
                factura = Factura(
                    factura_data["NumeroFactura"],
                    factura_data["Fecha"],
                    factura_data["Cliente"],
                    factura_data["MetodoPago"],
                    factura_data["EstadoPago"],
                    factura_data["ServiciosAdicionales"],
                    factura_data["Precio"]
                )
                self.avl_trees[hotel].insert(factura)
    
    def guardar_facturas_en_json(self):
        data = {}
        for hotel, tree in self.avl_trees.items():
            data[hotel] = [factura.to_dict() for factura in tree.to_list()]

        with open("facturas.json", "w") as file:
            json.dump(data, file, indent=4)

    def insert_factura(self, hotel, factura):
        if hotel not in self.avl_trees:
            self.avl_trees[hotel] = AVLTree()
        self.avl_trees[hotel].insert(factura)

    def eliminar_factura(self, hotel, numero_factura):
        if hotel not in self.avl_trees:
            return

        self.avl_trees[hotel].eliminar(numero_factura)
        self.guardar_facturas_en_json()

    def buscar_factura(self, hotel, numero_factura):
        if hotel in self.avl_trees:
            return self.avl_trees[hotel].buscar(numero_factura)

    def get_facturas(self, hotel):
        if hotel in self.avl_trees:
            return self.avl_trees[hotel].to_list()
        else:
            return []
