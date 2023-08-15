import redis

# Connect to the Redis server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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
        palabras = redis_client.keys('*')
        for palabra_id in palabras:
            palabra = redis_client.hgetall(palabra_id)
            print(f"{palabra_id.decode()}. {palabra[b'PALABRA'].decode()} ({palabra[b'DEFINICION'].decode()})")
    
    if opcion == 2:
        print("Vamos a agregar una nueva Palabra Y Definicion...")
        palabra = input("Palabra: ")
        definicion = input("Definicion: ")
        palabra_id = redis_client.incr('next_id')
        nueva_palabra = {
            b'PALABRA': palabra.encode(),
            b'DEFINICION': definicion.encode()
        }
        try:
            redis_client.hmset(palabra_id, nueva_palabra)
            print("Palabra Y Definicion agregada con éxito")
        except:
            print("ERR::Palabra Y Definicion ya existente, intentar otro")
                
    if opcion == 3:
        print("Vamos a eliminar una Palabra y Su Definicion...") 
        palabras = redis_client.keys('*')
        for palabra_id in palabras:
            palabra = redis_client.hgetall(palabra_id)
            print(f"{palabra_id.decode()}. {palabra[b'PALABRA'].decode()} ({palabra[b'DEFINICION'].decode()})")
        palabra_id = int(input("ID de la Palabra Y Definicion: "))
        if not redis_client.exists(palabra_id):
            print("ERR::Palabra Y Definicion no existe")
            continue
        else:
            redis_client.delete(palabra_id)
            print("Palabra Y Definicion eliminada con éxito")
    
    if opcion == 4:
        print("Vamos a modificar una Palabra y su Definicion...")
        palabras = redis_client.keys('*')
        for palabra_id in palabras:
            palabra = redis_client.hgetall(palabra_id)
            print(f"{palabra_id.decode()}. {palabra[b'PALABRA'].decode()}")
        palabra_id = int(input("ID de la Palabra a modificar: "))
        if not redis_client.exists(palabra_id):
            print("ERR::Palabra no existe")
            continue
        else:
            nueva_palabra = input("Palabra nueva: ")
            nueva_definicion = input("Definicion nueva: ")
            updated_palabra = {
                b'PALABRA': nueva_palabra.encode(),
                b'DEFINICION': nueva_definicion.encode()
            }
            redis_client.hmset(palabra_id, updated_palabra)
            print("Palabra y Definicion modificada con éxito")
    
    if opcion == 5:
        print("Gracias por preferirnos")
        break
