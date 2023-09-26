import tkinter as tk
from tkinter import ttk, messagebox
import json

from statistics_management import mostrar_lista

hotel_file_mapping = {
    "Hotel Maravilla": "hotela.txt",
    "Hotel Luxury": "hotelb.txt",
    "Hotel Cali": "hotelc.txt",
    "Hotel Banana": "hoteld.txt",
}


class Employee:
    def __init__(self, name, position, salary, hire_date):
        self.name = name
        self.position = position
        self.salary = salary
        self.hire_date = hire_date


class EmployeeManager:
    def __init__(self, hotel_name):
        self.hotel_name = hotel_name
        self.employees = []
        # El nombre del archivo de datos se basa en el nombre del hotel
        self.file_path = self.get_file_path(hotel_name)

    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_data_to_file()

    def remove_employee(self, name):
        for employee in self.employees:
            if employee.name == name:
                self.employees.remove(employee)
                self.save_data_to_file()
                return True
        return False

    def load_data_from_file(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                for employee_data in data:
                    employee = Employee(
                        employee_data["name"], employee_data["position"], employee_data["salary"], employee_data["hire_date"])
                    self.employees.append(employee)
        except FileNotFoundError:
            pass  # El archivo no existe, se creará cuando se agreguen empleados

    def save_data_to_file(self):
        data = []
        for employee in self.employees:
            data.append({
                "name": employee.name,
                "position": employee.position,
                "salary": employee.salary,
                "hire_date": employee.hire_date
            })
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def get_file_path(self, hotel_name):
        # Obtén la ruta del archivo TXT correspondiente al nombre del hotel desde el diccionario
        if hotel_name in hotel_file_mapping:
            return hotel_file_mapping[hotel_name]
        else:
            raise ValueError(
                f"No se encontró un archivo TXT para el hotel '{hotel_name}'")


class EmployeeManagementUI:
    def __init__(self, root, employee_manager, hotel_name):
        self.root = root
        self.root.title(f"Gestión de Empleados - {hotel_name}")
        self.employee_manager = employee_manager

        # Botones superiores
        self.add_button = tk.Button(
            root, text="Agregar Empleado", command=self.add_employee)
        self.add_button.pack()

        self.remove_button = tk.Button(
            root, text="Eliminar Empleado", command=self.remove_employee)
        self.remove_button.pack()

        self.update_button = tk.Button(
            root, text="Actualizar Tabla", command=self.update_table)
        self.update_button.pack()

        self.statistics_button = tk.Button(
            root, text="Estadisticas", command=lambda: mostrar_lista(hotel_name=hotel_name))
        self.statistics_button.pack()

        def cargar_tabla():
            # Crear tabla con la funcionalidad de ordenar al hacer clic en el encabezado
            self.tree = ttk.Treeview(root, columns=(
                "Nombre", "Posición", "Salario", "Fecha de Contratación"))
            self.tree.heading("#1", text="Nombre",
                              command=lambda: self.sort_column("Nombre", False))
            self.tree.heading(
                "#2", text="Posición", command=lambda: self.sort_column("Posición", False))
            self.tree.heading("#3", text="Salario",
                              command=lambda: self.sort_column("Salario", False))
            self.tree.heading("#4", text="Fecha de Contratación", command=lambda: self.sort_column(
                "Fecha de Contratación", False))
            self.tree.pack()

            # Diccionario para rastrear el estado de ordenamiento de las columnas
            self.sorting_states = {"Nombre": False, "Posición": False,
                                   "Salario": False, "Fecha de Contratación": False}

            self.tree.column("#0", width=0)

            # Cargar datos desde el archivo correspondiente al hotel al iniciar
            self.employee_manager.load_data_from_file()

            # Cargar datos al iniciar
            self.update_table()
        cargar_tabla()

    def sort_column(self, column, reverse):
        items = [(self.tree.set(item, column), item)
                 for item in self.tree.get_children("")]
        items.sort(reverse=reverse)
        for index, (val, item) in enumerate(items):
            self.tree.move(item, "", index)
        self.tree.heading(column, text=column + (" ▲" if reverse else " ▼"),
                          command=lambda: self.sort_column(column, not reverse))
        self.sorting_states[column] = reverse

    def add_employee(self):
        # Crea una ventana secundaria para agregar empleado
        add_employee_window = tk.Toplevel(self.root)
        add_employee_window.title("Agregar Empleado")

        # Etiquetas y campos de entrada en la ventana de agregar empleado
        name_label = tk.Label(add_employee_window, text="Nombre:")
        name_label.pack()

        name_entry = tk.Entry(add_employee_window)
        name_entry.pack()

        position_label = tk.Label(add_employee_window, text="Posición:")
        position_label.pack()

        position_entry = tk.Entry(add_employee_window)
        position_entry.pack()

        salary_label = tk.Label(add_employee_window, text="Salario:")
        salary_label.pack()

        salary_entry = tk.Entry(add_employee_window)
        salary_entry.pack()

        hire_date_label = tk.Label(
            add_employee_window, text="Fecha de Contratación:")
        hire_date_label.pack()

        hire_date_entry = tk.Entry(add_employee_window)
        hire_date_entry.pack()

        # Función para agregar un empleado desde la ventana de agregar empleado
        def add_employee_from_window():
            name = name_entry.get()
            position = position_entry.get()
            salary = salary_entry.get()
            hire_date = hire_date_entry.get()

            if name and position and salary and hire_date:
                employee = Employee(name, position, salary, hire_date)
                self.employee_manager.add_employee(employee)
                self.update_table()  # Actualiza la tabla después de agregar
                add_employee_window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Por favor, complete todos los campos.")

        # Botón para agregar empleado en la ventana de agregar empleado
        add_button = tk.Button(
            add_employee_window, text="Agregar Empleado", command=add_employee_from_window)
        add_button.pack()

    def remove_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Obtiene el nombre del empleado seleccionado en la tabla
            employee_name = self.tree.item(selected_item)["values"][0]
            if self.employee_manager.remove_employee(employee_name):
                self.update_table()  # Actualiza la tabla después de eliminar
            else:
                messagebox.showerror("Error", "Empleado no encontrado.")
        else:
            messagebox.showerror(
                "Error", "Seleccione un empleado de la tabla para eliminar.")

    def update_table(self):
        # Limpia la tabla y los indicadores de orden
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)

        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtiene la lista de empleados y la muestra en la tabla
        for employee in self.employee_manager.employees:
            self.tree.insert("", "end", values=(
                employee.name, employee.position, employee.salary, employee.hire_date))


# Si ejecutas este archivo directamente, crea una ventana de gestión de empleados
if __name__ == "__main__":
    root = tk.Tk()
    hotel_name = "Hotel Maravilla"  # Cambia el nombre del hotel según corresponda
    # Asegúrate de crear una instancia de EmployeeManager con el nombre del hotel
    employee_manager = EmployeeManager(hotel_name)
    employee_management_ui = EmployeeManagementUI(
        root, employee_manager, hotel_name)
    root.mainloop()
