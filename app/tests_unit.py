from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from app.models import (
    Client,
    Med,
    Pet,
    Product,
    Provider,
    Veterinary,
    validate_pet,
    validate_provider,
    validate_veterinary,
)


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
        """
        Verifica que se pueda crear y obtener un cliente
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "5454221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(str(clients[0].phone), "5454221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        """
        Verifica que se pueda actualizar los datos del clietne
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "5454221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(str(client.phone), "5454221555232")

        client.update_client({"phone": "54221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(str(client_updated.phone), "54221555233")

    def test_update_client_with_error(self):
        """
        Verifica que al momento de actualizar los clientes, no haya datos erroneos.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(str(client.phone), "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(str(client_updated.phone), "54221555232")

    def test_clients_delete(self):
        """
        Verifica que se puede eliminar un cliente
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)
        initial_count = Client.objects.count()
        response = self.client.post(reverse('clients_delete'), {'client_id': client.id})
        self.assertEqual(Client.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('clients_repo'))

    def test_create_client_with_error_name(self):
        """
        Verifica que se no se pueda crear un cliente con un error
        """
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron 7",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        self.assertFalse(saved)
        self.assertEqual(errors["name"], "El nombre no puede contener números.")

    def test_update_client_with_error_name(self):
        """
        Verifica que no se pueda editar un cliente con un nombre que contenga numeros.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.name, "Juan Sebastian Veron")

        client.update_client({"cliente": "JSV7"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.name, "Juan Sebastian Veron")

    def test_cant_update_client_with_characters_in_phone_input(self):
        """
        Prueba que no se pueda actualizar un cliente con caracteres no numéricos en el teléfono.
        Asegura que el número de teléfono no cambia cuando se intenta actualizar con un valor inválido.
        """
        Client.save_client(
            {
                "name": "Benjamin Peres",
                "phone": "542214504505",
                "address": "1 y 60",
                "email": "benjaminperes@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client({"phone": "123asd"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(str(client_updated.phone), "542214504505")

    def test_cant_create_client_with_characters_in_phone_input(self):
        """
        Prueba que no se pueda crear un cliente con caracteres no numéricos en el teléfono.
        Asegura que el número de teléfono no pueda contener caracteres no númericos.
        """
        Client.save_client(
            {
                "name": "Benjamin Peres",
                "phone": "54221asd",
                "address": "1 y 60",
                "email": "benjaminperes@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 0)


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
        """
        Verifica que se pueda crear y obtener un proveedor
        """
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

    def test_address_not_null(self):
        """
        Verifica que el campo direccion tenga un valor.
        """
        data = {"name": "Farmacity S.A",
                "email": "moltito@hotmail.com",
                "address": "",}
        errors = validate_provider(data)
        expected_errors = {
            "address": "Por favor ingrese una direccion",
        }
        self.assertDictEqual(expected_errors, errors)

    def test_provider_delete(self):
        """
        Verifica que se pueda borrar un proveedor
        """
        Provider.save_provider(
            {
                "name": "Farmacity S.A",
                "email": "moltito@hotmail.com",
                "address": "Rio negro 2265",
            },
        )
        provider = Provider.objects.get(pk=1)
        initial_count = Provider.objects.count()
        response = self.client.post(reverse('providers_delete'), {'provider_id': provider.id})
        self.assertEqual(Provider.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('providers_repo'))

    def test_can_update_provider(self):
        """
        Verifica que se pueda actualizar los proveedores
        """
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
        """
        Verifica que al actualizar un proveedor, no permita actualizar con datos erroneos.
        """
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
        """
        Verifica que se pueda crear y obtener una medicina
        """
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

    def test_med_delete(self):
        """
        Verifica que se pueda eliminar una medicina
        """
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 8,
            },
        )
        medicine = Med.objects.get(pk=1)
        initial_count = Med.objects.count()
        response = self.client.post(reverse('meds_delete'), {'med_id': medicine.id})
        self.assertEqual(Med.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('meds_repo'))

    def test_can_update_medicine(self):
        """
        Verifica que se pueda actualizar una medicina
        """
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
        """
        Verifica que cuando se actualize una medicina, no se actualize con datos erroneos.
        """
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

    def test_can_create_with_invalid_dosis(self):
        """
        Verifica que un medicamento con dosis inválida (18) no se guarde.

        Pasos:
        1. Llama a `save_med` con dosis 18.
        2. Verifica que no haya medicamentos guardados.

        Resultado esperado:
        - `medicines` debe tener longitud 0.
        """
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 18,
            },
        )
        medicines = Med.objects.all()
        self.assertEqual(len(medicines), 0) #Si esto es así, significa que no guardó el medicamento porque tenía errores

    def test_can_update_invalid_medicine_dosis(self):
        """
        Verifica que no se permita actualizar un medicamento con una dosis inválida (18).

        Pasos:
        1. Guarda un medicamento con dosis válida (1).
        2. Verifica que la dosis inicial es 1.
        3. Intenta actualizar la dosis a 18.
        4. Verifica que la dosis no cambia.

        Resultado esperado:
        - La dosis del medicamento sigue siendo 1.
        """
        Med.save_med(
            {
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 1,
            },
        )
        medicine = Med.objects.get(pk=1)
        self.assertEqual(medicine.dose, 1)
        medicine.update_med({"dose": 18})
        medicine_updated = Med.objects.get(pk=1)
        self.assertEqual(medicine_updated.dose, 1)

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
        """
        Verifica que se pueda crear un producto con stock y recuperarlo correctamente de la base de datos.
        """
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
        """
        Verifica que se pueda actualizar el stock de un producto.
        """
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

    def test_product_delete(self):
        """
        Verifica que se eliminar un producto
        """
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        initial_count = Product.objects.count()
        response = self.client.post(reverse('products_delete'), {'product_id': product.id})
        self.assertEqual(Product.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('products_repo'))

    def test_update_product_stock_with_error_negative_value(self):
        """
        Verifica que al momento de actualizar un producto, no permita que este se actualize con un valor negativo en el atributo stock.
        """
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
        """
        Verifica que al momento de actualizar un producto, no permita que este se actualize con un valor de tipo string en el atributo stock.
        """
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
        """
        Verifica que al momento de actualizar un producto, no permita que este se actualize con un valor nulo en el atributo stock.
        """
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

    def test_increment_stock(self):
        """
        Verifica que el atributo stock pueda incrementarse.
        """
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        initial_stock = product.stock
        response = self.client.post(reverse('increment_stock', args=[product.id]))
        product.refresh_from_db()
        self.assertEqual(product.stock, initial_stock + 1)
        self.assertRedirects(response, reverse('products_repo'))

    def test_decrement_stock(self):
        """
        Verifica que el atributo stock pueda decrementarse.
        """
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "50",
            },
        )
        product = Product.objects.get(pk=1)
        initial_stock = product.stock
        response = self.client.post(reverse('decrement_stock', args=[product.id]))
        product.refresh_from_db()
        self.assertEqual(product.stock, initial_stock - 1)
        self.assertRedirects(response, reverse('products_repo'))

    def test_decrement_stock_zero(self):
        """
        Verifica que el atributo stock no pueda decrementarse mas alla del valor 0.
        """
        Product.save_product(
            {
                "name": "Lavandina",
                "type": "Limpieza",
                "price": "100",
                "stock": "0",
            },
        )
        product = Product.objects.get(pk=1)
        initial_stock = product.stock
        response = self.client.post(reverse('decrement_stock', args=[product.id]))
        product.refresh_from_db()
        self.assertEqual(product.stock, initial_stock)
        self.assertRedirects(response, reverse('products_repo'))

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
        """
        Verifica que se cree una mascota correctamente con los valores del atributo breed correspondientes.
        """
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
        """
        Verifica que el atributo breed se actualize con un nuevo valor de manera correcta.
        """
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

    def test_pet_delete(self):
        """
        Verifica que se pueda eliminar una mascota
        """
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Benita",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )
        pet = Pet.objects.get(pk=1)
        initial_count = Pet.objects.count()
        response = self.client.post(reverse('pets_delete'), {'pet_id': pet.id})
        self.assertEqual(Pet.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('pets_repo'))

    def test_update_pet_with_error(self):
        """
        Verifica que al actualizar los datos de una mascota, no se pueda actualizar con datos erroneos.-
        """
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
        """
        Verifica que el atributo birthday no pueda actualizarse con una fecha invalida.
        """
        future_birthday = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        pet_data = {
            "name": "Paco",
            "breed": "Perro",
            "birthday": future_birthday,
        }
        errors = validate_pet(pet_data)
        self.assertIn("birthday", errors)
        self.assertEqual(errors["birthday"], "La fecha de nacimiento no puede ser posterior al día actual.")

    def test_update_pet_with_birthay_after_current_date(self):
        """
        Verifico que cuando se actualiza la fecha cumpla con la restriccion de tiempo.
        """
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Paco",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )

        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.birthday, date(2021, 1, 1))  # Comparar objetos datetime.date

        pet.update_pet({"birthday": "2028-10-10"})

        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.birthday, date(2021, 1, 1))

    def test_update_pet_with_invalid_birthday(self):
        """
        Verifica que la fecha no sea invalida
        """
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        Pet.save_pet(
            {
                "name": "Paco",
                "breed": "Perro",
                "birthday": pet_birthday,
            },
        )

        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.birthday, date(2021, 1, 1))  # Comparar objetos datetime.date

        pet.update_pet({"birthday": "aaaaaa"})

        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.birthday, date(2021, 1, 1))


class VeterinaryModelTest(TestCase):
    """
    Prueba para el modelo de datos Veterinary.
    Esta clase contiene pruebas para verificar la funcionalidad de creación
    y recuperación de registros en el modelo Veterinary. Se asegura de que
    los datos se almacenen y se recuperen correctamente desde la base de datos.
    """
    def test_can_create_and_get_vet(self):
        """
        Verifica que se pueda crear y obtener un nuevo veterinario
        """
        Veterinary.save_veterinary(
            {
                "name": "Jose Rodriguez",
                "phone": "2214504505",
                "email": "joser@hotmail.com",
            },
        )
        veterinaries = Veterinary.objects.all()
        self.assertEqual(len(veterinaries), 1)

        self.assertEqual(veterinaries[0].name, "Jose Rodriguez")
        self.assertEqual(veterinaries[0].phone, "2214504505")
        self.assertEqual(veterinaries[0].email, "joser@hotmail.com")

    def test_vet_delete(self):
        """
        Verifica que se puede eliminar un veterinario ya creado
        """
        Veterinary.save_veterinary(
            {
                "name": "Jose Rodriguez",
                "phone": "2214504505",
                "email": "joser@hotmail.com",
            },
        )
        veterinary = Veterinary.objects.get(pk=1)
        initial_count = Veterinary.objects.count()
        response = self.client.post(reverse('veterinary_delete'), {'veterinary_id': veterinary.id})
        self.assertEqual(Veterinary.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('veterinary_repo'))

    def test_validate_veterinary_empty_data(self):
        """
        Verifica que al momento de crear un nuevo veterinario no se cree con valores nulos
        """
        data = {}
        errors = validate_veterinary(data)
        expected_errors = {
            "name": "Por favor ingrese un nombre",
            "phone": "Por favor ingrese un teléfono",
            "email": "Por favor ingrese un email",
        }
        self.assertDictEqual(expected_errors, errors)

    def test_validate_wrong_email(self):
        """
        Verifica que el atributo email del veterinario este en el formato correcto
        """
        data = {"name": "Jose Rodriguez",
                "phone": "2214504505",
                "email": "joserhotmail.com",}
        errors = validate_veterinary(data)
        expected_errors = {
            "email": "Por favor ingrese un email valido",
        }
        self.assertDictEqual(expected_errors, errors)

    def test_cant_update_veterinary_with_error(self):
        """
        Verifica que se pueda actualizar un veterinario sin datos erroneos.
        """
        Veterinary.save_veterinary(
            {
                "name": "Jose Rodriguez",
                "phone": "2214504505",
                "email": "joser@hotmail.com",
            },
        )
        veterinary = Veterinary.objects.get(pk=1)
        self.assertEqual(veterinary.phone, "2214504505")
        veterinary.update_veterinary({"phone": "2214504506"})
        veterinary_updated = Veterinary.objects.get(pk=1)
        self.assertEqual(veterinary_updated.phone, "2214504506")
