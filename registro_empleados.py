from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from decouple import config
import sql

root = Tk()
root.title("Registro de empleados")
root.geometry("640x350")

# Variables de la tabla
id_t = StringVar()
nombre = StringVar()
cargo = StringVar()
salario = StringVar()

server = config('SERVER')
database = config('DATABASE')
username = config("USER")
password = config("PASSWORD")



connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};' \
                   f'UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'
try:
    conn = sql.connect(connectionString)
    miCursor = conn.cursor()
except pyodbc.Error as e:
    print("error connectandose a la base de datos")


def tabla_existe(tabla, cursor):
    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tabla}'")
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def crear_tabla():
    columnas_tablas = ["ID INT PRIMARY KEY IDENTITY(1,1)", "NOMBRE VARCHAR(50) NOT NULL", "CARGO VARCHAR(50) NOT NULL",
                       "SALARIO INT NOT NULL"]

    try:
        if not tabla_existe("empleados", miCursor):
            sql.create_table("empleados", columnas_tablas, miCursor)
            messagebox.showinfo("Conexion", "Tabla creada exitosamente")
        else:
            messagebox.showinfo("Conexion", "La tabla ya existe")

    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al crear la base de datos o tabla: {e}")
        print("Error al crear la base de datos o tabla:", e)


# ==================Métodos CRUD============================
# Crear registro
def insertar_dato():
    nombre_columnas = ["NOMBRE", "CARGO", "SALARIO"]
    try:
        datos = nombre.get(), cargo.get(), salario.get()
        sql.insert_data("empleados", nombre_columnas, datos, miCursor)

        messagebox.showinfo("Exito", "Registro creado exitosamente")
    except pyodbc.Error as e:
        messagebox.showwarning("Error", f"Ocurrió un error al crear el registro: {e}")

    limpiarCampos()
    mostrar()


# Mostrar registros
def mostrar():
    global b_mostar
    registros = tree.get_children()

    for elemento in registros:
        tree.delete(elemento)

    try:
        rows = sql.get_all_data("empleados", miCursor)
        for row in rows:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))
        print("registros mostrados")
        b_mostar.destroy()
    except pyodbc.Error as e:
        print("Error al mostrar registros:", e)


# Actualizar registro
def actualizar():
    nombre_columnas = ["NOMBRE", "CARGO", "SALARIO"]
    try:
        datos = nombre.get(), cargo.get(), salario.get(), id_t.get()
        sql.update_data("empleados", nombre_columnas, datos, miCursor)
        messagebox.showinfo("Exito", "Registro actualizado exitosamente")

        limpiarCampos()
        mostrar()
    except pyodbc.Error as e:
        messagebox.showwarning("Error", f"Ocurrió un error al actualizar el registro: {e}")


# Eliminar registro
def eliminar():
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            sql.delete_data("empleados", id_t.get(), miCursor)
        else:
            limpiarCampos()
    except pyodbc.Error as e:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro")
        print(e)
        pass

    limpiarCampos()
    mostrar()


# ====================Funciones de los widgets de la ventana==============================
# Eliminar toda la base de datos
def eliminar_bd():
    if messagebox.askyesno(message="Los datos se perderán definitivamente, ¿desea continuar?", title="Advertencia"):
        sql.delete_database("empleados", miCursor)
        messagebox.showinfo("Conexion", "Tabla borrada exitosamente")
        mostrar()
    else:
        pass


def salir_aplicacion():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir?")
    if valor == "yes":
        root.destroy()


def limpiarCampos():
    global b_crear, b_mostar, b_modificar, b_no_modficar, b_eliminar
    id_t.set("")
    nombre.set("")
    cargo.set("")
    salario.set("")

    b_eliminar.destroy()
    b_modificar.destroy()
    b_no_modficar.destroy()

    b_crear = Button(root, text="Crear Registro", command=insertar_dato)
    b_crear.place(x=50, y=90)


