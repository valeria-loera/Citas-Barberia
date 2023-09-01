import mysql.connector
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime

"""INICIO BASE DE DATOS"""
#acceso a base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vale0404",
    database="citas_barbería"
)

#cursores
cursor_citas = mydb.cursor() #cursor citas
cursor_clientes = mydb.cursor() #cursor clientes
cursor_empleados = mydb.cursor() #cursor empleados
cursor_servicios = mydb.cursor() #cursor servicios
#instancia librería
frameM= tk.Tk()

"""CONFIGURACIÓN TKINTER"""
#cambio de título
frameM.title("Barbería Padre Santo")

#configuración ventana
frameM.geometry('935x655') #anchoxalto
frameM.resizable(True,True)

#función cambiar de frame
def raise_frame(frame):
    frame.tkraise()



#FRAME PANTALLA INICIAL
frame_menu=ttk.Frame(frameM)
frame_menu.grid(column=0, row=0,sticky="NSEW")
raise_frame(frame_menu)

nt_menu=ttk.Notebook(frame_menu)


#IMPORTAR IMAGEN
imagen=Image.open('logo.png')
var_img= imagen.resize((180,180))
im_logo=ImageTk.PhotoImage(var_img)



"""LISTAS DE BASE DE DATOS"""
def servicios_disponibles():
    #recuperar servicios base de datos
    sqlQuery1 = "select * from servicios where disponible = 'Si'"
    cursor_servicios.execute(sqlQuery1)
    tabla_servicios = cursor_servicios.fetchall()

    array_serv=[]#lista nombre servicios
    for h in tabla_servicios:
        array_serv.append(h[1])
    return array_serv

def servicios_todos():
    #recuperar servicios base de datos
    sqlQuery2 = "select * from servicios"
    cursor_servicios.execute(sqlQuery2)
    tabla_servicios = cursor_servicios.fetchall()
    return tabla_servicios

def obtener_clientes():
    sqlQuery4 = "select * from clientes"
    cursor_clientes.execute(sqlQuery4) 
    tabla_clientes = cursor_clientes.fetchall()

    array_clien=[] #lista nombre clientes
    for i in tabla_clientes:
        array_clien.append(i[1])
    return array_clien

def solo_empleados():
    sqlQuery3 = "select * from empleados where perfil = 'Empleado'"
    cursor_empleados.execute(sqlQuery3)
    tabla_empleados = cursor_empleados.fetchall()
    return tabla_empleados
    
    
def inner_join():
    sqlQueryJ = "select * from citas C INNER JOIN clientes L ON C.ID_cliente = L.ID_cliente INNER JOIN servicios S ON C.ID_servicio = S.ID_servicio INNER JOIN empleados E ON C.ID_empleado = E.ID_empleado ORDER BY fecha"
    cursor_citas.execute(sqlQueryJ)
    registro_citas =cursor_citas.fetchall()
    return registro_citas



#################################################################################



