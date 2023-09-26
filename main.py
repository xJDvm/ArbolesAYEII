import tkinter as tk
from tkinter import ttk, messagebox
from employee_management import EmployeeManagementUI, EmployeeManager
from billingui import BillingUI

# Función para abrir la ventana de gestión de empleados
def open_employee_management(hotel_name):
    root_employee_management = tk.Toplevel(root)
    employee_manager = EmployeeManager(hotel_name)
    employee_management_ui = EmployeeManagementUI(root_employee_management, employee_manager, hotel_name)

# Función para abrir la ventana de facturación
def open_billing(hotel_name):
    # Crea una ventana secundaria para la facturación
    billing_window = tk.Toplevel(root)
    billing_window.title(f"Facturación - {hotel_name}")

    # Inicializa la interfaz de facturación con el nombre del hotel seleccionado
    billing_ui = BillingUI(billing_window, hotel_name)
    # Puedes agregar la lógica para la ventana de facturación aquí

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Reservaciones")

# Crear pestañas para cada hotel
tab_control = ttk.Notebook(root)

hotel_names = ["Hotel Maravilla", "Hotel Luxury", "Hotel Cali", "Hotel Banana"]  # Lista de nombres de hoteles
for hotel_name in hotel_names:
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=hotel_name)

    open_button = tk.Button(tab, text=f"Gestionar Empleados - {hotel_name}", command=lambda name=hotel_name: open_employee_management(name))
    open_button.pack(pady=20)
    
    # Agregar el botón de Facturación en cada pestaña
    billing_button = tk.Button(tab, text=f"Facturación - {hotel_name}", command=lambda name=hotel_name: open_billing(name))
    billing_button.pack(pady=2)

tab_control.pack(expand=1, fill="both")

root.mainloop()
