import re
from datetime import date, datetime

from django.db import models


def validate_client(data):
    """
    Valida los datos del cliente.

    Este método verifica que los campos 'name', 'phone' y 'email' estén presentes
    y no vacíos en el diccionario 'data'. También valida que el campo 'email' contenga
    al menos un carácter '@'.

    Parámetros:
        data (dict): Un diccionario que contiene los datos del cliente con posibles
        claves 'name', 'phone' y 'email'.

    Devuelve:
        dict: Un diccionario que contiene los errores de validación. Si no hay errores,
        el diccionario estará vacío. Las posibles claves del diccionario son:
            - 'name': Si el nombre está vacío.
            - 'phone': Si el teléfono está vacío.
            - 'email': Si el email está vacío o no es válido.
    """

    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    pattern_email = r'^[a-zA-Z0-9._%+-]+@vetsoft\.com$'

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if any(char.isdigit() for char in name):
        errors["name"] = "El nombre no puede contener números."

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.isdigit():
        errors["phone"] = "Por favor ingrese un numero de telefono valido, solo digitos"
    if email == "":
        errors["email"] = "Por favor ingrese un email"
    else:
        try:
            if not re.match(pattern_email, email):
                 errors["email"] =("El email debe terminar con @vetsoft.com y contener algo antes")
        except ValueError:
            errors["email"] = "Formato de email inválido."
    return errors

def validate_provider(data):
    """
    Valida los datos proporcionados para un proveedor.

    Args:
        data (dict): Un diccionario que contiene los datos del proveedor a validar.
                     Debe contener las claves "name", "email" y "address".

    Returns:
        dict: Un diccionario que contiene los errores de validación.
              Las claves son los nombres de los campos y los valores son los mensajes de error.
    """
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if address == "":
        errors["address"] = "Por favor ingrese una direccion"

    if email == "":
        errors["email"] = "Por favor ingrese un email valido"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_product(data):
    """
    Valida los datos proporcionados para un producto.

    Args:
        data (dict): Un diccionario que contiene los datos del producto a validar.
                     Debe contener las claves "name", "type", "price" y "stock".

    Returns:
        dict: Un diccionario que contiene los errores de validación.
              Las claves son los nombres de los campos y los valores son los mensajes de error.
    """
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")
    stock = data.get("stock", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if price == "":
        errors["price"] = "Por favor ingrese un precio"

    if stock == "":
        errors["stock"] = "Por favor ingrese un stock"
    return errors

def validate_veterinary(data):
    """
    Valida los datos proporcionados para una veterinaria.

    Args:
        data (dict): Un diccionario que contiene los datos de la veterinaria a validar.
                     Debe contener las claves "name", "phone" y "email".

    Returns:
        dict: Un diccionario que contiene los errores de validación.
              Las claves son los nombres de los campos y los valores son los mensajes de error.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


def validate_med(data):
    """
    Valida los datos proporcionados para un medicamento.

    Args:
        data (dict): Un diccionario que contiene los datos del medicamento a validar.
                     Debe contener las claves "name", "desc" y "dose".

    Returns:
        dict: Un diccionario que contiene los errores de validación.
              Las claves son los nombres de los campos y los valores son los mensajes de error.
    """
    errors = {}

    name = data.get("name", "")
    desc = data.get("desc", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if desc == "":
        errors["desc"] = "Por favor ingrese una descripcion"

    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"

    else:
        try:
            dose = float(dose)
            if dose < 1.0 or dose > 10.0:
                errors["dose"] = "La dosis debe estar entre 1 y 10"
        except ValueError:
            errors["dose"] = "La dosis debe ser un número decimal"

    return errors

class Client(models.Model):
    """
    Modelo que representa a un cliente.

    Este modelo contiene la información básica de un cliente, como su nombre, teléfono, correo electrónico
    y dirección. También proporciona métodos para guardar y actualizar la información del cliente.

    Atributos:
        name (str): Nombre del cliente.
        phone (str): Número de teléfono del cliente.
        email (str): Dirección de correo electrónico del cliente.
        address (str, opcional): Dirección del cliente (opcional).

    Métodos:
        __str__: Método para representar el objeto cliente como una cadena.
        save_client: Método de clase para guardar un nuevo cliente en la base de datos.
        update_client: Método para actualizar la información de un cliente existente en la base de datos.
    """

    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Guarda un nuevo cliente en la base de datos después de validar los datos proporcionados.

        Parámetros:
        client_data (dict): Un diccionario que contiene los datos del cliente. Claves esperadas:
            - "name" (str): El nombre del cliente.
            - "phone" (str): El número de teléfono del cliente.
            - "email" (str): La dirección de correo electrónico del cliente.
            - "address" (str): La dirección del cliente.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        """
        Metodo para actualizar los clientes con nuevos datos
        """
        pattern_email = r'^[a-zA-Z0-9._%+-]+@vetsoft\.com$'
        errors = {}
        self.name = client_data.get("name", "") or self.name
        if (client_data.get("phone", "").isdigit()):
            self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address
        email = client_data.get("email", "")
        if email:
            try:
                if not re.match(pattern_email, email):
                    errors["email"] = "El email debe terminar con @vetsoft.com y contener algo antes"
                    self.email = Client.objects.get(pk=self.pk).email
                    return False, errors
                self.email= email
            except ValueError:
                errors["email"] = "Formato de email inválido.o"
                self.email = Client.objects.get(pk=self.pk).email
                return False, errors
        self.save()


class Product(models.Model):
    """
    Modelo que representa un producto en el inventario.

    Este modelo contiene la información de un producto, incluyendo su nombre, tipo,
    precio y stock disponible.

    Atributos:
        name (str): Nombre del producto.
        type (str): Tipo o categoría del producto.
        price (float): Precio del producto.
        stock (int): Cantidad de stock disponible del producto.

    Métodos:
        __str__: Método para representar el objeto producto como una cadena.
        save_product: Método de clase para guardar un nuevo producto en la base de datos.
        update_product: Método para actualizar la información de un producto existente en la base de datos.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        """
            Retorna la representación en string del objeto.
        """
        return self.name

    @classmethod
    def save_product(cls, product_data):
        """
        Guarda un producto
        """
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
            stock=product_data.get("stock"),
        )

        return True, None

    def update_product(self, product_data):
        """
            Actualiza los datos de un producto
        """
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price
        self.stock = product_data.get("stock", "") or self.stock

        try:
            if (int(self.stock) < 0):
                raise ValueError("El stock no puede ser negativo.")
        except ValueError:
            self.stock = Product.objects.get(pk=self.pk).stock

        self.save()



