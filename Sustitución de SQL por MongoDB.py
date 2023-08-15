from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['palabras_db']
collection = db['palabras']

while True:
    print("\n\nMENU - SISTEMA ALQUILER")
    print("1. Ver Listado De Palabras")
    print("2. Agregar Nueva Palabra")
    print("3. Eliminar Palabra Existente")
    print("4. Editar Palabra Existente")
    print("5. Salir")
    
    try:
        opcion = int(input("Opcion: "))
    except ValueError:
        print("ERR::Opcion invalida")
        opcion = 999
    
    if opcion == 1:
        print("Vamos a ver las Palabras Y Definiciones...")
        palabras = collection.find()
        for palabra in palabras:
            print(f"{palabra['_id']}. {palabra['PALABRA']} ({palabra['DEFINICION']})")
    
    if opcion == 2:
        print("Vamos a agregar una nueva Palabra Y Definicion...")
        palabra = input("Palabra: ")
        definicion = input("Definicion: ")
        nueva_palabra = {
            'PALABRA': palabra,
            'DEFINICION': definicion
        }
        try:
            collection.insert_one(nueva_palabra)
            print("Palabra Y Definicion agregada con éxito")
        except:
            print("ERR::Palabra Y Definicion ya existente, intentar otro")
                
    if opcion == 3:
        print("Vamos a eliminar una Palabra y Su Definicion...") 
        palabras = collection.find()
        for palabra in palabras:
            print(f"{palabra['_id']}. {palabra['PALABRA']} ({palabra['DEFINICION']})")
        palabra_id = int(input("ID de la Palabra Y Definicion: "))
        palabra_obj = collection.find_one({'_id': palabra_id})
        if palabra_obj is None:
            print("ERR::Palabra Y Definicion no existe")
            continue
        else:
            collection.delete_one({'_id': palabra_id})
            print("Palabra Y Definicion eliminada con éxito")
    
    if opcion == 4:
        print("Vamos a modificar una Palabra y su Definicion...")
        palabras = collection.find()
        for palabra in palabras:
            print(f"{palabra['_id']}. {palabra['PALABRA']}")
        palabra_id = int(input("ID de la Palabra a modificar: "))
        palabra_obj = collection.find_one({'_id': palabra_id})
        if palabra_obj is None:
            print("ERR::Palabra no existe")
            continue
        else:
            nueva_palabra = input("Palabra nueva: ")
            nueva_definicion = input("Definicion nueva: ")
            collection.update_one(
                {'_id': palabra_id},
                {'$set': {'PALABRA': nueva_palabra, 'DEFINICION': nueva_definicion}}
            )
            print("Palabra y Definicion modificada con éxito")
    
    if opcion == 5:
        print("Gracias por preferirnos")
        break

client.close()
