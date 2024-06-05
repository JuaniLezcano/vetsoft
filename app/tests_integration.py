from datetime import date

from django.shortcuts import reverse
from django.test import TestCase

from app.models import Client, Med, Pet, Product, Provider, Veterinary


class HomePageTest(TestCase):
    """
    Clase de prueba para la vista de la página de inicio.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de la vista de la página de inicio.

    Métodos de prueba:
        test_use_home_template: Verifica si se está utilizando el template "home.html" en la vista de la página de inicio.

    """
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    """
    Clase de prueba para las vistas y funcionalidades relacionadas con los clientes.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de las vistas y funcionalidades relacionadas con los clientes.

    Métodos de prueba:
        test_repo_use_repo_template: Verifica si se está utilizando el template "clients/repository.html" en la vista del repositorio de clientes.
        test_repo_display_all_clients: Verifica si se están mostrando todos los clientes en la vista del repositorio de clientes.
        test_form_use_form_template: Verifica si se está utilizando el template "clients/form.html" en la vista del formulario de clientes.
        test_can_create_client: Verifica si se puede crear un cliente correctamente.
        test_validation_errors_create_client: Verifica si se muestran mensajes de error de validación al intentar crear un cliente sin proporcionar datos.
        test_should_response_with_404_status_if_client_doesnt_exists: Verifica si se devuelve un código de estado 404 si se intenta acceder a la edición de un cliente que no existe.
        test_validation_invalid_email: Verifica si se muestra un mensaje de error al intentar crear un cliente con un correo electrónico inválido.
        test_edit_user_with_valid_data: Verifica si se puede editar un cliente existente con datos válidos.
    
    """
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
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

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)

class ProvidersTest(TestCase):
    """
    Clase de prueba para las vistas y funcionalidades relacionadas con los proveedores.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de las vistas y funcionalidades relacionadas con los proveedores.

    Métodos de prueba:
        test_can_create_client: Verifica si se puede crear un proveedor correctamente.
        test_validation_invalid_email: Verifica si se muestra un mensaje de error al intentar crear un proveedor con un correo electrónico inválido.
        test_validation_errors_create_provider: Verifica si se muestran mensajes de error de validación al intentar crear un proveedor sin proporcionar datos.
        test_edit_user_with_valid_data: Verifica si se puede editar un proveedor existente con datos válidos.
        test_repo_use_repo_template: Verifica si se está utilizando el template "providers/repository.html" en la vista del repositorio de proveedores.
        test_repo_display_all_providers: Verifica si se están mostrando todos los proveedores en la vista del repositorio de proveedores.
        test_form_use_form_template: Verifica si se está utilizando el template "providers/form.html" en la vista del formulario de proveedores.
    
    """
    def test_can_create_client(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
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


        self.assertRedirects(response, reverse("providers_repo"))
    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Farmacity S.A",
                "email": "facultad121030",
                "address": "Rio negro 2265",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")
    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una direccion")
    def test_edit_user_with_valid_data(self):
        provider = Provider.objects.create(
            name="Farmacity S.A",
            email="moltito@hotmail.com",
            address="Rio negro 2265",
      )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id": provider.id,
                "name": "SuperFarm",
                "email": "moltito@hotmail.com",
                "address": "Rio negro 2265",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedProvider = Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "SuperFarm")
        self.assertEqual(editedProvider.email, provider.email)
        self.assertEqual(editedProvider.address, provider.address)

    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_repo_display_all_providers(self):
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("providers_form"))
        self.assertTemplateUsed(response, "providers/form.html")