class Provider(models.Model):
    """
    Modelo que representa un proveedor de productos.

    Este modelo contiene la información de un proveedor, incluyendo su nombre,
    dirección de correo electrónico y dirección física.

    Atributos:
        name (str): Nombre del proveedor.
        email (str): Dirección de correo electrónico del proveedor.
        address (str, opcional): Dirección física del proveedor (opcional).

    Métodos:
        __str__: Método para representar el objeto proveedor como una cadena.
        save_provider: Método de clase para guardar un nuevo proveedor en la base de datos.
        update_provider: Método para actualizar la información de un proveedor existente en la base de datos.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """
            Retorna la representación en string del objeto.
        """
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """
            Guarda la informacio del proveedor
        """
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            address=provider_data.get("address"),
        )

        return True, None

    def update_provider(self, provider_data):
        """
    Actualiza los datos del proveedor con los datos proporcionados.

    Parámetros:
    provider_data (dict): Un diccionario que contiene los datos del proveedor. Claves opcionales:
        - "name" (str): El nuevo nombre del proveedor.
        - "email" (str): La nueva dirección de correo electrónico del proveedor.
        - "address" (str): La nueva dirección del proveedor.

    Retorna:
    None
    """
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address","") or self.address


        self.save()

class Veterinary(models.Model):
    """
    Modelo que representa una veterinario.

    Este modelo contiene la información de una veterinario, incluyendo su nombre,
    número de teléfono y dirección de correo electrónico.

    Atributos:
        name (str): Nombre del veterinario.
        phone (str): Número de teléfono del veterinario.
        email (str): Dirección de correo electrónico del veterinario.

    Métodos:
        __str__: Método para representar el objeto veterinario como una cadena.
        save_veterinary: Método de clase para guardar un nuevo veterinario en la base de datos.
        update_veterinary: Método para actualizar la información de un veterinario existente en la base de datos.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @classmethod
    def save_veterinary(cls, veterinary_data):
        """
        Guarda un veterinario
        """
        errors = validate_veterinary(veterinary_data)

        if len(errors.keys()) > 0:
            return False, errors

        Veterinary.objects.create(
            name=veterinary_data.get("name"),
            phone=veterinary_data.get("phone"),
            email=veterinary_data.get("email"),
        )

        return True, None

    def update_veterinary(self, veterinary_data):
        """
        Actualiza los datos del veterinario
        """
        self.name = veterinary_data.get("name", "") or self.name
        self.email = veterinary_data.get("email", "") or self.email
        self.phone = veterinary_data.get("phone", "") or self.phone

        self.save()

