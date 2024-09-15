from tkinter import *
from tkinter import messagebox,ttk
from ttkthemes import ThemedStyle
from PIL import Image,ImageTk
from flask import Flask,render_template,redirect,url_for,request,jsonify
import tkinter as tk
import sqlite3,threading,webbrowser

conexion=sqlite3.connect("usuarios.db")
DATABASE = 'productos.db'

def base_de_datos():
    tienda_sql = sqlite3.connect(DATABASE)
    return tienda_sql

stop_event = threading.Event()
server_ready = threading.Event()

color_login="#F0F0F0"
color_login2="#EEEEEE"
color_usuario="#E4D8AF"
color_admin="#CEEAD1"
font_programa=("Calibri",16)
font_admin=("Calibri",18)
tamaño_boton=20

def mis_estilos():
    global estilos
    estilos=ttk.Style()
    estilos.theme_use("alt")
    estilos.configure("boton_admin.TButton",background=color_login,font=font_programa,relief=FLAT,border=0)
    estilos.map("boton_admin.TButton",background=[("pressed",color_login2),("active",color_login2)])
    return estilos

def centrar_ventana(ventana,ancho_ventana,largo_ventana):
    ancho = ventana.winfo_screenwidth()
    largo = ventana.winfo_screenheight()
    x = (ancho // 2) - (ancho_ventana//2)
    y = (largo //2) - (largo_ventana//2)
    ventana.geometry(f"{ancho_ventana}x{largo_ventana}+{x}+{y}")

def ventana_login():
    global ventana_login,mi_imagen,mi_imagen_user,imagen_mostrar,imagen_esconder,entry_usuario,entry_contraseña
    ventana_login=Tk()
    ventana_login.state("zoomed")
    centrar_ventana(ventana_login,1400,800)
    ventana_login.title("Divina Amarga")
    ventana_login.config(bg=color_login)
    ventana_login.iconbitmap("zapato.ico")

    frame_login=Frame(ventana_login,bg=color_login)
    frame_login.pack(side=RIGHT,ipadx=200,ipady=400)
    imagen=Image.open("Imagen_login6.jpg")
    ancho,alto=800,700
    tamaño_imagen=imagen.resize((ancho,alto))
    mi_imagen=ImageTk.PhotoImage(tamaño_imagen)
    label_imagen=Label(frame_login,image=mi_imagen)
    label_imagen.pack(side=LEFT)

    imagen_user=Image.open("user.jpg")
    ancho,alto=100,100
    tamaño_user=imagen_user.resize((ancho,alto))
    mi_imagen_user=ImageTk.PhotoImage(tamaño_user)
    label_imagen_user=Label(frame_login,image=mi_imagen_user)
    label_imagen_user.pack(side=RIGHT,pady=(0,400),padx=(0,220))

    def show():
        if entry_contraseña.get()!="":
            boton_hide=Button(frame_login,image=imagen_esconder,bg=color_login,command=hide)
            boton_hide.place(anchor="center",relx=0.9,rely=0.54)
            entry_contraseña.config(show="")
    def hide():
        if entry_contraseña.get()!="":
            boton_show=Button(frame_login,image=imagen_mostrar,bg=color_login,command=show)
            boton_show.place(anchor="center",relx=0.9,rely=0.54)
            entry_contraseña.config(show="*")
    
    mostrar=Image.open("visible.png")
    esconder=Image.open("not_visible.png")
    ancho,alto=20,20
    tamaño_mostrar=mostrar.resize((ancho,alto))
    tamaño_esconder=esconder.resize((ancho,alto))
    imagen_mostrar=ImageTk.PhotoImage(tamaño_mostrar)
    imagen_esconder=ImageTk.PhotoImage(tamaño_esconder)

    label_usuario=Label(frame_login,text="Usuario",bg=color_login,font=font_programa)
    label_usuario.place(anchor="center",relx=0.800,rely=0.355)
    entry_usuario=Entry(frame_login,font=font_programa)
    entry_usuario.place(anchor="center",relx=0.794,rely=0.415,width=244)
    label_contraseña=Label(frame_login,text="Contraseña",bg=color_login,font=font_programa)
    label_contraseña.place(anchor="center",relx=0.800,rely=0.470)
    entry_contraseña=Entry(frame_login,show="*",font=font_programa)
    entry_contraseña.place(anchor="center",relx=0.794,rely=0.54,width=244)
    boton_show=Button(frame_login,image=imagen_mostrar,bg=color_login,command=show)
    boton_show.place(anchor="center",relx=0.9,rely=0.54)

    boton_login=Button(frame_login,text="Ingresar",bg=color_login,font=font_programa,command=usuario)
    boton_login.place(anchor="center",relx=0.794,rely=0.620,width=244)
    boton_nuevo_usuario=Button(frame_login,text="Registrar",bg=color_login,font=font_programa,command=nuevo_usuario)
    boton_nuevo_usuario.place(anchor="center",relx=0.794,rely=0.700,width=244)

    ventana_login.mainloop()

def ventana_cliente():
    global root
    ventana_login.destroy()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    server_ready.wait()
    webbrowser.open("http://127.0.0.1:5000/Divina_Amarga")
    """
    root=tk.Tk()
    root.withdraw()
    root.protocole("WM_DELETE_WINDOW", handle_window_close)
    
def handle_window_close():
    # Aquí puedes realizar acciones antes de que la ventana se cierre
    # Por ejemplo, detener el hilo o guardar datos
    print("evento iniciado")
    stop_event.set()
    root.destroy()
    """
    
def run_flask():
    web = Flask(__name__)
    @web.route("/Divina_Amarga")
    def web_cliente():
        return render_template("index.html")

    @web.route("/Divina_Amarga/botas_negras")
    def botas_negras():
        return render_template("botas_negras.html")

    server_ready.set()
    while not stop_event.is_set():
        web.run(debug=True, use_reloader=False, port=5000)
    print("Hilo detenido correctamente")
    """
    @web.route("/Divina_Amarga/compra",methods=['POST'])
    def realizar_compra():
        data=request.json
        tienda_sql=base_de_datos()
        tabla_carrito=tienda_sql.cursor()
        for item in data['carrito']:
            tabla_carrito.execute("INSERT INTO carrito(producto_id,nombre_producto,talle,color,cantidad,precio,total) VALUES (?,?,?,?,?,?)",(item['producto_id'],item['nombre_producto'],item['talle'],item['color'],item['cantidad'],item['precio'],item['total']))
        tienda_sql.commit()
        tienda_sql.close()
        return jsonify({"message": "Compra realizada con éxito"}),201
    """
def ventana_admin():
    global ventana_admin,frame_clientes,frame_stock,frame_ventas,frame_compras,frame_proveedores,frame_config
    ventana_login.destroy()
    ventana_admin=Tk()
    style = ThemedStyle(ventana_admin)
    style.set_theme("elegance")
    mis_estilos()
    ventana_admin.state("zoomed")
    centrar_ventana(ventana_admin,1400,800)
    ventana_admin.title("Administración")
    ventana_admin.config(bg=color_admin)
    ventana_admin.iconbitmap("zapato.ico")

    frame_botones_admin=Frame(ventana_admin,bg=color_login)
    frame_botones_admin.pack(fill=X)

    def ver_clientes():
        borrar_frames()
        if "frame_clientes" not in globals():
            clientes()
        else:
            frame_clientes.pack(fill=BOTH,expand=1)
    boton_clientes=ttk.Button(frame_botones_admin,text="Clientes",width=tamaño_boton,style="boton_admin.TButton",command=ver_clientes)
    boton_clientes.pack(side=LEFT)
    def ver_stock():
        borrar_frames()
        if "frame_stock" not in globals():
            stock()
        else:
            frame_stock.pack(fill=BOTH,expand=1)
    boton_stock=ttk.Button(frame_botones_admin,text="Stock",width=tamaño_boton,style="boton_admin.TButton",command=ver_stock)
    boton_stock.pack(side=LEFT)
    def ver_ventas():
        borrar_frames()
        if "frame_ventas" not in globals():
            ventas()
        else:
            frame_ventas.pack(fill=BOTH,expand=1)
    boton_ventas=ttk.Button(frame_botones_admin,text="Ventas",width=tamaño_boton,style="boton_admin.TButton",command=ver_ventas)
    boton_ventas.pack(side=LEFT)
    def ver_compras():
        borrar_frames()
        if "frame_compras" not in globals():
            compras()
        else:
            frame_compras.pack(fill=BOTH,expand=1)
    boton_compras=ttk.Button(frame_botones_admin,text="Compras",width=tamaño_boton,style="boton_admin.TButton",command=ver_compras)
    boton_compras.pack(side=LEFT)
    def ver_proveedores():
        borrar_frames()
        if "frame_proveedores" not in globals():
            proveedores()
        else:
            frame_proveedores.pack(fill=BOTH,expand=1)
    boton_proveedores=ttk.Button(frame_botones_admin,text="Proveedores",width=tamaño_boton,style="boton_admin.TButton",command=ver_proveedores)
    boton_proveedores.pack(side=LEFT)
    def ver_config():
        borrar_frames()
        if "frame_config" not in globals():
            config()
        else:
            frame_config.pack(fill=BOTH,expand=1)
    boton_config=ttk.Button(frame_botones_admin,text="Configuración",width=tamaño_boton,style="boton_admin.TButton",command=ver_config)
    boton_config.pack(side=LEFT)

def borrar_frames():
    if "frame_clientes" in globals():
        frame_clientes.pack_forget()
    if "frame_stock" in globals():
        frame_stock.pack_forget()
    if "frame_ventas" in globals():
        frame_ventas.pack_forget()
    if "frame_compras" in globals():
        frame_compras.pack_forget()
    if "frame_proveedores" in globals():
        frame_proveedores.pack_forget()
    if "frame_config" in globals():
        frame_config.pack_forget()
    
def clientes():
    global frame_clientes
    frame_clientes=Frame(ventana_admin,bg=color_admin)
    frame_clientes.pack(fill=BOTH,expand=1)
    frame_botones_clientes=Frame(frame_clientes,bg=color_login)
    frame_botones_clientes.pack(side=LEFT,fill=Y)
    label_clientes=Label(frame_clientes,text="Clientes",bg=color_admin,font=font_admin)
    label_clientes.pack()

    def selectLista(event):
        if lista_clientes.curselection():
            boton_buscar_cliente.config(state=tk.DISABLED)
            boton_guardar_cliente.config(state=tk.NORMAL)
            boton_modificar_cliente.config(state=tk.NORMAL)
            boton_eliminar_cliente.config(state=tk.NORMAL)
    lista_clientes=Listbox(frame_clientes,width=40,heigh=20,font=("Calibri",14))
    lista_clientes.place(x=550,y=50)
    lista_clientes.insert(1,"Opción 1")
    lista_clientes.insert(2,"Opción 2")
    lista_clientes.insert(3,"Opción 3")
    lista_clientes.bind("<<ListboxSelect>>",selectLista)

    boton_buscar_cliente=ttk.Button(frame_botones_clientes,text="Buscar",style="boton_admin.TButton",state=tk.NORMAL)
    boton_buscar_cliente.pack(ipady=20)
    boton_guardar_cliente=ttk.Button(frame_botones_clientes,text="Guardar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_guardar_cliente.pack(ipady=20)
    boton_modificar_cliente=ttk.Button(frame_botones_clientes,text="Modificar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_modificar_cliente.pack(ipady=20)
    def eliminarClientes():
        Id=entryClientesId.get()
        datos=(Id,)
        tabla=conexion.cursor()
        tabla.execute("DELETE FROM clientes WHERE Id=?",datos)
        conexion.commit()
        messagebox.showinfo("Sistema","Eliminado con éxito!")
    boton_eliminar_cliente=ttk.Button(frame_botones_clientes,text="Eliminar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_eliminar_cliente.pack(ipady=20)

def stock():
    global frame_stock
    frame_stock=Frame(ventana_admin,bg=color_admin)
    frame_stock.pack(fill=BOTH,expand=1)
    frame_botones_stock=Frame(frame_stock,bg=color_login)
    frame_botones_stock.pack(side=LEFT,fill=Y)
    label_stock=Label(frame_stock,text="Stock",bg=color_admin,font=font_admin)
    label_stock.pack()

    def select_lista_stock(event):
        if lista_stock.curselection():
            boton_buscar_stock.config(state=tk.DISABLED)
            boton_guardar_stock.config(state=tk.NORMAL)
            boton_modificar_stock.config(state=tk.NORMAL)
            boton_eliminar_stock.config(state=tk.NORMAL)
    lista_stock=Listbox(frame_stock,width=40,heigh=20,font=("Calibri",14))
    lista_stock.place(x=550,y=50)
    lista_stock.insert(1,"Opción 1")
    lista_stock.insert(2,"Opción 2")
    lista_stock.insert(3,"Opción 3")
    lista_stock.bind("<<ListboxSelect>>",select_lista_stock)

    boton_buscar_stock=ttk.Button(frame_botones_stock,text="Buscar",style="boton_admin.TButton",state=tk.NORMAL)
    boton_buscar_stock.pack(ipady=20)
    boton_guardar_stock=ttk.Button(frame_botones_stock,text="Guardar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_guardar_stock.pack(ipady=20)
    boton_modificar_stock=ttk.Button(frame_botones_stock,text="Modificar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_modificar_stock.pack(ipady=20)
    boton_eliminar_stock=ttk.Button(frame_botones_stock,text="Eliminar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_eliminar_stock.pack(ipady=20)

def ventas():
    global frame_ventas
    frame_ventas=Frame(ventana_admin,bg=color_admin)
    frame_ventas.pack(fill=BOTH,expand=1)
    frame_botones_ventas=Frame(frame_ventas,bg=color_login)
    frame_botones_ventas.pack(side=LEFT,fill=Y)
    label_ventas=Label(frame_ventas,text="Ventas",bg=color_admin,font=font_admin)
    label_ventas.pack()

    def select_lista_ventas(event):
        if lista_ventas.curselection():
            boton_buscar_ventas.config(state=tk.DISABLED)
            boton_guardar_ventas.config(state=tk.NORMAL)
            boton_modificar_ventas.config(state=tk.NORMAL)
            boton_eliminar_ventas.config(state=tk.NORMAL)
    lista_ventas=Listbox(frame_ventas,width=40,heigh=20,font=("Calibri",14))
    lista_ventas.place(x=550,y=50)
    lista_ventas.insert(1,"Opción 1")
    lista_ventas.insert(2,"Opción 2")
    lista_ventas.insert(3,"Opción 3")
    lista_ventas.bind("<<ListboxSelect>>",select_lista_ventas)

    boton_buscar_ventas=ttk.Button(frame_botones_ventas,text="Buscar",style="boton_admin.TButton",state=tk.NORMAL)
    boton_buscar_ventas.pack(ipady=20)
    boton_guardar_ventas=ttk.Button(frame_botones_ventas,text="Guardar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_guardar_ventas.pack(ipady=20)
    boton_modificar_ventas=ttk.Button(frame_botones_ventas,text="Modificar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_modificar_ventas.pack(ipady=20)
    boton_eliminar_ventas=ttk.Button(frame_botones_ventas,text="Eliminar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_eliminar_ventas.pack(ipady=20)

def compras():
    global frame_compras
    frame_compras=Frame(ventana_admin,bg=color_admin)
    frame_compras.pack(fill=BOTH,expand=1)
    frame_botones_compras=Frame(frame_compras,bg=color_login)
    frame_botones_compras.pack(side=LEFT,fill=Y)
    label_compras=Label(frame_compras,text="Compras",bg=color_admin,font=font_admin)
    label_compras.pack()

    def select_lista_compras(event):
        if lista_compras.curselection():
            boton_buscar_compras.config(state=tk.DISABLED)
            boton_guardar_compras.config(state=tk.NORMAL)
            boton_modificar_compras.config(state=tk.NORMAL)
            boton_eliminar_compras.config(state=tk.NORMAL)
    lista_compras=Listbox(frame_compras,width=40,heigh=20,font=("Calibri",14))
    lista_compras.place(x=550,y=50)
    lista_compras.insert(1,"Opción 1")
    lista_compras.insert(2,"Opción 2")
    lista_compras.insert(3,"Opción 3")
    lista_compras.bind("<<ListboxSelect>>",select_lista_compras)

    boton_buscar_compras=ttk.Button(frame_botones_compras,text="Buscar",style="boton_admin.TButton",state=tk.NORMAL)
    boton_buscar_compras.pack(ipady=20)
    boton_guardar_compras=ttk.Button(frame_botones_compras,text="Guardar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_guardar_compras.pack(ipady=20)
    boton_modificar_compras=ttk.Button(frame_botones_compras,text="Modificar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_modificar_compras.pack(ipady=20)
    boton_eliminar_compras=ttk.Button(frame_botones_compras,text="Eliminar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_eliminar_compras.pack(ipady=20)

def proveedores():
    global frame_proveedores
    frame_proveedores=Frame(ventana_admin,bg=color_admin)
    frame_proveedores.pack(fill=BOTH,expand=1)
    frame_botones_proveedores=Frame(frame_proveedores,bg=color_login)
    frame_botones_proveedores.pack(side=LEFT,fill=Y)
    label_proveedores=Label(frame_proveedores,text="Proveedores",bg=color_admin,font=font_admin)
    label_proveedores.pack()

    def select_lista_proveedores(event):
        if lista_proveedores.curselection():
            boton_buscar_proveedores.config(state=tk.DISABLED)
            boton_guardar_proveedores.config(state=tk.NORMAL)
            boton_modificar_proveedores.config(state=tk.NORMAL)
            boton_eliminar_proveedores.config(state=tk.NORMAL)
    lista_proveedores=Listbox(frame_proveedores,width=40,heigh=20,font=("Calibri",14))
    lista_proveedores.place(x=550,y=50)
    lista_proveedores.insert(1,"Opción 1")
    lista_proveedores.insert(2,"Opción 2")
    lista_proveedores.insert(3,"Opción 3")
    lista_proveedores.bind("<<ListboxSelect>>",select_lista_proveedores)

    boton_buscar_proveedores=ttk.Button(frame_botones_proveedores,text="Buscar",style="boton_admin.TButton",state=tk.NORMAL)
    boton_buscar_proveedores.pack(ipady=20)
    boton_guardar_proveedores=ttk.Button(frame_botones_proveedores,text="Guardar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_guardar_proveedores.pack(ipady=20)
    boton_modificar_proveedores=ttk.Button(frame_botones_proveedores,text="Modificar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_modificar_proveedores.pack(ipady=20)
    boton_eliminar_proveedores=ttk.Button(frame_botones_proveedores,text="Eliminar",style="boton_admin.TButton",state=tk.DISABLED)
    boton_eliminar_proveedores.pack(ipady=20)

def config():
    global frame_config
    frame_config=Frame(ventana_admin,bg=color_admin)
    frame_config.pack(fill=BOTH,expand=1)
    label_config=Label(frame_config,text="Configuración",bg=color_admin,font=font_admin)
    label_config.pack()

def usuario():
    if(entry_usuario.get()=="" and entry_contraseña.get()==""):
        messagebox.showwarning("Ventana","Complete todos los campos")
    else:
        if(entry_usuario.get()=="admin@gmail.com" and entry_contraseña.get()=="123456"):
            ventana_admin()
        else:
            datos=(entry_usuario.get(),entry_contraseña.get())
            tabla=conexion.cursor()
            sql="SELECT correo,contraseña FROM user WHERE correo=? and contraseña=?"
            tabla.execute(sql,datos)
            datos_buscados=tabla.fetchall()
            conexion.commit()
            tabla.close()
            if any((entry_usuario.get(),entry_contraseña.get()) == tupla for tupla in datos_buscados):
                ventana_cliente()
            else:
                entry_usuario.delete(0,END)
                entry_contraseña.delete(0,END)
                messagebox.showwarning("Ventana","Usuario o contraseña incorrectos")

def guardar_usuario():
    if(entry_nuevo_usuario.get()!="" and entry_nueva_contraseña.get()!=""):
        datos=(entry_nuevo_usuario.get(),entry_nueva_contraseña.get())
        tabla=conexion.cursor()
        sql="INSERT INTO user(correo,contraseña) VALUES (?,?)"
        tabla.execute(sql,datos)
        conexion.commit()
        tabla.close()
        messagebox.showinfo("Ventana","Usuario guardado correctamente")
        ventana_usuario.destroy()
    else:
        ventana_usuario.destroy()
        messagebox.showwarning("Ventana","Complete todos los campos")

def nuevo_usuario():
    global entry_nuevo_usuario,entry_nueva_contraseña,ventana_usuario
    ventana_usuario=Tk()
    ventana_usuario.title("Nuevo usuario")
    ventana_usuario.iconbitmap("zapato.ico")
    centrar_ventana(ventana_usuario,500,400)
    ventana_usuario.config(bg=color_usuario)

    label_nuevo_usuario=Label(ventana_usuario,text="Ingrese su correo electrónico",bg=color_usuario,font=font_programa)
    label_nuevo_usuario.pack(pady=(60,5))
    entry_nuevo_usuario=Entry(ventana_usuario,font=font_programa)
    entry_nuevo_usuario.pack(pady=5,ipadx=20)
    label_nueva_contraseña=Label(ventana_usuario,text="Ingrese su contraseña",bg=color_usuario,font=font_programa)
    label_nueva_contraseña.pack(pady=5)
    entry_nueva_contraseña=Entry(ventana_usuario,show="*",font=font_programa)
    entry_nueva_contraseña.pack(pady=5,ipadx=20)
    boton_guardar_usuario=Button(ventana_usuario,text="Guardar usuario",bg=color_login,font=font_programa,command=guardar_usuario)
    boton_guardar_usuario.pack(pady=15,ipadx=50)

    ventana_usuario.mainloop()

if __name__ == "__main__": 
    ventana_login()