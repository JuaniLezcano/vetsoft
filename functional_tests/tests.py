import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import Client, Product, Pet, Med, Provider
from datetime import date

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

class MedicineRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        expect(self.page.get_by_text("No existen medicamentos")).to_be_visible()

    def test_should_show_medicines_data(self):
        Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        Med.objects.create(
            name="Ubuprofendog",
            desc="Este medicamento es para vomitos felinos",
            dose=2,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        expect(self.page.get_by_text("No existen medicamentos")).not_to_be_visible()

        expect(self.page.get_by_text("Paracetamoldog")).to_be_visible()
        expect(self.page.get_by_text("Este medicamento es para vomitos caninos")).to_be_visible()
        expect(self.page.get_by_text("8")).to_be_visible()

        expect(self.page.get_by_text("Ubuprofendog")).to_be_visible()
        expect(self.page.get_by_text("Este medicamento es para vomitos felinos")).to_be_visible()
        expect(self.page.get_by_text("2")).to_be_visible()

    def test_should_show_add_medicine_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nuevo Medicamento", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("meds_form"))

    def test_should_show_medicine_edit_action(self):
        medicine = Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("meds_edit", kwargs={"id": medicine.id})
        )

    def test_should_show_medicine_delete_action(self):
        medicine = Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de medicamentos"
        )
        medicine_id_input = edit_form.locator("input[name=med_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("meds_delete"))
        expect(medicine_id_input).not_to_be_visible()
        expect(medicine_id_input).to_have_value(str(medicine.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        expect(self.page.get_by_text("Paracetamoldog")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("meds_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Paracetamoldog")).not_to_be_visible()

class productCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_product(self):
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Lavandina")
        self.page.get_by_label("Tipo").fill("Limpieza")
        self.page.get_by_label("Precio").fill("100")
        self.page.get_by_label("Stock").fill("50")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Lavandina")).to_be_visible()
        expect(self.page.get_by_text("Limpieza")).to_be_visible()
        expect(self.page.get_by_text("100")).to_be_visible()
        expect(self.page.get_by_text("50")).to_be_visible()

    def test_increase_stock_product_by_touching_button(self):
        product = Product.objects.create(
            name="Lavandina",
            type="Limpieza",
            price=100,
            stock=50,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")
        expect(self.page.get_by_text("Lavandina")).to_be_visible()
        expect(self.page.get_by_text("Limpieza")).to_be_visible()
        expect(self.page.get_by_text("100")).to_be_visible()
        expect(self.page.get_by_text("50")).to_be_visible()

        self.page.get_by_role("button", name="+").click()

        expect(self.page.get_by_text("50")).not_to_be_visible()
        expect(self.page.get_by_text("51")).to_be_visible()

    def test_edit_form_should_be_able_to_throw_an_error_if_negative_stock(self):
        product = Product.objects.create(
            name="Lavandina",
            type="Limpieza",
            price=100,
            stock=50,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")
        expect(self.page.get_by_text("Lavandina")).to_be_visible()
        expect(self.page.get_by_text("Limpieza")).to_be_visible()
        expect(self.page.get_by_text("100")).to_be_visible()
        expect(self.page.get_by_text("50")).to_be_visible()

        self.page.get_by_role("link", name="Editar").click()
        expect(self.page.get_by_label("Nombre")).to_have_value("Lavandina")
        expect(self.page.get_by_label("Tipo")).to_have_value("Limpieza")
        expect(self.page.get_by_label("Precio")).to_have_value("100.0")
        expect(self.page.get_by_label("Stock")).to_have_value("50")

        self.page.evaluate("document.querySelector('input[name=stock]').value = '-100'")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_label("Nombre")).to_have_value("Lavandina")
        expect(self.page.get_by_label("Tipo")).to_have_value("Limpieza")
        expect(self.page.get_by_label("Precio")).to_have_value("100.0")
        expect(self.page.get_by_label("Stock")).to_have_value("-100")
        expect(self.page.get_by_text("El stock no puede ser negativo."))

class PetCreateEditTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_be_able_to_create_a_new_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Benita")
        self.page.get_by_label("Raza").select_option("Perro")
        self.page.get_by_label("Nacimiento").fill("2021-01-01")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Benita")).to_be_visible()
        expect(self.page.get_by_text("Perro")).to_be_visible()
        expect(self.page.get_by_text("Jan. 1, 2021")).to_be_visible()
    
    def test_should_view_errors_if_form_pet_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Benita")
        self.page.get_by_label("Raza").select_option("")
        self.page.get_by_label("Nacimiento").fill("2021-01-01")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento")).not_to_be_visible()
    
    def test_should_be_able_to_edit_a_pet(self):
        pet_birthday = (date(2021, 1, 1)).strftime("%Y-%m-%d")
        pet = Pet.objects.create(
            name="Benita",
            breed="Perro",
            birthday=pet_birthday,
        )

        path = reverse("pets_edit", kwargs={"id": pet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Rocco")
        self.page.get_by_label("Raza").select_option("Gato")
        self.page.get_by_label("Nacimiento").fill("2016-02-02")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Benita")).not_to_be_visible()
        expect(self.page.get_by_text("Perro")).not_to_be_visible()
        expect(self.page.get_by_text("Jan. 1, 2021")).not_to_be_visible()

        expect(self.page.get_by_text("Rocco")).to_be_visible()
        expect(self.page.get_by_text("Gato")).to_be_visible()
        expect(self.page.get_by_text("Feb. 2, 2016")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute("href", reverse("pets_edit", kwargs={"id": pet.id}))

    def test_edit_form_should_be_able_to_throw_an_error_if(self):
        pet = Pet.objects.create(
            name="Paco",
            breed="Perro",
            birthday="2008-05-10"
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        expect(self.page.get_by_text("Paco")).to_be_visible()
        expect(self.page.get_by_text("Perro")).to_be_visible()
        expect(self.page.get_by_text("May 10, 2008")).to_be_visible()

        self.page.get_by_role("link", name="Editar").click()
        expect(self.page.get_by_label("Nombre")).to_have_value("Paco")
        breed_select = self.page.get_by_label("Raza")
        expect(breed_select).to_have_value("Perro")
        expect(self.page.get_by_label("Nacimiento")).to_have_value("2008-05-10")

        self.page.evaluate("document.querySelector('input[name=birthday]').value = '2028-05-10'")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_label("Nombre")).to_have_value("Paco")
        breed_select = self.page.get_by_label("Raza")
        expect(breed_select).to_have_value("Perro")
        expect(self.page.get_by_label("Nacimiento")).to_have_value("")
        expect(self.page.get_by_text("La fecha de nacimiento no puede ser posterior al día actual."))