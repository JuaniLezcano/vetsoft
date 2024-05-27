from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Product, Pet
from datetime import date, timedelta


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
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

class ProductsTest(TestCase):
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