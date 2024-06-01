from django.test import TestCase
from app.models import Client, Product, Pet, Med, validate_pet, Provider
from datetime import date, timedelta


class ClientModelTest(TestCase):
    """
    Clase de prueba para el modelo Client.

    Esta clase contiene métodos de prueba para verificar la creación y actualización
    de objetos de cliente en el modelo Client.

    Métodos de prueba:
        test_can_create_and_get_client: Verifica si se puede crear y obtener un cliente correctamente.
        test_can_update_client: Verifica si se puede actualizar la información de un cliente correctamente.
        test_update_client_with_error: Verifica si el cliente no se actualiza cuando se proporciona un valor de teléfono vacío.
    
    """
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class ProviderModelTest(TestCase):
    """
    Clase de prueba para el modelo Provider.

    Esta clase contiene métodos de prueba para verificar la creación y actualización
    de objetos de proveedor en el modelo Provider.

    Métodos de prueba:
        test_can_create_and_get_provider: Verifica si se puede crear y obtener un proveedor correctamente.
        test_can_update_provider: Verifica si se puede actualizar la información de un proveedor correctamente.
        test_update_provider_with_error: Verifica si el proveedor no se actualiza cuando se proporciona una dirección vacía.
    
    """
    def test_can_create_and_get_provider(self):
        Provider.save_provider(
            {
                "name": "Farmacity S.A",
                "email": "moltito@hotmail.com",
                "address": "Rio negro 2265",

            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Farmacity S.A")
        self.assertEqual(providers[0].email, "moltito@hotmail.com")
        self.assertEqual(providers[0].address, "Rio negro 2265")

    def test_can_update_provider(self):
        Provider.save_provider(
            {
                "name": "Farmacity S.A",
                "email": "moltito@hotmail.com",
                "address": "Rio negro 2265",

            },
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.address, "Rio negro 2265")

        provider.update_provider({"address": "Cardenal pironio 2265"})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.address, "Cardenal pironio 2265")

    def test_update_provider_with_error(self):
        Provider.save_provider(
            {
                "name": "Farmacity S.A",
                "email": "moltito@hotmail.com",
                "address": "Rio negro 2265",
            },
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.address, "Rio negro 2265")

        provider.update_provider({"address": ""})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.address, "Rio negro 2265")


class MedicineModelTest(TestCase):
    """
    Clase de prueba para el modelo de Medicamento (Med).

    Esta clase contiene métodos de prueba para verificar la creación y actualización
    de objetos de medicamento en el modelo Med.

    Métodos de prueba:
        test_can_create_and_get_medicine: Verifica si se puede crear y obtener un medicamento correctamente.
        test_can_update_medicine: Verifica si se puede actualizar la información de un medicamento correctamente.
        test_update_medicine_with_error: Verifica si el medicamento no se actualiza cuando se proporciona una dosis vacía.
    
    """
    def test_can_create_and_get_medicine(self):
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 8,
            },
        )
        medicines = Med.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamoldog")
        self.assertEqual(medicines[0].desc, "Este medicamento es para vomitos caninos")
        self.assertEqual(medicines[0].dose, 8)

    def test_can_update_medicine(self):
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 8,
            },
        )
        medicine = Med.objects.get(pk=1)

        self.assertEqual(medicine.dose, 8)

        medicine.update_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 7,
            },
        )

        medicine_updated = Med.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 7)

    def test_update_medicine_with_error(self):
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 8,
            },
        )
        medicine = Med.objects.get(pk=1)

        self.assertEqual(medicine.dose, 8)

        medicine.update_med({"dose": ""})

        medicine_updated = Med.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 8)

class ProductModelTest(TestCase):
    """
    Clase de prueba para el modelo de Producto (Product).

    Esta clase contiene métodos de prueba para verificar la creación y actualización
    de objetos de producto en el modelo Product.

    Métodos de prueba:
        test_can_create_and_get_product_with_stock: Verifica si se puede crear y obtener un producto con stock correctamente.
        test_can_update_product_stock: Verifica si se puede actualizar el stock de un producto correctamente.
        test_update_product_stock_with_error_negative_value: Verifica que el stock del producto no se actualice si se proporciona un valor negativo.
        test_update_product_stock_with_error_string_value: Verifica que el stock del producto no se actualice si se proporciona un valor no numérico.
        test_update_product_stock_with_error_empty_value: Verifica que el stock del producto no se actualice si se proporciona un valor vacío.
    
    """
    def test_can_create_and_get_product_with_stock(self):
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Lavandina")
        self.assertEqual(products[0].type, "Limpieza")
        self.assertEqual(products[0].price, 100.0)
        self.assertEqual(products[0].stock, 50)

    def test_can_update_product_stock(self):
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.stock, 50)
        product.update_product({"stock":"75"})
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.stock, 75)
        
    def test_update_product_stock_with_error_negative_value(self):
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.stock, 50)
        product.update_product({"stock":"-75"})
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.stock, 50)
        
    def test_update_product_stock_with_error_string_value(self):
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.stock, 50)
        product.update_product({"stock":"asd"})
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.stock, 50)
    
    def test_update_product_stock_with_error_empty_value(self):
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.stock, 50)
        product.update_product({"stock":""})
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.stock, 50)

class PetModelTest(TestCase):
    """
    Clase de prueba para el modelo de Mascota (Pet).

    Esta clase contiene métodos de prueba para verificar la creación y actualización
    de objetos de mascota en el modelo Pet.

    Métodos de prueba:
        test_can_create_pet_with_breed_options: Verifica si se puede crear una mascota con opciones de raza válidas.
        test_can_update_pet_breed: Verifica si se puede actualizar la raza de una mascota correctamente.
        test_update_pet_with_error: Verifica que la raza de la mascota no se actualice si se proporciona un valor vacío.
        test_cant_invalidate_birthday: Verifica que no se pueda crear una mascota con una fecha de nacimiento futura.

   
    """
    def test_can_create_pet_with_breed_options(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Benita",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )

        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, "Benita")
        self.assertEqual(pets[0].breed, "Perro")
        self.assertEqual(pets[0].birthday, date(2021, 1, 1))

    def test_can_update_pet_breed(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Benita",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )

        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.breed, "Perro")
        pet.update_pet({"breed": "Gato"})
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.breed, "Gato")

    def test_update_pet_with_error(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Benita",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )

        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.breed, "Perro")
        pet.update_pet({"breed": ""})
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.breed, "Perro")
    
    def test_cant_invalidate_birthday(self):
        future_birthday = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        pet_data = {
            "name": "Paco",
            "breed": "Perro",
            "birthday": future_birthday,
        }
        errors = validate_pet(pet_data)
        self.assertIn("birthday", errors)
        self.assertEqual(errors["birthday"], "La fecha de nacimiento no puede ser posterior al día actual.")
    
    