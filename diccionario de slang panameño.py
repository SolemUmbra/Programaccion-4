import sqlite3

conn = sqlite3.connect('prueba.db')
print("Base de datos abierta con exito!")

conn.execute('''CREATE TABLE IF NOT EXISTS PALABRASYDEFINICIONES
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             PALABRA TEXT NOT NULL,
             DEFINICION TEXT NOT NULL);''')
print("Tabla creada con exito!")

while True:
    print("\n\nMENU - SISTEMA ALQUILER")
    print("1. Ver Listado De Palabras") #Ver Listado De Palabras
    print("2. Agregar Nueva Palabra") #Agregar Nueva Palabra
    print("3. Eliminar Palabra Existente") #Eliminar Palabra Existente
    print("4. Editar Palabra Existente") #Editar Palabra Existente
    print("5. Salir") #Salir
    try:
        opcion = int(input("Opcion: "))
    except:
        print("ERR::Opcion invalida")
        opcion = 999
    
    if opcion == 1:
        print("Vamos a ver las Palabras Y Definiciones...")
        juegos = conn.execute("SELECT * FROM PALABRASYDEFINICIONES")
        for juego in juegos:
            print(str(juego[0])+". "+str(juego[1])+" ("+str(juego[2])+")" )
    
    if opcion == 2:
            print("Vamos a agregar un nueva Palabra Y Definicion...")
            palabra = input("Palabra: ")
            definicion = input("Definicion: ")
            try:
                conn.execute("INSERT INTO PALABRASYDEFINICIONES(PALABRA, DEFINICION) VALUES(?, ?)", (palabra, definicion))
                conn.commit()
            except:
                print("ERR::Palabra Y Definicion ya existente, intentar otro")
                
    if opcion == 3:
        print("Vamos a eliminar una Palabra y Su Definicion...") 
        juegos = conn.execute("SELECT * FROM PALABRASYDEFINICIONES")
        for juego in juegos:
            print(str(juego[0])+". "+str(juego[1])+" ("+str(juego[2])+")" )
        juegoelegido = int(input("ID la Palabra Y Definicion: "))
        stat_je = conn.execute("SELECT * FROM PALABRASYDEFINICIONES WHERE ID = " + str(juegoelegido))
        num_s_je = len(stat_je.fetchall())
        if num_s_je == 0:
            print("ERR::Palabra Y Definicion no existe")
            continue
        else:
            conn.execute("DELETE FROM PALABRASYDEFINICIONES WHERE ID = " + str(juegoelegido))
            conn.commit()
            print("Palabra Y Definicion eliminado con éxito")
    
    if opcion == 4:
        print("Vamos a modificar a una Palabra y su Definicion...")
        usuarios = conn.execute("SELECT * FROM PALABRASYDEFINICIONES")
        for usuario in usuarios:
            print(str(usuario[0])+" - "+str(usuario[1]))
        usuarioelegido = input("Palabra y Definicion a modificar: ")
        nombre = input("Palabra nueva: ")
        correo = input("Definicion nueva: ")
        try:
            conn.execute("UPDATE PALABRASYDEFINICIONES SET PALABRA=?, DEFINICION=? WHERE PALABRA=?", (nombre, correo, usuarioelegido))
            conn.commit()
        except:
            print("ERR::Error con la Palabra Y Definicion, intentar nuevamente")

    if opcion == 5:
        print("Gracias por preferirnos")
        exit()

conn.close()