from django.db import models
from datetime import datetime, date

def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    else:
        try:
            if not phone.startswith("54"):
                errors["phone"] = "El telefono debe comenzar con '54'"
        except ValueError:
            errors["phone"] = "Formato de telefono invalido"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if address == "":
        errors["address"] = "Por favor ingrese una direccion"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors

def validate_product(data):
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
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    else:
        try:
            if not phone.startswith("54"):
                errors["phone"] = "El telefono debe comenzar con '54'"
        except ValueError:
            errors["phone"] = "Formato de telefono invalido"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


def validate_med(data):
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
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
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
        errors = {}
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.address = client_data.get("address", "") or self.address

        phone = client_data.get("phone", "")
        if phone:
            try:
                if not phone.startswith("54"):
                    errors["phone"] = "El telefono debe comenzar con '54'"
                    self.phone = Client.objects.get(pk=self.pk).phone
                    return False, errors
                self.phone = phone
            except ValueError:
                errors["phone"] = "Formato de Telefono invalido"
                self.phone = Client.objects.get(pk=self.pk).phone
                return False, errors

        if not (client_data.get("name") or client_data.get("email") or client_data.get("adress") or client_data.get("phone")):
            return True, None

        self.save()
        return True, None


class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    @classmethod
    def save_product(cls, product_data):
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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
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
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address","") or self.address


        self.save()

class Veterinary(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @classmethod
    def save_veterinary(cls, veterinary_data):
        errors = validate_client(veterinary_data)

        if len(errors.keys()) > 0:
            return False, errors

        Veterinary.objects.create(
            name=veterinary_data.get("name"),
            phone=veterinary_data.get("phone"),
            email=veterinary_data.get("email"),
        )

        return True, None

    def update_veterinary(self, veterinary_data):
        errors = {}
        self.name = veterinary_data.get("name", "") or self.name
        self.email = veterinary_data.get("email", "") or self.email

        phone = veterinary_data.get("phone", "")
        if phone:
            try:
                if not phone.startswith("54"):
                    errors["phone"] = "El telefono debe comenzar con '54'"
                    self.phone = Veterinary.objects.get(pk=self.pk).phone
                    return False, errors
                self.phone = phone
            except ValueError:
                errors["phone"] = "Formato de Telefono invalido"
                self.phone = Veterinary.objects.get(pk=self.pk).phone
                return False, errors

        if not (veterinary_data.get("name") or veterinary_data.get("email") or veterinary_data.get("phone")):
            return True, None

        self.save()
        return True, None

def validate_pet(data):
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
            errors["birthday"] = "Formato de fecha inválido. Use AAAA-MM-DD."

    return errors

class Pet(models.Model):
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
        return self.name

    @classmethod
    def save_pet(cls, pet_data):
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
        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()

class Med(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=50)
    dose = models.FloatField()

    def __str__(self):
            return self.name
    
    @classmethod
    def save_med(cls, med_data):
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

