from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PalabraDefinicion(Base):
    __tablename__ = 'PALABRASYDEFINICIONES'
    ID = Column(Integer, primary_key=True)
    PALABRA = Column(String, nullable=False)
    DEFINICION = Column(String, nullable=False)

engine = create_engine('sqlite:///prueba.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
        palabras = session.query(PalabraDefinicion).all()
        for palabra in palabras:
            print(f"{palabra.ID}. {palabra.PALABRA} ({palabra.DEFINICION})")
    
    if opcion == 2:
        print("Vamos a agregar una nueva Palabra Y Definicion...")
        palabra = input("Palabra: ")
        definicion = input("Definicion: ")
        try:
            nueva_palabra = PalabraDefinicion(PALABRA=palabra, DEFINICION=definicion)
            session.add(nueva_palabra)
            session.commit()
        except:
            print("ERR::Palabra Y Definicion ya existente, intentar otro")
                
    if opcion == 3:
        print("Vamos a eliminar una Palabra y Su Definicion...") 
        palabras = session.query(PalabraDefinicion).all()
        for palabra in palabras:
            print(f"{palabra.ID}. {palabra.PALABRA} ({palabra.DEFINICION})")
        palabra_id = int(input("ID de la Palabra Y Definicion: "))
        palabra_obj = session.query(PalabraDefinicion).filter_by(ID=palabra_id).first()
        if palabra_obj is None:
            print("ERR::Palabra Y Definicion no existe")
            continue
        else:
            session.delete(palabra_obj)
            session.commit()
            print("Palabra Y Definicion eliminada con éxito")
    
    if opcion == 4:
        print("Vamos a modificar una Palabra y su Definicion...")
        palabras = session.query(PalabraDefinicion).all()
        for palabra in palabras:
            print(f"{palabra.ID}. {palabra.PALABRA}")
        palabra_id = int(input("ID de la Palabra a modificar: "))
        palabra_obj = session.query(PalabraDefinicion).filter_by(ID=palabra_id).first()
        if palabra_obj is None:
            print("ERR::Palabra no existe")
            continue
        else:
            nueva_palabra = input("Palabra nueva: ")
            nueva_definicion = input("Definicion nueva: ")
            palabra_obj.PALABRA = nueva_palabra
            palabra_obj.DEFINICION = nueva_definicion
            session.commit()
    
    if opcion == 5:
        print("Gracias por preferirnos")
        break

session.close()