def Instrucciones():
    instrucciones = """
        Crear un nuevo empleado: Llena todos los campos con 
        la informacion del nuevo empleado.   
        
        Mostar empleados: Click en el boton mostrar empleados 
        y se desplegara una lista con todos los empelados.
        
        Modficar empleado: Doble Click en el empleado que 
        desaeas modficar, luego modifica los campos que deseas 
        cambiar y dale click a modificar registro o dale click
        en no modificar para limpiar los campos.
        
        Eliminar empleado : Doble Click en el empleado que 
        deseas eliminar, dar click en elboton de eliminar 
        y aceptar en la advertencia.
         
    """

    messagebox.showinfo(title="INSTRUCCIONES", message=instrucciones)

def AcercaDe():
    acerca = """
    Aplicacion CRUD empleados SQL
    Version 1.0.0
    Tecnologias: Python, Tkinter, Pyodbc
    """
    messagebox.showinfo(title="INFORMACION", message=acerca)


# ==================== widgets de la ventana==============================

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear tabla de empleados", command=crear_tabla)
menubasedat.add_command(label="Eliminar tabla de empleados", command=eliminar_bd)
menubasedat.add_command(label="Salir", command=salir_aplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Instrucciones", command=Instrucciones)
ayudamenu.add_command(label="Acerca", command=AcercaDe)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)


# =======================Tabla=======================
tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2'))
tree.place(x=0, y=130)

tree.column('#0', width=100)
tree.heading('#0', text="id", anchor=CENTER)
tree.heading('#1', text="Nombre del empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)

tree.column('#3', width=100)
tree.heading('#3', text="Salario", anchor=CENTER)


def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    id_t.set(tree.item(item, "text"))
    nombre.set(tree.item(item, "values")[0])
    cargo.set(tree.item(item, "values")[1])
    salario.set(tree.item(item, "values")[2])


tree.bind("<Double-1>", seleccionarUsandoClick)

# ===========================Etiquetas y cajas de texto===========================
e1 = Entry(root, textvariable=id_t)

l2 = Label(root, text="Nombre")
l2.place(x=50, y=10)
e2 = Entry(root, textvariable=nombre, width=50)
e2.place(x=100, y=10)

l3 = Label(root, text="Cargo")
l3.place(x=50, y=40)
e3 = Entry(root, textvariable=cargo)
e3.place(x=100, y=40)

l4 = Label(root, text="Salario")
l4.place(x=280, y=40)
e4 = Entry(root, textvariable=salario, width=10)
e4.place(x=320, y=40)

l5 = Label(root, text="USD")
l5.place(x=380, y=40)

# =======================Botones============================
b_crear = Button(root, text="Crear Registro", command=insertar_dato)
b_crear.place(x=50, y=90)
b_mostar = Button(root, text="Mostrar Empleados", command=mostrar)
b_mostar.place(x=180, y=90)

b_eliminar = Button(root, text="Eliminar Registro", bg="red", command=eliminar)

b_modificar = Button(root, text="Modificar Registro", command=actualizar)

b_no_modficar = Button(root, text="No Modificar", command=limpiarCampos)

def seleccionarUsandoClick(event):
    global b_crear, b_mostar, b_modificar, b_no_modficar, b_eliminar
    item = tree.identify('item', event.x, event.y)
    id_t.set(tree.item(item, "text"))
    nombre.set(tree.item(item, "values")[0])
    cargo.set(tree.item(item, "values")[1])
    salario.set(tree.item(item, "values")[2])

    b_mostar.destroy()
    b_crear.destroy()

    b_modificar = Button(root, text="Modificar Registro", command=actualizar)
    b_modificar.place(x=50, y=90)

    b_no_modficar = Button(root, text="No Modificar", command=limpiarCampos)
    b_no_modficar.place(x=180, y=90)

    b_eliminar = Button(root, text="Eliminar Registro", bg="red", command=eliminar)
    b_eliminar.place(x=320, y=90)



tree.bind("<Double-1>", seleccionarUsandoClick)

root.config(menu=menubar)
root.mainloop()