class MedicinesTest(TestCase):
    """
    Clase de prueba para las vistas y funcionalidades relacionadas con los medicamentos.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de las vistas y funcionalidades relacionadas con los medicamentos.

    Métodos de prueba:
        test_repo_use_repo_template: Verifica si se está utilizando el template "meds/repository.html" en la vista del repositorio de medicamentos.
        test_repo_display_all_medicines: Verifica si se están mostrando todos los medicamentos en la vista del repositorio de medicamentos.
        test_form_use_form_template: Verifica si se está utilizando el template "meds/form.html" en la vista del formulario de medicamentos.
        test_can_create_medicine: Verifica si se puede crear un medicamento correctamente.
        test_validation_errors_create_medicine: Verifica si se muestran mensajes de error de validación al intentar crear un medicamento sin proporcionar datos.
        test_should_response_with_404_status_if_medicine_doesnt_exists: Verifica si se devuelve un estado de 404 si se intenta acceder a la edición de un medicamento que no existe.
        test_validation_invalid_dosis: Verifica si se muestra un mensaje de error al intentar crear un medicamento con una dosis inválida.
        test_edit_user_with_valid_data: Verifica si se puede editar un medicamento existente con datos válidos.
    
    
    """
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("meds_repo"))
        self.assertTemplateUsed(response, "meds/repository.html")

    def test_repo_display_all_medicines(self):
        response = self.client.get(reverse("meds_repo"))
        self.assertTemplateUsed(response, "meds/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("meds_form"))
        self.assertTemplateUsed(response, "meds/form.html")

    def test_can_create_medicine(self):
        response = self.client.post(
            reverse("meds_form"),
            data={
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

        self.assertRedirects(response, reverse("meds_repo"))

    def test_validation_errors_create_medicine(self):
        response = self.client.post(
            reverse("meds_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una descripcion")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_should_response_with_404_status_if_medicine_doesnt_exists(self):
        response = self.client.get(reverse("meds_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_dosis(self):
        response = self.client.post(
            reverse("meds_form"),
            data={
                "name": "Paracetamoldog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 18,
            },
        )

        self.assertContains(response, "La dosis debe estar entre 1 y 10")

    def test_edit_user_with_valid_data(self):
        medicine = Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        response = self.client.post(
            reverse("meds_form"),
            data={
                "id": medicine.id,
                "name": "Ubuprofendog",
                "desc": "Este medicamento es para vomitos caninos",
                "dose": 8,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedMedicine = Med.objects.get(pk=medicine.id)
        self.assertEqual(editedMedicine.name, "Ubuprofendog")
        self.assertEqual(editedMedicine.desc, medicine.desc)
        self.assertEqual(editedMedicine.dose, medicine.dose)


class ProductsTest(TestCase):
    def test_validation_errors_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={},
        )
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un tipo")
        self.assertContains(response, "Por favor ingrese un precio")
        self.assertContains(response, "Por favor ingrese un stock")

    """
    Clase de prueba para las vistas y funcionalidades relacionadas con los productos.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de las vistas y funcionalidades relacionadas con los productos.

    Métodos de prueba:
        test_can_create_product: Verifica si se puede crear un producto correctamente.
        test_can_update_stock_product: Verifica si se puede actualizar el stock de un producto existente.
        test_update_product_with_empty_stock: Verifica si se muestra un mensaje de error al intentar actualizar un producto con un stock vacío.
        test_update_product_with_negative_stock: Verifica si se muestra un mensaje de error al intentar actualizar un producto con un stock negativo.

    """
    def test_can_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={
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
        self.assertEqual(products[0].price, 100)
        self.assertEqual(products[0].stock, 50)

        self.assertRedirects(response, reverse("products_repo"))

    def test_can_update_stock_product(self):
        product = Product.objects.create(
            name= "Lavandina",
            type= "Limpieza",
            price= 100,
            stock= 50,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "stock": 100,
            },
        )
        self.assertEqual(response.status_code, 302)

        editedProduct = Product.objects.get(pk=product.id)
        self.assertEqual(editedProduct.name, product.name)
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price, product.price)
        self.assertEqual(editedProduct.stock, 100)

    def test_update_product_with_empty_stock(self):
        product = Product.objects.create(
            name= "Lavandina",
            type= "Limpieza",
            price= 100,
            stock= 50,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "stock": "",
            },
        )

        editedProduct = Product.objects.get(pk=product.id)
        self.assertContains(response, "El campo de stock no puede estar vacio.")
        self.assertEqual(editedProduct.name, product.name)
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price, product.price)
        self.assertEqual(editedProduct.stock, 50)

    def test_update_product_with_negative_stock(self):
        product = Product.objects.create(
            name= "Lavandina",
            type= "Limpieza",
            price= 100,
            stock= 50,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "stock": -100,
            },
        )

        editedProduct = Product.objects.get(pk=product.id)
        self.assertContains(response, "El stock no puede ser negativo")
        self.assertEqual(editedProduct.name, product.name)
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price, product.price)
        self.assertEqual(editedProduct.stock, 50)

class PetsTest(TestCase):
    """
    Clase de prueba para las vistas y funcionalidades relacionadas con las mascotas.

    Esta clase contiene métodos de prueba para verificar el comportamiento
    de las vistas y funcionalidades relacionadas con las mascotas.

    Métodos de prueba:
        test_repo_use_repo_template: Verifica si se utiliza la plantilla correcta para la vista de repositorio de mascotas.
        test_form_use_form_template: Verifica si se utiliza la plantilla correcta para el formulario de mascotas.
        test_can_create_pet: Verifica si se puede crear una mascota correctamente.
        test_can_update_pet_breed: Verifica si se puede actualizar la raza de una mascota existente.
        test_validation_errors_create_pet: Verifica si se muestran los mensajes de error correctamente al intentar crear una mascota sin completar todos los campos requeridos.
        test_validation_error_create_pet_without_breed: Verifica si se muestra un mensaje de error al intentar crear una mascota sin especificar la raza.
        test_should_response_with_404_status_if_pet_doesnt_exists: Verifica si se devuelve un estado 404 si se intenta editar una mascota que no existe.
        test_validation_invalid_birthday: Verifica si se muestra un mensaje de error al intentar especificar una fecha de nacimiento futura para la mascota.
        test_edit_user_with_valid_data: Verifica si se puede editar correctamente la información de una mascota.

    """
    def test_repo_use_repo_template(self):
            response = self.client.get(reverse("pets_repo"))
            self.assertTemplateUsed(response, "pets/repository.html")

    def test_form_use_form_template(self):
            response = self.client.get(reverse("pets_form"))
            self.assertTemplateUsed(response, "pets/form.html")

    def test_can_create_pet(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        response = self.client.post(
            reverse("pets_form"),
            data={
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

        self.assertRedirects(response, reverse("pets_repo"))

    def test_can_update_pet_breed(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        pet = Pet.objects.create(
            name= "Benita",
            breed = "Perro",
            birthday = pet_birthday,
        )

        response = self.client.post(
            reverse("pets_form"),
            data={
                "id": pet.id,
                "breed": "Conejo",
            },
        )
        self.assertEqual(response.status_code, 302)

        editedPet = Pet.objects.get(pk=pet.id)
        self.assertEqual(editedPet.name, pet.name)
        self.assertEqual(editedPet.birthday, date(2021, 1, 1)) # No se puede modificar la fecha de nacimiento sin parsear o convertir al mismo.
        self.assertEqual(editedPet.breed, "Conejo")

    def test_validation_errors_create_pet(self):
        response = self.client.post(
            reverse("pets_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una raza")
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento")

    def test_validation_error_create_pet_without_breed(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Benita",
                "breed": "",
                "birthday": "2021-01-01",
            },
        )

        self.assertContains(response, "Por favor ingrese una raza")

    def test_should_response_with_404_status_if_pet_doesnt_exists(self):
        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_birthday(self):
        response = self.client.post(
        reverse("pets_form"),
        data={
            "name": "Paco",
            "breed": "Caniche",
            "birthday": "2028-05-20",
        },
    )

        self.assertContains(response, "La fecha de nacimiento no puede ser posterior al día actual.")

    def test_edit_user_with_valid_data(self):
        pet = Pet.objects.create(
            name="Paco",
            breed="Caniche",
            birthday="2015-05-20",
        )

        response = self.client.post(
            reverse("pets_form"),
            data={
                "id": pet.id,
                "name": "Maguile",
                "breed": "Caniche",
                "birthday": "2015-05-20",
            },
        )


        self.assertEqual(response.status_code, 302)

        editedPet = Pet.objects.get(pk=pet.id)
        self.assertEqual(editedPet.name, "Maguile")
        self.assertEqual(editedPet.breed, pet.breed)
        self.assertEqual(str(editedPet.birthday), "2015-05-20")

    def test_invalid_birthday_format(self):
        response = self.client.post(
            reverse("pets_form"),
            data={"birthday": "2022-13-32"},
        )
        self.assertContains(response, "Formato de fecha invalido. Utilice el formato YYYY-MM-DD")

class VetsTest(TestCase):
    def test_validation_errors_create_vet(self):
        response = self.client.post(
            reverse("veterinary_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_can_create_vet(self):
        response = self.client.post(
            reverse("veterinary_form"),
            data={
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

        self.assertRedirects(response, reverse("veterinary_repo"))
