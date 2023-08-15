import sqlite3
import redis

class InventoryApp:
    def __init__(self):
        self.db_connection = sqlite3.connect('inventory.db')
        self.db_cursor = self.db_connection.cursor()

        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        ''')
        self.db_connection.commit()

    def register_item(self, name, quantity, price):
        self.db_cursor.execute('''
            INSERT INTO items (name, quantity, price)
            VALUES (?, ?, ?)
        ''', (name, quantity, price))
        self.db_connection.commit()

        item_id = self.db_cursor.lastrowid
        self.redis_client.hmset(item_id, {'name': name, 'quantity': quantity, 'price': price})
        print("Artículo registrado con éxito.")

    def search_item(self, item_id):
        item = self.redis_client.hgetall(item_id)
        if item:
            print(f"ID: {item_id}, Nombre: {item[b'name'].decode()}, Cantidad: {item[b'quantity'].decode()}, Precio: {item[b'price'].decode()}")
        else:
            print("Artículo no encontrado.")

    def edit_item(self, item_id, new_name, new_quantity, new_price):
        self.db_cursor.execute('''
            UPDATE items
            SET name=?, quantity=?, price=?
            WHERE id=?
        ''', (new_name, new_quantity, new_price, item_id))
        self.db_connection.commit()

        self.redis_client.hmset(item_id, {'name': new_name, 'quantity': new_quantity, 'price': new_price})
        print("Artículo editado con éxito.")

    def delete_item(self, item_id):
        self.db_cursor.execute('''
            DELETE FROM items
            WHERE id=?
        ''', (item_id,))
        self.db_connection.commit()

        self.redis_client.delete(item_id)
        print("Artículo eliminado con éxito.")

    def show_inventory(self):
        self.db_cursor.execute('SELECT * FROM items')
        items = self.db_cursor.fetchall()

        for item in items:
            print(f"ID: {item[0]}, Nombre: {item[1]}, Cantidad: {item[2]}, Precio: {item[3]}")

    def close_connections(self):
        self.db_connection.close()

def main():
    app = InventoryApp()

    while True:
        print("\nMENU - SISTEMA DE INVENTARIO")
        print("1. Registrar artículo")
        print("2. Buscar artículo")
        print("3. Editar artículo")
        print("4. Eliminar artículo")
        print("5. Mostrar inventario")
        print("6. Salir")

        try:
            option = int(input("Opción: "))
        except ValueError:
            print("Opción inválida")
            continue

        if option == 1:
            name = input("Nombre del artículo: ")
            quantity = int(input("Cantidad del artículo: "))
            price = float(input("Precio del artículo: "))
            app.register_item(name, quantity, price)

        elif option == 2:
            item_id = input("ID del artículo a buscar: ")
            app.search_item(item_id)

        elif option == 3:
            item_id = int(input("ID del artículo a editar: "))
            new_name = input("Nuevo nombre del artículo: ")
            new_quantity = int(input("Nueva cantidad del artículo: "))
            new_price = float(input("Nuevo precio del artículo: "))
            app.edit_item(item_id, new_name, new_quantity, new_price)

        elif option == 4:
            item_id = int(input("ID del artículo a eliminar: "))
            app.delete_item(item_id)

        elif option == 5:
            app.show_inventory()

        elif option == 6:
            app.close_connections()
            print("Gracias por usar el sistema de inventario.")
            break

        else:
            print("Opción inválida, por favor selecciona una opción válida.")

if __name__ == "__main__":
    main()
