import os
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Med, Pet, Product, Provider

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    """
    Clase base para pruebas utilizando Playwright.

    Esta clase proporciona configuraciones básicas para ejecutar pruebas utilizando
    el framework Playwright. Configura un navegador web y proporciona métodos de
    configuración y limpieza.

    Atributos de Clase:
        browser (Browser): Instancia del navegador web.
        headless (bool): Define si el navegador se ejecutará en modo headless.
        slow_mo (int): Retardo en milisegundos para ralentizar la ejecución del navegador.

    Métodos de Clase:
        setUpClass: Configura el navegador antes de iniciar las pruebas.
        tearDownClass: Cierra el navegador después de finalizar las pruebas.

    Métodos:
        setUp: Configura una nueva página del navegador antes de cada prueba.
        tearDown: Cierra la página del navegador después de cada prueba.
    """
    @classmethod
    def setUpClass(cls):
        """
        Configura el entorno de prueba para ejecutar pruebas con un navegador Firefox utilizando Playwright.

        Este método se ejecuta una vez antes de todas las pruebas de la clase. Lanza una instancia de
        Firefox en modo sin cabeza (headless) o con un retraso en las acciones (slow_mo) según las configuraciones
        proporcionadas.
        """
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo),
        )

    @classmethod
    def tearDownClass(cls):
        """
        Limpia el entorno de prueba cerrando el navegador lanzado por Playwright.
        """
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        """
        Configura el entorno de prueba para ejecutar pruebas con un navegador Firefox utilizando Playwright.
        """
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        """
        Configura el entorno de prueba para ejecutar pruebas con un navegador Firefox utilizando Playwright.
        """
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """
    Clase de caso de prueba para probar la funcionalidad de la página de inicio.

    Esta clase incluye métodos de prueba para verificar la presencia de la barra de navegación con enlaces y tarjetas de inicio con enlaces.
    """
    def test_should_have_navbar_with_links(self):
        """
        Verifica que la barra de navegación tenga los enlaces correctos.
        """
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
        """
        Verifica que la página de inicio tenga tarjetas con enlaces correctos.
        """
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    """
    Clase de caso de prueba para probar la funcionalidad del repositorio de clientes.

    Esta clase incluye métodos de prueba para verificar si se muestra un mensaje si la tabla está vacía,
    mostrar datos de clientes, mostrar la acción para agregar un cliente, mostrar la acción para editar un cliente
    y mostrar la acción para eliminar un cliente.
    """
    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla de clientes está vacía.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """
        Verifica que se muestren los datos de los clientes en la tabla de clientes.

        Este método realiza una prueba funcional que:
        1. Crea dos clientes en la base de datos.
        2. Navega a la URL del repositorio de clientes.
        3. Verifica que el mensaje "No existen clientes" no sea visible.
        4. Verifica que los datos de ambos clientes sean visibles en la página.

        Pasos:
        1. Crea dos clientes con diferentes datos.
        2. Navega a la URL del repositorio de clientes en el servidor en vivo.
        3. Verifica que el mensaje "No existen clientes" no se muestre.
        4. Verifica que los nombres, direcciones, teléfonos y correos electrónicos de ambos clientes sean visibles en la página.
        """
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="54221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """
        Verifica que se muestre la acción para agregar un nuevo cliente en el repositorio de clientes.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """
        Verifica que se muestre la acción para editar un cliente en el repositorio de clientes.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_show_client_delete_action(self):
        """
        Verifica que se muestre la acción para eliminar un cliente en el repositorio de clientes.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente",
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """
        Verifica que se pueda eliminar un cliente desde el repositorio de clientes.
        """
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
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
    """
    Clase de caso de prueba para probar la creación y edición de clientes.

    Esta clase incluye métodos de prueba para:
    - Crear un nuevo cliente.
    - Ver errores si el formulario es inválido.
    - Editar un cliente existente.
    """
    def test_should_be_able_to_create_a_new_client(self):
        """
        Verifica que se pueda crear un nuevo cliente utilizando el formulario de clientes.

        Este método realiza una prueba funcional que:
        1. Navega a la URL del formulario de creación de clientes en el servidor en vivo.
        2. Verifica que el formulario sea visible en la página.
        3. Rellena el formulario con datos de cliente.
        4. Envía el formulario haciendo clic en el botón "Guardar".
        5. Verifica que los detalles del cliente recién creado sean visibles en la página.

        Pasos:
        1. Navega a la URL del formulario de creación de clientes en el servidor en vivo.
        2. Verifica que el formulario sea visible en la página.
        3. Rellena el formulario con datos de cliente.
        4. Envía el formulario haciendo clic en el botón "Guardar".
        5. Verifica que los detalles del cliente recién creado sean visibles en la página.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren los errores en el formulario si los campos no son válidos.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        """
        Verifica que se pueda editar un cliente correctamente.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="54221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_not_be_able_to_create_a_client_with_number_in_name(self):
        """
        Verifica que no se pueda crear un cliente con numeros en el nombre
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron 7")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre no puede contener números.")).to_be_visible()

    def test_should_not_be_able_to_edit_a_client_with_number_in_name(self):
        """
        Verifica que no se pueda editar un nombre con numeros en un cliente.
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo 9")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre no puede contener números.")).to_be_visible()

    def test_should_be_able_to_show_error_if_invalid_phone(self):
        """
        Prueba que se muestre un mensaje de error si se ingresa un número de teléfono inválido.
        Asegura que el formulario retorna un mensaje de error cuando el número de teléfono
        contiene caracteres no numéricos.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        self.page.get_by_label("Nombre").fill("Benjamin Peres")
        self.page.evaluate("document.querySelector('input[name=phone]').value = '54221asd'")
        self.page.get_by_label("Email").fill("benjaminperes@hotmail.com")
        self.page.get_by_label("Dirección").fill("1 y 60")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()

class MedicineRepoTestCase(PlaywrightTestCase):
    """
    Clase de caso de prueba para probar la funcionalidad del repositorio de medicamentos.

    Esta clase incluye métodos de prueba para:
    - Verificar si se muestra un mensaje si la tabla está vacía.
    - Mostrar datos de medicamentos.
    - Mostrar la acción para agregar un medicamento.
    - Mostrar la acción para editar un medicamento.
    - Mostrar la acción para eliminar un medicamento.
    """
    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla de medicamentos está vacía.
        """
        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        expect(self.page.get_by_text("No existen medicamentos")).to_be_visible()

    def test_should_show_medicines_data(self):
        """
        Verifica que se muestre la tabla de medicina
        """
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
        """
        Verifica que se muestre la opcion de agregar medicina
        """
        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nuevo Medicamento", exact=False,
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("meds_form"))

    def test_should_show_medicine_edit_action(self):
        """
        Verifica que se muestre la accion de editar medicina
        """
        medicine = Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("meds_edit", kwargs={"id": medicine.id}),
        )

    def test_should_show_medicine_delete_action(self):
        """
        Verifica que se la accion de borrar una medicina
        """
        medicine = Med.objects.create(
            name="Paracetamoldog",
            desc="Este medicamento es para vomitos caninos",
            dose=8,
        )

        self.page.goto(f"{self.live_server_url}{reverse('meds_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de medicamentos",
        )
        medicine_id_input = edit_form.locator("input[name=med_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("meds_delete"))
        expect(medicine_id_input).not_to_be_visible()
        expect(medicine_id_input).to_have_value(str(medicine.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """
        Verifica que se muestre la accion de borrar un cliente
        """
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


    def test_should_validate_medicine_dose(self):
        """
        Verifica la validación de la dosis de un medicamento en el formulario.

        Pasos:
        1. Navega al formulario de medicamentos.
        2. Llena el formulario con una dosis inválida (0).
        3. Intenta guardar el formulario.
        4. Verifica que se muestre el mensaje de error correspondiente.

        Resultado esperado:
        - El mensaje "La dosis debe estar entre 1 y 10" es visible.
        """
        self.page.goto(f"{self.live_server_url}{reverse('meds_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        # Probar con una dosis menor a 1
        self.page.get_by_label("Nombre").fill("Paracetamoldog")
        self.page.get_by_label("Descripcion").fill("Este medicamento es para vomitos caninos")
        self.page.get_by_label("Dosis").fill("0")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La dosis debe estar entre 1 y 10")).to_be_visible()


class productCreateEditTestCase(PlaywrightTestCase):
    """
    Clase de caso de prueba para probar la creación y edición de productos.

    Esta clase incluye métodos de prueba para:
    - Crear un nuevo producto.
    - Aumentar el stock de un producto al hacer clic en un botón.
    - Verificar si se muestra un error al intentar editar un producto con un stock negativo.
    """
    def test_should_be_able_to_create_a_new_product(self):
        """
        Verifica que se pueda crear un nuevo producto
        """
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
        """
        Verifica que se pueda aumentar el stock de un producto al hacer clic en un botón.

        Este método realiza una prueba funcional que:
        1. Crea un producto en la base de datos.
        2. Navega a la URL de la página de la lista de productos.
        3. Verifica que los detalles del producto sean visibles en la página.
        4. Hace clic en el botón para aumentar el stock del producto.
        5. Verifica que el stock del producto se haya actualizado correctamente.

        """
        product = Product.objects.create( # noqa: F841
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
        """
        Verifica que se avise del error de cargar un stock negativo
        """
        product = Product.objects.create( # noqa: F841
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
    """
    Clase de caso de prueba para probar la creación y edición de mascotas.

    Esta clase incluye métodos de prueba para:
    - Verificar si se muestra un mensaje si la tabla está vacía.
    - Crear una nueva mascota.
    - Verificar si se muestran errores si el formulario de mascotas es inválido.
    - Editar una mascota existente.
    - Verificar si se muestra un error al intentar editar una mascota con una fecha de nacimiento futura.
    """
    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se avise si las tablas estan vacias
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_be_able_to_create_a_new_pet(self):
        """
        Verifica que se pueda crear una mascota
        """
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
        """
        Verifica que al momento de crear una mascota los datos no sean erroneos, si lo son avisa
        """
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
        """
        Verifica que se permita editar una mascota
        """
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
        """
        Muestra un error en caso de editar con datos erroneos
        """
        pet = Pet.objects.create( # noqa: F841
            name="Paco",
            breed="Perro",
            birthday="2008-05-10",
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

class ProviderCreateEditTestCase(PlaywrightTestCase):
    """
    Clase de caso de prueba para probar la creación y edición de proveedores
    """
    def test_should_be_able_to_create_a_new_provider(self):
        """
        Verifica que la vista pueda crear un nuevo proveedor con sus datos correspondientes de manera satisfactoria.
        """
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Farmacity S.A")
        self.page.get_by_label("Email").fill("moltito@hotmail.com")
        self.page.get_by_label("Direccion").fill("Rio negro 2265")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Farmacity S.A")).to_be_visible()
        expect(self.page.get_by_text("moltito@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("Rio negro 2265")).to_be_visible()


    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que la vista pueda avisar de errores en los datos en caso de ser invalidos
        """
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Farmacity S.A")
        self.page.get_by_label("Email").fill("moltito@hotmail.com")
        self.page.get_by_label("Direccion").fill("Rio negro 2265")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).not_to_be_visible()

    def test_should_view_error_if_address_is_empty(self):
        """
        Verifica que el campo direccion de proveedor sea no nulo.
        """
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Farmacity S.A")
        self.page.get_by_label("Email").fill("moltito@hotmail.com")

        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Farmacity S.A")
        self.page.get_by_label("Email").fill("moltito@hotmail.com")
        self.page.get_by_label("Direccion").fill("Rio negro 2265")

        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).not_to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        """
        Verifica que se puedan actualizar los datos de proveedor.
        """
        provider = Provider.objects.create(
            name="Farmacity S.A",
            email="moltito@hotmail.com",
            address="Rio negro 2265",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Tonci S.A")
        self.page.get_by_label("Email").fill("gepe@hotmail.com")
        self.page.get_by_label("Direccion").fill("Diagonal 80 750")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Farmacity S.A")).not_to_be_visible()
        expect(self.page.get_by_text("moltito@hotmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("Rio negro 2265")).not_to_be_visible()

        expect(self.page.get_by_text("Tonci S.A")).to_be_visible()
        expect(self.page.get_by_text("gepe@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("Diagonal 80 750")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id}),
        )