def validate_pet(data):
    """
    Valida los datos proporcionados para una mascota.

    Args:
        data (dict): Un diccionario que contiene los datos de la mascota a validar.
                     Debe contener las claves "name", "breed" y "birthday".

    Returns:
        dict: Un diccionario que contiene los errores de validación.
              Las claves son los nombres de los campos y los valores son los mensajes de error.
    """
    errors = {}

    name = data.get("name", "")
    breed = data.get("breed", "")
    birthday = data.get("birthday", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"

    if birthday == "":
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento"
    else:
        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
            if birthday_date > date.today():
                errors["birthday"] = "La fecha de nacimiento no puede ser posterior al día actual."
        except ValueError:
            errors["birthday"] = "Formato de fecha invalido. Utilice el formato YYYY-MM-DD"

    return errors

class Pet(models.Model):
    """
    Modelo que representa una mascota.

    Este modelo contiene la información de una mascota, incluyendo su nombre, raza y fecha de nacimiento.

    Atributos:
        name (str): Nombre de la mascota.
        breed (str): Raza de la mascota.
        birthday (date): Fecha de nacimiento de la mascota.

    Métodos:
        __str__: Método para representar el objeto mascota como una cadena.
        save_pet: Método de clase para guardar una nueva mascota en la base de datos.
        update_pet: Método para actualizar la información de una mascota existente en la base de datos.
    """
    class Breed(models.TextChoices):
        Perro = "Perro"
        Gato = "Gato"
        Conejo = "Conejo"
        Pájaro = "Pájaro"
        Pez = "Pez"
        Otro = "Otro"

    name = models.CharField(max_length=100)
    breed = models.CharField(choices=Breed.choices, max_length=50)
    birthday = models.DateField()

    def __str__(self):
        """
            Retorna la representación en string del objeto.
        """
        return self.name

    @classmethod
    def save_pet(cls, pet_data):
        """
        Guarda una mascota
        """
        errors = validate_pet(pet_data)

        if errors:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )

        return True, None

    def update_pet(self, pet_data):
        """
        Actualiza los datos de la mascota
        """
        errors = {}
        self.name = pet_data.get("name", self.name)
        self.breed = pet_data.get("breed", self.breed)

        birthday_str = pet_data.get("birthday", None)

        if birthday_str:
            try:
                birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d").date()
                if birthday_date > date.today():
                    errors["birthday"] = "La fecha de nacimiento no puede ser posterior al día actual."
                    self.birthday = Pet.objects.get(pk=self.pk).birthday
                    return False, errors
                self.birthday = birthday_date
            except ValueError:
                errors["birthday"] = "Formato de fecha inválido. Utilice AAAA-MM-DD."
                self.birthday = Pet.objects.get(pk=self.pk).birthday
                return False, errors

        # No se realizan cambios en la mascota si no hay datos válidos proporcionados
        if not (pet_data.get("name") or pet_data.get("breed") or pet_data.get("birthday")):
            return True, None

        self.save()
        return True, None

class Med(models.Model):
    """
     Modelo que representa un medicamento.

    Este modelo contiene la información de un medicamento, incluyendo su nombre, descripción y dosis.

    Atributos:
        name (str): Nombre del medicamento.
        desc (str): Descripción del medicamento.
        dose (float): Dosis del medicamento.

    Métodos:
        __str__: Método para representar el objeto medicamento como una cadena.
        save_med: Método de clase para guardar un nuevo medicamento en la base de datos.
        update_med: Método para actualizar la información de un medicamento existente en la base de datos.
        """
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=50)
    dose = models.FloatField()

    def __str__(self):
            return self.name

    @classmethod
    def save_med(cls, med_data):
        """
        Guarda una medicina
        """
        errors = validate_med(med_data)

        if len(errors.keys()) > 0:
            return False, errors

        Med.objects.create(
            name=med_data.get("name"),
            desc=med_data.get("desc"),
            dose=med_data.get("dose"),
        )
        return True, None

    def update_med(self, med_data):
        """
        Actualizar medicina
        """
        errors = validate_med(med_data)

        if len(errors.keys()) > 0:
            return False, errors

        errors = validate_med(med_data)

        if len(errors.keys()) > 0:
            return False, errors
        else:
            self.name = med_data.get("name", "") or self.name
            self.desc = med_data.get("desc", "") or self.desc
            self.dose = med_data.get("dose", "") or self.dose

        self.save()
        return True, None