"""FRAMES BOTONES ADICIONALES"""
"""GUARDAR NUEVA CITA"""
def guardar_cita():
    frame_rcita=ttk.Frame(frame_nuevacita)
    frame_rcita.grid(column=0, row=0, sticky="NSEW")
    
    ttk.Label(frame_rcita, text = "Nueva Cita", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)

    #botón regresar
    def regresar():
        raise_frame(frame_new)

    flecha=ttk.Button(frame_rcita, text="⬅︎",command=regresar)
    flecha.grid(column=0, row=6,pady=60, padx=50,columnspan=2, sticky='w')
    
    #insertar cita en base de datos
    def insertar_cita():
        #insertar id cliente, id servicio, horario, fecha, día, estatus = P,id empleado = Por definir
        sqlQueryI = "insert into citas (ID_cliente, ID_servicio, fecha, día, horario, ID_empleado, estatus) values (%s,%s,%s,%s,%s,%s,%s)"
        ID_cliente = str(var_idclien) 
        ID_servicio = str(var_idserv)
        fecha=str(entry_fecha.get())
        día=str(var_dia.get())
        horario=str(var_hora.get())
        ID_empleado = 12
        estatus = str('Pendiente')
        cursor_citas.execute(sqlQueryI,(ID_cliente, ID_servicio, fecha, día, horario, ID_empleado, estatus))
        mydb.commit()
        tr1.delete(*tr1.get_children())
        #recuperar citas base de datos
        tabla_citas = inner_join()
        for m in tabla_citas:
            tr1.insert('', tk.END, values=(m[0],m[9],m[12],m[5],m[4],m[19],m[6]))
        #frame éxito
        ttk.Label(frame_rcita, text="Cita Guardada", font=("Norwester", 35, 'bold')).grid(column=1, row=2,ipadx=20, ipady=20, columnspan=2,sticky='E')
        ttk.Label(frame_rcita, text = "La cita ingresada ha sido\n     guardada con éxito.", font=("Kollektif",20)).grid(column=1, row=3,ipadx=20,ipady=20, columnspan=2,sticky='NS')
        ttk.Label(frame_rcita, text = "   Consulta las todas las citas\n en la pestaña Registro de Citas", font=("Kollektif", 25)).grid(column=2, row=4,ipadx=15,ipady=20, columnspan=2,sticky='NS')
    
    
    #id cliente con nombre cliente
    sqlQueryC = "select ID_cliente from clientes where nombre_cliente = '" + str(var_clien.get()) + "'"
    cursor_clientes.execute(sqlQueryC)
    array_idclien=cursor_clientes.fetchall()
    var_idclien=str(array_idclien[0][0])
                 
    #id servicio con nombre servicio
    sqlQueryS ="select ID_servicio from servicios where nombre_servicio = '" + str(var_serv.get()) + "'"
    cursor_clientes.execute(sqlQueryS)
    array_idserv=cursor_clientes.fetchall()
    var_idserv=str(array_idserv[0][0])

    """VALIDACIONES"""
    #no exista una cita con un mismo servicio, fecha y hora
    def comprobar_empalmes():
        sqlQueryE = "select * from citas where horario = '" + (var_hora.get()) + "' and ID_servicio = " + str(var_idserv) + " and fecha = '" + str(entry_fecha.get()) + "'"
        cursor_citas.execute(sqlQueryE)
        array_empalme=cursor_citas.fetchall()
        if not array_empalme:
            #no hay coincidencias
            insertar_cita()
        else:
            #empalme
            ttk.Label(frame_rcita, text="Error", font=("Norwester", 35, 'bold')).grid(column=0, row=2,ipadx=20,ipady=20,columnspan=2,sticky= 'E')
            ttk.Label(frame_rcita, text = " Empalme por saturación de\nhorarios en citas registradas", font=("Kollektif",20)).grid(column=1,columnspan=2,row=3,ipadx=15,ipady=20,sticky='NS')
            ttk.Label(frame_rcita, text = "Intente algún otro horario.", font=("Kollektif", 25)).grid(column=2, row=4,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
            

    #el formato de la fecha
    def validar_fecha():
        while True:
            try:
                datetime.strptime(entry_fecha.get(), '%Y/%m/%d')
                #fecha válida
                comprobar_empalmes()
                break
            except ValueError:
                #fecha inválida
                ttk.Label(frame_rcita, text="Error", font=("Norwester", 35, 'bold')).grid(column=0, row=2,columnspan=2,ipadx=20,ipady=20,sticky= 'E')
                ttk.Label(frame_rcita, text = "Ingrese la fecha en \n        el formato:", font=("Kollektif",20)).grid(column=1,row=3,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
                ttk.Label(frame_rcita, text = "(AAAA/MM/DD)", font=(14)).grid(column=2,columnspan=2,row=4,ipadx=15,ipady=20, sticky='NS')
                break
            continue

    #citas en sábado y domingo antes de las 15:00
    def horario_fines():
        #if día == sábado or domingo and hora == 15,16,17,18,19
        if var_dia.get() == "Sábado" or var_dia.get() == "Domingo":
            if var_hora.get() == "15:15" or var_hora.get() == "15:30" or var_hora.get() == "15:45" or var_hora.get() == "16:00" or var_hora.get() == "16:15" or var_hora.get() == "16:30" or var_hora.get() == "16:45" or var_hora.get() == "17:00" or var_hora.get() == "17:15" or var_hora.get() == "17:30" or var_hora.get() == "17:45" or var_hora.get() == "18:00" or var_hora.get() == "18:15" or var_hora.get() == "18:30" or var_hora.get() == "18:45" or var_hora.get() == "19:00":
                #horario no válido, fin de semana
                ttk.Label(frame_rcita, text="Error", font=("Norwester", 35,'bold')).grid(column=0, row=2,columnspan=2,ipadx=20,ipady=20,sticky= 'E')
                ttk.Label(frame_rcita, text = "Padre Santo Barbería cuenta \n    con el siguiente horario:", font=("Kollektif",20)).grid(column=1,row=3,columnspan=2,ipadx=15,ipady=20, sticky= 'NS')
                ttk.Label(frame_rcita, text = "Lunes a Viernes: 9:00 a 20:00\nSábado y Domingo: 9:00 a 16:00.", font=(14)).grid(column=2, row=4,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
                ttk.Label(frame_rcita, text = "Intente algún otro horario.", font=("Kollektif", 25)).grid(column=2, row=5,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
            
            else:
                #sábado con horario válido
                validar_fecha()
        else:
            #entre semana, horario válido
            validar_fecha()

    horario_fines()
    raise_frame(frame_rcita)
    

"""FRAME NUEVO CLIENTE"""
def nuevo_cliente():
    frame_clien=ttk.Frame(frame_nuevacita)
    frame_clien.grid(column=0, row=0, sticky="NSEW")
    raise_frame(frame_clien)
        
    ttk.Label(frame_clien, text = "Nuevo Cliente", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)
        
    ttk.Label(frame_clien, text = "Nombre Completo", font=("Kollektif", 18)).grid(column=1, row=5,ipadx=20,ipady=20)
    entry_nombre=tk.StringVar()
    entry4 = ttk.Entry(frame_clien,width=15,justify=tk.CENTER, textvariable=entry_nombre)
    entry4.grid(column=2, row=5)

    ttk.Label(frame_clien, text = "Contacto", font=("Kollektif", 18)).grid(column=1, row=6, ipadx=20,ipady=20)
    entry_contacto=tk.StringVar()
    entry5 = ttk.Entry(frame_clien,width=15, justify=tk.CENTER, textvariable=entry_contacto)
    entry5.grid(column=2, row=6)

    def guardar_cliente():
        #guardar en base de datos
        sqlQueryF= "insert into clientes (nombre_cliente,contacto) VALUES (%s,%s)"
        nombre_cliente=str(entry_nombre.get())
        contacto=str(entry_contacto.get())
        cursor_clientes.execute(sqlQueryF, (nombre_cliente,contacto))
        mydb.commit()
        #cambiar combobox
        array_clien=obtener_clientes()
        cb2['values']=array_clien
        #raise frame
        raise_frame(frame_new)
        
    #botón nuevo cliente
    bt6=ttk.Button(frame_clien, text="Guardar Cliente", command=guardar_cliente).grid(column=3, row=7, columnspan=2,pady=40, padx=20)

    #botón regresar
    def regresar():
        raise_frame(frame_new)


    flecha=ttk.Button(frame_clien, text="⬅︎",command=regresar)
    flecha.grid(column=0, row=8,pady=100, padx=50,columnspan=2, sticky='w')




"""FRAME ACTUALIZAR ESTADO CITA"""
def act_estado():
    frame_estado=ttk.Frame(frame_registro)
    frame_estado.grid(column=0, row=0, sticky="NSEW")
    raise_frame(frame_estado)
        
    ttk.Label(frame_estado, text = "Actualizar Estado", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)
        
    ttk.Label(frame_estado, text = "Folio de Cita", font=("Kollektif", 18)).grid(column=1,row=5,ipadx=20,ipady=20)
    entry_folio=tk.StringVar()
    entry6 = ttk.Entry(frame_estado,width=15,justify=tk.CENTER,textvariable=entry_folio)
    entry6.grid(column=2, row=5)

    ttk.Label(frame_estado, text = "Nuevo Estado", font=("Kollektif", 18)).grid(column=1, row=6, ipadx=20,ipady=20)
    var_estado=tk.StringVar()
    cb6= ttk.Combobox(frame_estado,state="readonly", justify=tk.CENTER,width= 15,textvariable=var_estado,values =["Pendiente", "Completado", "Cancelado"])
    cb6.grid(column=2, row=6)


    def guardar_estado():
        #guardar en base de datos
        sqlQueryA = "update citas_barbería.citas SET estatus = '" + str(var_estado.get()) + "' where ID_cita = " + str(entry_folio.get()) + ""
        cursor_citas.execute(sqlQueryA)
        update_estado = cursor_citas.fetchall()
        mydb.commit()
        tr1.delete(*tr1.get_children())
        #volver a llenar
        tabla_citas=inner_join()
        for m in tabla_citas:
            tr1.insert('', tk.END, values=(m[0],m[9],m[12],m[5],m[4],m[19],m[6]))
        raise_frame(frame_citas)

        
    #botón guardar cambios
    bt7=ttk.Button(frame_estado, text="Guardar Cambios", command=guardar_estado).grid(column=3, row=7, columnspan=2,pady=40, padx=20)

    #botón regresar
    def regresar():
        raise_frame(frame_citas)

    flecha=ttk.Button(frame_estado,text="⬅︎",command=regresar)
    flecha.grid(column=0, row=8,pady=100, padx=50,columnspan=2, sticky='w')






"""FRAME EDITAR SERVICIOS"""
def gest_servicio():
    frame_gserv=ttk.Frame(frame_servicios)
    frame_gserv.grid(column=0, row=0, sticky="NSEW")
    raise_frame(frame_gserv)

    ttk.Label(frame_gserv, text = "Editar Servicios", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)

#NUEVO SERVICIO
    ttk.Label(frame_gserv, text = "Nuevo Servicio", font=("Kollektif", 18,'bold')).grid(column=1,row=5,ipadx=20,sticky='w')

    #nombre entry
    ttk.Label(frame_gserv, text="Nombre del Servicio", font=(14)).grid(column=1, row=6, ipadx=10, ipady=20)
    entry_nombreserv=tk.StringVar()
    entry7=ttk.Entry(frame_gserv, width=15,justify=tk.CENTER, textvariable=entry_nombreserv)
    entry7.grid(column=2, row=6)
        
    #precio entry
    ttk.Label(frame_gserv, text="Precio", font=(14)).grid(column=1, row=7, ipadx=10, ipady=20)
    entry_precioserv=tk.StringVar()
    entry8=ttk.Entry(frame_gserv, width=15,justify=tk.CENTER, textvariable=entry_precioserv)
    entry8.insert(0,"$") 
    entry8.grid(column=2, row=7)

    #disponibilidad combo si/no
    ttk.Label(frame_gserv, text="Disponibilidad", font=(14)).grid(column=1, row=8, ipadx=10, ipady=20)
    var_dispo=tk.StringVar()
    cb7=ttk.Combobox(frame_gserv, state="readonly", justify=tk.CENTER,width= 15, textvariable=var_dispo,values =["Si", "No"])
    cb7.grid(column=2,row=8)

    def guardar_nuevo():
        #guardar en base de datos
        sqlQueryB = "insert into servicios (nombre_servicio,precio,disponible) values (%s,%s,%s)"
        nombre_servicio = str(entry_nombreserv.get())
        precio = str(entry_precioserv.get())
        disponible= str (var_dispo.get())
        cursor_servicios.execute(sqlQueryB, (nombre_servicio,precio,disponible))
        mydb.commit()
        tr2.delete(*tr2.get_children())
        #llenar treeview
        tabla_servicios=servicios_todos()
        for n in tabla_servicios:
            tr2.insert('', tk.END, values=(n[0],n[1],n[2],n[3]))
        #llenar combobox
        array_serv=servicios_disponibles()
        cb3['values']=array_serv
        raise_frame(frame_serv)
            
    #botón nuevo servicio
    bt8=ttk.Button(frame_gserv, text="Guardar Nuevo Servicio", command=guardar_nuevo).grid(column=3, row=8, columnspan=2,pady=20, padx=20)



#MODIFICAR DISPONIBILIDAD
    ttk.Label(frame_gserv, text = "Modificar Disponibilidad", font=("Kollektif", 18,'bold')).grid(column=1, row=10, ipadx=20,ipady=20,sticky='w')
    #nombre servicio combo basedatos
    ttk.Label(frame_gserv, text="Nombre del Servicio", font=(14)).grid(column=1, row=11, ipadx=10, ipady=20)
    var_nomserv=tk.StringVar()
    cb8=ttk.Combobox(frame_gserv, state="readonly", justify=tk.CENTER,width= 25, textvariable=var_nomserv)#database

    #recuperar servicios base de datos
    tabla_servicios=servicios_todos()
    array_serv=[]#lista nombre servicios
    for h in tabla_servicios:
        array_serv.append(h[1])

    cb8['values']=array_serv
    cb8.grid(column=2,row=11)
        
    #nueva disponibilidad combo si/no
    ttk.Label(frame_gserv, text="Nueva Disponibilidad", font=(14)).grid(column=1, row=12, ipadx=10, ipady=20)
    var_ndispo=tk.StringVar()
    cb9=ttk.Combobox(frame_gserv, state="readonly", justify=tk.CENTER,width= 15, textvariable=var_ndispo,values =["Si", "No"])
    cb9.grid(column=2,row=12)

    def guardar_modificar():
        #guardar en base de datos
        sqlQueryC= "update citas_barbería.servicios SET disponible = '" + str(var_ndispo.get()) + "' where nombre_servicio = '" + str(var_nomserv.get()) + "'"
        cursor_servicios.execute(sqlQueryC)
        update_dispo = cursor_citas.fetchall()
        mydb.commit()
        tr2.delete(*tr2.get_children())
        #llenar de nuevo el treeview
        tabla_servicios=servicios_todos()
        for n in tabla_servicios:
            tr2.insert('', tk.END, values=(n[0],n[1],n[2],n[3]))
        #modificar combobox
        array_serv=servicios_disponibles()
        cb3['values']=array_serv
        #raise
        raise_frame(frame_serv)

    #botón modificar disponible
    bt9=ttk.Button(frame_gserv, text="Guardar Cambios", command=guardar_modificar).grid(column=3, row=12, columnspan=2,pady=20, padx=20)

#botón regresar
    def regresar():
        raise_frame(frame_serv)

    flecha=ttk.Button(frame_gserv,text="⬅︎",command=regresar)
    flecha.grid(column=0, row=13,pady=10, padx=50,columnspan=2, sticky='w')
        







"""FRAME GESTIONAR EMPLEADOS"""
def edit_employ():
    frame_gemploy=ttk.Frame(frame_empleados)
    frame_gemploy.grid(column=0, row=0, sticky="NSEW")
    raise_frame(frame_gemploy)
    ttk.Label(frame_gemploy, text = "Editar Empleados", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)

#ASIGNAR CITA
    #DISEÑO ASIGNAR EMPLEADO
    ttk.Label(frame_gemploy, text = "Asignar Cita", font=("Kollektif", 18,'bold')).grid(column=1, row=5, ipadx=20,sticky='w')
    #empleado combo basedatos
    ttk.Label(frame_gemploy, text="Nombre del Empleado", font=(14)).grid(column=1, row=6, ipadx=10, ipady=20)
    var_nemploy=tk.StringVar()
    cb11=ttk.Combobox(frame_gemploy, state="readonly", textvariable=var_nemploy,justify=tk.CENTER,width= 15)#database
    
    tabla_empleados=solo_empleados()
    array_employ=[]#lista nombre empleados
    for j in tabla_empleados:
        array_employ.append(j[4])
    cb11['values']=array_employ
    cb11.grid(column=2,row=6)
        
    #folio entry
    ttk.Label(frame_gemploy, text="Folio de Cita", font=(14)).grid(column=1, row=7, ipadx=10, ipady=20)
    entry_folioemploy=tk.StringVar()
    entry11=ttk.Entry(frame_gemploy, width=15,justify=tk.CENTER, textvariable=entry_folioemploy)
    entry11.grid(column=2,row=7)

    
    def guardar_asig():
        #recuperar id de empleado
        sqlQueryID = (f"select ID_empleado from empleados where nombre_empleado= '{var_nemploy.get()}'")
        cursor_empleados.execute(sqlQueryID)
        id_empleado=cursor_empleados.fetchall()
        var_idemploy=str(id_empleado[0][0])

        #recuperar fecha de la cita
        sqlQueryF = (f"select fecha from citas where ID_cita= '{entry_folioemploy.get()}'")
        cursor_citas.execute(sqlQueryF)
        f_cita=cursor_citas.fetchall()
        var_fcita=str(f_cita[0][0])

        #recuperar horario de la cita
        sqlQueryH = (f"select horario from citas where ID_cita= '{entry_folioemploy.get()}'")
        cursor_citas.execute(sqlQueryH)
        h_cita=cursor_citas.fetchall()
        var_hcita=str(h_cita[0][0])

        #recuperar día de la cita
        sqlQueryD = (f"select día from citas where ID_cita= '{entry_folioemploy.get()}'")
        cursor_citas.execute(sqlQueryD)
        d_cita=cursor_citas.fetchall()
        var_dcita=str(d_cita[0][0])

        #recuperar descanso de empleado
        sqlQueryS = (f"select día_descanso from empleados where ID_empleado= '{var_idemploy}'")
        cursor_citas.execute(sqlQueryS)
        d_employ=cursor_citas.fetchall()
        var_demploy=str(d_employ[0][0])


        frame_eemploy=ttk.Frame(frame_empleados)

        def frame_errores():
            frame_eemploy.grid(column=0, row=0, sticky="NSEW")
            ttk.Label(frame_eemploy, text = "Editar Empleados", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)
            #botón regresar
            def regresar():
                raise_frame(frame_gemploy)
        
            flecha=ttk.Button(frame_eemploy, text="⬅︎",command=regresar)
            flecha.grid(column=0, row=6,pady=60, padx=50,columnspan=2, sticky='w')


        #update idempleado con folio de cita
        def asignar_empleado():
            sqlQueryU = (f"update citas_barbería.citas SET ID_empleado = '{var_idemploy}' where ID_cita = '{entry_folioemploy.get()}'")
            cursor_empleados.execute(sqlQueryU)
            mydb.commit()
            tr1.delete(*tr1.get_children())
            #volver a llenar el treeview"
            registro_citas = inner_join()
            for m in registro_citas:
                tr1.insert('',tk.END, values=(m[0],m[9],m[12],m[5],m[4],m[19],m[6]))
            #raise frame
            raise_frame(frame_employ)

        
        #no exista una cita con un mismo empleado, fecha y hora
        def comprobar_empalmes():
            sqlQueryE = "select * from citas where horario = '" + str(var_hcita) + "' and ID_empleado = " + str(var_idemploy) + " and fecha = '" + str(var_fcita) + "'"
            cursor_citas.execute(sqlQueryE)
            array_empalme=cursor_citas.fetchall()
            if not array_empalme:
                #no hay coincidencias
                asignar_empleado()
            else:
                #empalme
                frame_errores()
                ttk.Label(frame_eemploy, text="Error", font=("Norwester", 35, 'bold')).grid(column=0, row=2,ipadx=20,ipady=20,columnspan=2,sticky= 'E')
                ttk.Label(frame_eemploy, text = "El empleado ya tiene una cita en esa\n      fecha en ese horario.", font=("Kollektif",20)).grid(column=1,columnspan=2,row=3,ipadx=15,ipady=20,sticky='NS')
                ttk.Label(frame_eemploy, text = "Intente algún otro empleado.", font=("Kollektif", 25)).grid(column=2, row=4,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
                raise_frame(frame_eemploy)
    

        def dia_descanso():
            if var_dcita == var_demploy:
                frame_errores()
                ttk.Label(frame_eemploy, text="Error", font=("Norwester", 35, 'bold')).grid(column=0, row=2,ipadx=20,ipady=20,columnspan=2,sticky= 'E')
                ttk.Label(frame_eemploy, text = "El empleado no trabaja ese día", font=("Kollektif",20)).grid(column=1,columnspan=2,row=3,ipadx=15,ipady=20,sticky='NS')
                ttk.Label(frame_eemploy, text = "Intente algún otro empleado.", font=("Kollektif", 25)).grid(column=2, row=4,columnspan=2,ipadx=15,ipady=20,sticky= 'NS')
                raise_frame(frame_eemploy)
                print("no labora")
            else:
                print("si labora el employ")
                comprobar_empalmes()
    
        dia_descanso()
        

    #botón modificar asignación
    bt11=ttk.Button(frame_gemploy, text="Guardar Asignación", command=guardar_asig).grid(column=3, row=8, columnspan=2,pady=20, padx=20)













#NUEVO EMPLEADO
    ttk.Label(frame_gemploy, text = "Nuevo Empleado", font=("Kollektif", 18,'bold')).grid(column=1,row=10,ipadx=20,ipady=20,sticky='w')

    #nombre entry
    ttk.Label(frame_gemploy, text="Nombre", font=(14)).grid(column=1, row=11, ipadx=10, ipady=20)
    entry_nombreemploy=tk.StringVar()
    entry10=ttk.Entry(frame_gemploy, width=15,justify=tk.CENTER, textvariable=entry_nombreemploy)
    entry10.grid(column=2, row=11)

    #descanso combo
    ttk.Label(frame_gemploy, text="Día de Descanso", font=(14)).grid(column=1, row=12, ipadx=10, ipady=20)
    var_descanso = tk.StringVar()
    cb10=ttk.Combobox(frame_gemploy, state="readonly", justify=tk.CENTER,width= 15, textvariable=var_descanso,values =["Lunes", "Martes", "Miércoles", "Jueves", "Domingo"])
    cb10.grid(column=2, row=12)

    def guardar_nuevo():
        #guardar en base de datos
        sqlQueryE = "insert into empleados (nombre_empleado,día_descanso) values (%s,%s)"
        nombre_empleado = str(entry_nombreemploy.get())
        día_descanso = str(var_descanso.get())
        cursor_empleados.execute(sqlQueryE, (nombre_empleado,día_descanso))
        mydb.commit()
        tr3.delete(*tr3.get_children())
        #recuperar empleados base de datos
        tabla_empleados = solo_empleados()
        for d in tabla_empleados:
            tr3.insert('', tk.END, values=(d[0],d[4],d[5]))
        raise_frame(frame_employ)
            
    #botón nuevo servicio
    bt10=ttk.Button(frame_gemploy, text="Guardar Nuevo Empleado", command=guardar_nuevo).grid(column=3, row=12, columnspan=2,pady=20, padx=20)

    #botón regresar
    def regresar():
        raise_frame(frame_employ)

    flecha=ttk.Button(frame_gemploy,text="⬅︎",command=regresar)
    flecha.grid(column=0, row=13,pady=10, padx=50,columnspan=2, sticky='w')
            
    ######################################################







"""FRAMES PESTAÑAS NOTEBOOK"""

"""FRAME NUEVA CITA"""
frame_nuevacita=ttk.Frame(nt_menu)
frame_new=ttk.Frame(frame_nuevacita)
frame_new.grid(column=0,row=0,sticky="NSEW")
ttk.Label(frame_new, text = "Nueva Cita", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40)

#combobox clientes
ttk.Label(frame_new, text="Cliente", font=("Kollektif", 18)).grid(column=1, row=1,ipadx=20)
var_clien=tk.StringVar()
cb2= ttk.Combobox(frame_new,state="readonly", textvariable=var_clien,justify=tk.CENTER,width= 15)
array_clien=obtener_clientes()
cb2['values']=array_clien
cb2.grid(column=2, row=1)

#botón nuevo cliente
bt2=ttk.Button(frame_new, text="Nuevo Cliente",command=nuevo_cliente).grid(column=3, row=2,pady=20, padx=20)

#combobox servicios
ttk.Label(frame_new, text="Servicio", font=("Kollektif", 18)).grid(column=1, row=3, ipadx=20,pady=20)
var_serv=tk.StringVar()
cb3= ttk.Combobox(frame_new,state="readonly", textvariable=var_serv,justify=tk.CENTER,width= 25)
array_serv=servicios_disponibles()
cb3['values']=array_serv
cb3.grid(column=2, row=3)


#selección horario
ttk.Label(frame_new, text="Horario", font=("Kollektif", 18)).grid(column=2, row=5, ipady=20)
ttk.Label(frame_new, text="Hora", font=(14)).grid(column=1, row=6, ipadx=20, ipady=20)
var_hora=tk.StringVar()
cb4= ttk.Combobox(frame_new,state="readonly", textvariable=var_hora,justify=tk.CENTER,width= 10, values =["9:00","9:15","9:30","9:45",
                                                                                                          "10:00","10:15","10:30","10:45",
                                                                                                          "11:00","11:15","11:30","11:45",
                                                                                                          "12:00","12:15","12:30","12:45",
                                                                                                          "13:00","13:15","13:30","13:45",
                                                                                                          "14:00","14:15","14:30","14:45",
                                                                                                          "15:00","15:15","15:30","15:45",
                                                                                                          "16:00","16:15","16:30","16:45",
                                                                                                          "17:00","17:15","17:30","17:45",
                                                                                                          "18:00","18:15","18:30","18:45",
                                                                                                          "19:00"])
cb4.grid(column=2, row=6)
ttk.Label(frame_new, text="Día", font=(14)).grid(column=1, row=7, ipadx=20, ipady=20)
var_dia=tk.StringVar()
cb5= ttk.Combobox(frame_new,state="readonly", textvariable=var_dia, justify=tk.CENTER,width= 15, values =["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
cb5.grid(column=2, row=7)


ttk.Label(frame_new, text="Fecha", font=(14)).grid(column=1, row=8, ipadx=20, ipady=20)
entry_fecha=tk.StringVar()
entry3=ttk.Entry(frame_new, width=15,textvariable=entry_fecha)
entry3.insert(0,"AAAA/MM/DD") 
entry3.grid(column=2,row=8)

bt3=ttk.Button(frame_new, text="Guardar Cita", command=guardar_cita).grid(column=3, row=9,pady=20, padx=20)


"""FRAME REGISTRO DE CITAS"""
frame_registro=ttk.Frame(nt_menu)
frame_citas=ttk.Frame(frame_registro)
frame_citas.grid(column=0,row=0,sticky="NSEW")
ttk.Label(frame_citas, text = "Registro de Citas", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40, stick='nw')

#treeview citas
ct1= ('id','cliente', 'servicio', 'fecha','horario','empleado','estado')
tr1 = ttk.Treeview(frame_citas, columns=ct1, show='headings')
tr1.heading('id',text='Folio')
tr1.heading('cliente', text='Cliente')
tr1.heading('servicio', text='Servicio')
tr1.heading('fecha', text='Fecha')
tr1.heading('horario', text='Horario')
tr1.heading('empleado', text='Empleado')
tr1.heading('estado', text='Estado')
tr1.grid(row=1, column=0, padx=30, ipady=40)

tr1.column('id', width=43, anchor=tk.CENTER)
tr1.column('cliente', width=120,anchor=tk.CENTER)
tr1.column('servicio', width=250,anchor=tk.CENTER)
tr1.column('fecha', width=100,anchor=tk.CENTER)
tr1.column('horario', width=100,anchor=tk.CENTER)
tr1.column('empleado', width=100,anchor=tk.CENTER)
tr1.column('estado', width=100,anchor=tk.CENTER)

#scrollbar treeview citas
sc1 = ttk.Scrollbar(frame_citas, orient=tk.VERTICAL, command=tr1.yview)
tr1.configure(yscroll=sc1.set)
sc1.grid(row=1, column=1, sticky=tk.NS)


#recuperar citas base de datos
registro_citas = inner_join()
for m in registro_citas:
    tr1.insert('',tk.END, values=(m[0],m[9],m[12],m[5],m[4],m[19],m[6]))

bt5=ttk.Button(frame_citas, text="Actualizar Estado", command=act_estado).grid(column=0, row=3,pady=55, padx=20, columnspan=2, stick='e')



"""FRAME LISTADO SERVICIOS"""
frame_servicios=ttk.Frame(nt_menu)
frame_serv=ttk.Frame(frame_servicios)
frame_serv.grid(column=0,row=0,sticky="NSEW")
ttk.Label(frame_serv, text = "Listado de Servicios", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40,stick='nw')

#treeview servicios
ct2 = ('número', 'nombre', 'precio', 'disponible')
tr2 = ttk.Treeview(frame_serv, columns=ct2, show='headings')
tr2.heading('número', text='Número')
tr2.heading('nombre', text='Nombre del Servicio')
tr2.heading('precio', text='Precio ($)')
tr2.heading('disponible', text='Disponibilidad')
tr2.grid(row=1, column=0, padx=30, ipady=40, sticky='e')

tr2.column('número', width=80,anchor=tk.CENTER)
tr2.column('nombre', width=280,anchor=tk.CENTER)
tr2.column('precio', width=100,anchor=tk.CENTER)
tr2.column('disponible', width=80,anchor=tk.CENTER)

#scrollbar treeview servicios
sc2 = ttk.Scrollbar(frame_serv, orient=tk.VERTICAL, command=tr2.yview)
tr2.configure(yscroll=sc2.set)
sc2.grid(row=1, column=1,sticky='ns')

#recuperar servicios base de datos
tabla_servicios = servicios_todos()
for n in tabla_servicios:
    tr2.insert('', tk.END, values=(n[0],n[1],n[2],n[3]))

bt3=ttk.Button(frame_serv, text="Editar Servicios", command=gest_servicio).grid(column=0, row=3,pady=40, padx=20, columnspan=2, stick='e')



"""FRAME LISTADO DE EMPLEADOS"""
frame_empleados=ttk.Frame(nt_menu)
frame_employ=ttk.Frame(frame_empleados)
frame_employ.grid(column=0,row=0,sticky="NSEW")
ttk.Label(frame_employ, text = "Listado de Empleados", font=("Norwester", 30, "bold")).grid(column=0, row=0, columnspan=2, padx=50, ipady=40,stick='nw')

#treeview empleados
ct3 = ('id', 'nombre', 'descanso')
tr3 = ttk.Treeview(frame_employ, columns=ct3, show='headings')
tr3.heading('id', text='Número de Empleado')
tr3.heading('nombre', text='Nombre Completo')
tr3.heading('descanso', text='Día de Descanso')
tr3.grid(row=1, column=0, padx=30, ipady=40, sticky='e')

tr3.column('id', width=150,anchor=tk.CENTER)
tr3.column('nombre', anchor=tk.CENTER)
tr3.column('descanso', width=150,anchor=tk.CENTER)

#scrollbar treeview servicios
sc3 = ttk.Scrollbar(frame_employ, orient=tk.VERTICAL, command=tr3.yview)
tr3.configure(yscroll=sc3.set)
sc3.grid(row=1, column=1,sticky='ns')

#recuperar EMPLEADOS base de datos
tabla_empleados=solo_empleados()
for d in tabla_empleados:
    tr3.insert('', tk.END, values=(d[0],d[4],d[5]))

bt4=ttk.Button(frame_employ, text="Asignar Empleados", command=edit_employ).grid(column=0, row=3,pady=55, padx=20, columnspan=2, stick='e')



"""INTEGRACIÓN FRAMES A NOTEBOOK"""
nt_menu.add(frame_nuevacita, text="Nueva Cita")
nt_menu.add(frame_registro, text="Registro de Citas")
nt_menu.add(frame_servicios, text="Listado de Servicios")
nt_menu.add(frame_empleados, text="Listado de Empleados")
nt_menu.grid(column=0, row=0, sticky="NSEW")




"""INICIO DE SESIÓN"""
#interfaz
frame_i=ttk.Frame(frameM)
frame_i.grid(column=0, row=0, sticky="NSEW")
raise_frame(frame_i)
tk.Label(frame_i, text = "Sistema de Citas", font=("Norwester", 30,'bold')).grid(column=0, row=0,columnspan=2, ipadx=40, ipady=60, sticky='E')
tk.Label(frame_i, text="Inicio de Sesión", font=("Kollektif", 18)).grid(column=1, row=1, rowspan=2, ipadx=20)

"""tk.Label(frame_i, text = "Perfil",font = (14)).grid(column=1, row=5, ipadx=20, ipady=20)
cb1= ttk.Combobox(frame_i,state="readonly", width= 15, values =["Administrador", "Empleado"])
cb1.grid(column=2, row=5)"""

tk.Label(frame_i, text = "Usuario", font = (14)).grid(column=1, row=5, ipadx=20,ipady=20)
entry_usuario=tk.StringVar()
entry1 = ttk.Entry(frame_i,width=15,justify=tk.CENTER, textvariable=entry_usuario)
entry1.grid(column=2, row=5)

tk.Label(frame_i, text = "Contraseña", font = (14)).grid(column=1, row=6, ipadx=20,ipady=20)
entry_contra=tk.StringVar()
entry2 = ttk.Entry(frame_i,width=15, justify=tk.CENTER, textvariable=entry_contra,show="*")
entry2.grid(column=2, row=6)

#logo
logo=ttk.Label(frame_i,image=im_logo)
logo.grid(column=4, row=1,rowspan=6,columnspan=1, sticky='W')
logo.image=im_logo



#BOTÓN INICIO SESIÓN
def boton_inicio():
    acceso = False
    print ("\n❊ INICIO DE SESIÓN")
    usuario = entry_usuario.get() #entry de tkinter
    contraseña = entry_contra.get()

    sqlQuery1 = "select * from empleados where usuario_empleado = %s and contraseña_empleado = %s"
    cursor_empleados.execute(sqlQuery1, [usuario,contraseña])
    inicio_sesión = cursor_empleados.fetchall()
       
    if len (inicio_sesión):
        acceso = True
        raise_frame(frame_menu)   
        for a in inicio_sesión:
            print ("\n\n\t ⋙ Bienvenidx", a[3], a[4], "⋘")
            id_empleado = (a[0])
    else:
        #texto en tkinter
        print("\tACCESO DENEGADO")

bt1=ttk.Button(frame_i, text="Iniciar Sesión", command=boton_inicio).grid(column=3, row=8,ipady=50)



#LOOP TKINTER
frameM.mainloop()
