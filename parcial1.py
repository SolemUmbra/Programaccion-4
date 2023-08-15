class InventoryApp:
    def __init__(self):
        self.inventory = {}

    def register_item(self, item_id, name, quantity, price):
        if item_id in self.inventory:
            print("Error: El artículo ya está registrado.")
        else:
            self.inventory[item_id] = {'name': name, 'quantity': quantity, 'price': price}
            print("Artículo registrado con éxito.")

    def search_item(self, item_id):
        if item_id in self.inventory:
            item = self.inventory[item_id]
            print(f"ID: {item_id}, Nombre: {item['name']}, Cantidad: {item['quantity']}, Precio: {item['price']}")
        else:
            print("Artículo no encontrado.")

    def edit_item(self, item_id, new_name, new_quantity, new_price):
        if item_id in self.inventory:
            self.inventory[item_id]['name'] = new_name
            self.inventory[item_id]['quantity'] = new_quantity
            self.inventory[item_id]['price'] = new_price
            print("Artículo editado con éxito.")
        else:
            print("Artículo no encontrado.")

    def delete_item(self, item_id):
        if item_id in self.inventory:
            del self.inventory[item_id]
            print("Artículo eliminado con éxito.")
        else:
            print("Artículo no encontrado.")

    def show_inventory(self):
        for item_id, item in self.inventory.items():
            print(f"ID: {item_id}, Nombre: {item['name']}, Cantidad: {item['quantity']}, Precio: {item['price']}")


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
            item_id = input("ID del artículo: ")
            name = input("Nombre del artículo: ")
            quantity = int(input("Cantidad del artículo: "))
            price = float(input("Precio del artículo: "))
            app.register_item(item_id, name, quantity, price)

        elif option == 2:
            item_id = input("ID del artículo a buscar: ")
            app.search_item(item_id)

        elif option == 3:
            item_id = input("ID del artículo a editar: ")
            new_name = input("Nuevo nombre del artículo: ")
            new_quantity = int(input("Nueva cantidad del artículo: "))
            new_price = float(input("Nuevo precio del artículo: "))
            app.edit_item(item_id, new_name, new_quantity, new_price)

        elif option == 4:
            item_id = input("ID del artículo a eliminar: ")
            app.delete_item(item_id)

        elif option == 5:
            app.show_inventory()

        elif option == 6:
            print("Gracias por usar el sistema de inventario.")
            break

        else:
            print("Opción inválida, por favor selecciona una opción válida.")


if __name__ == "__main__":
    main()
