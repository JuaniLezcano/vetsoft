from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Client, Product , Med, Provider, Veterinary, Pet
from django.contrib import messages
from datetime import date, datetime

def home(request):
    return render(request, "home.html")


def clients_repository(request):
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    if request.method == "POST":
        client_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))

        return render(
            request, "clients/form.html", {"errors": errors, "client": request.POST},
        )

    client = None
    if id is not None:
        client = get_object_or_404(Client, pk=id)

    return render(request, "clients/form.html", {"client": client})


def clients_delete(request):
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))


def pets_repository(request):
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})


def pets_form(request, id=None):
    breeds = dict(Pet.Breed.choices)

    if request.method == "POST":
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            saved, errors = pet.update_pet(request.POST)

        if saved:
            return redirect(reverse("pets_repo"))  # Redireccionar si se guarda con éxito

        # Pasar los errores y datos del formulario en caso de fallo
        return render(
            request, "pets/form.html", {"errors": errors, "pet": request.POST, "breeds": breeds},
        )

    pet = None
    if id is not None:
        pet = get_object_or_404(Pet, pk=id)

    return render(request, "pets/form.html", {"pet": pet, "breeds": breeds})

def pets_delete(request):
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))


def products_repository(request):
    products = Product.objects.all()
    for product in products:
        if product.stock == 0:
            messages.warning(request, f'El stock del producto "{product.name}" es 0.')
    return render(request, "products/repository.html", {"products": products})


def products_form(request, id=None):
    if request.method == "POST":
        product_id = request.POST.get("id", "")
        errors = {}
        saved = True
        stock = request.POST.get("stock")

        try:
            int(stock)
        except Exception:
            if (product_id == ""):
                saved, errors = Product.save_product(request.POST)
            else:
                errors["stock"] = "El campo de stock no puede estar vacio."
            return render(
            request, "products/form.html", {"errors": errors, "product": request.POST},
            )
        
        if (product_id == "" and int(stock) >= 0):
            stock = int(request.POST.get("stock"))
            saved, errors = Product.save_product(request.POST)
        elif (int(stock) < 0):
            saved = False
            errors["stock"] = "El stock no puede ser negativo."
        else:
            product = get_object_or_404(Product, pk=product_id)
            product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))

        return render(
            request, "products/form.html", {"errors": errors, "product": request.POST},
        )

    product = None
    if id is not None:
        product = get_object_or_404(Product, pk=id)

    return render(request, "products/form.html", {"product": product})


def products_delete(request):
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))

def increment_stock(request, id):
    product = get_object_or_404(Product, pk=id)

    product.stock += 1

    product.save()

    return redirect('products_repo')

def decrement_stock(request, id):
    product = get_object_or_404(Product, pk=id)

    if (product.stock > 0):
        product.stock -= 1
        product.save()
        return redirect('products_repo')
    else:
        return redirect('products_repo')
    

def providers_repository(request):
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):
    if request.method == "POST":
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))

        return render(
            request, "providers/form.html", {"errors": errors, "provider": request.POST},
        )

    provider = None
    if id is not None:
        provider = get_object_or_404(Provider, pk=id)

    return render(request, "providers/form.html", {"provider": provider})


def providers_delete(request):
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))

def veterinary_repository(request):
    veterinarians = Veterinary.objects.all()
    return render(request, "veterinary/repository.html", {"veterinarians": veterinarians})

def veterinary_form(request, id=None):
    if request.method == "POST":
        veterinary_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if veterinary_id == "":
            saved, errors = Veterinary.save_veterinary(request.POST)
        else:
            veterinary = get_object_or_404(Veterinary, pk=veterinary_id)
            veterinary.update_veterinary(request.POST)

        if saved:
            return redirect(reverse("veterinary_repo"))

        return render(
            request, "veterinary/form.html", {"errors": errors, "veterinary": request.POST},
        )

    veterinary = None
    if id is not None:
        veterinary = get_object_or_404(Veterinary, pk=id)

    return render(request, "veterinary/form.html", {"veterinary": veterinary})


def veterinary_delete(request):
    veterinary_id = request.POST.get("veterinary_id")
    veterinary = get_object_or_404(Veterinary, pk=int(veterinary_id))
    veterinary.delete()

    return redirect(reverse("veterinary_repo"))


def meds_repository(request):
    meds = Med.objects.all()
    return render(request, "meds/repository.html", {"meds": meds})

def meds_form(request, id=None):
    if request.method == "POST":
        med_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if med_id == "":
            saved, errors = Med.save_med(request.POST)
        else:
            med = get_object_or_404(Med, pk=med_id)
            saved, errors = med.update_med(request.POST)

        if saved:
            return redirect(reverse("meds_repo"))

        return render(request, "meds/form.html", {"errors": errors, "med": request.POST})

    med = None
    if id is not None:
        med = get_object_or_404(Med, pk=id)
    else:
        med = {"name": "", "desc": "", "dose": ""} 

    return render(request, "meds/form.html", {"med": med})


def meds_delete(request):
    med_id = request.POST.get("med_id")
    med = get_object_or_404(Med, pk=int(med_id))
    med.delete()

    return redirect(reverse("meds_repo"))


