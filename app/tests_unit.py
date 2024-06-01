from django.test import TestCase
from django.urls import reverse
from app.models import Client, Product, Pet, Med, validate_pet, Provider, Veterinary, validate_veterinary
from datetime import date, timedelta


class ClientModelTest(TestCase):
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
        
    def test_clients_delete(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        client = Client.objects.get(pk=1)
        initial_count = Client.objects.count()
        response = self.client.post(reverse('clients_delete'), {'client_id': client.id})
        self.assertEqual(Client.objects.count(), initial_count - 1)
        self.assertRedirects(response, reverse('clients_repo'))

class ProviderModelTest(TestCase):
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

    def test_provider_delete(self):
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

    def test_med_delete(self):
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
        
    def test_product_delete(self):
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
    
    def test_increment_stock(self):
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

    def test_pet_delete(self):
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
    

    
class VeterinaryModelTest(TestCase):
    def test_can_create_and_get_vet(self):
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
        data = {}
        errors = validate_veterinary(data)
        expected_errors = {
            "name": "Por favor ingrese un nombre",
            "phone": "Por favor ingrese un teléfono",
            "email": "Por favor ingrese un email",
        }
        self.assertDictEqual(expected_errors, errors)
        
    def test_validate_wrong_email(self):
        data = {"name": "Jose Rodriguez",
                "phone": "2214504505",
                "email": "joserhotmail.com",}
        errors = validate_veterinary(data)
        expected_errors = {
            "email": "Por favor ingrese un email valido",
        }
        self.assertDictEqual(expected_errors, errors)
        
    def test_cant_update_veterinary_with_error(self):
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