import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from employee_management import EmployeeManagementUI, EmployeeManager

# Función para abrir la ventana de gestión de empleados
def open_employee_management(hotel_name):
    root_employee_management = tk.Toplevel(root)
    employee_manager = EmployeeManager(hotel_name)
    employee_management_ui = EmployeeManagementUI(root_employee_management, employee_manager, hotel_name)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Reservaciones")

# Crear pestañas para cada hotel
tab_control = ttk.Notebook(root)

hotel_names = ["Hotel Maravilla", "Hotel Luxury", "Hotel Cali", "Hotel Banana"]  # Lista de nombres de hoteles
print("sexo")
for hotel_name in hotel_names:
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=hotel_name)
    open_button = tk.Button(tab, text=f"Gestionar Empleados - {hotel_name}", command=lambda name=hotel_name: open_employee_management(name))
    open_button.pack(pady=20)

tab_control.pack(expand=1, fill="both")

root.mainloop()

