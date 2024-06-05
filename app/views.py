
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Client, Med, Pet, Product, Provider, Veterinary


def home(request):
    """
    Renderiza la página principal.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Un objeto HttpResponse que renderiza la plantilla 'home.html'.
    """
    return render(request, "home.html")


def clients_repository(request):
    """
    Renderiza la página de repositorio de clientes.

    Muestra una lista de todos los clientes almacenados en la base de datos.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Un objeto HttpResponse que renderiza la plantilla 'clients/repository.html'
        con la lista de clientes pasada como contexto.
    """
    clients = Client.objects.all()
    return render(request, "clients/repository.html", {"clients": clients})


def clients_form(request, id=None):
    """
    Renderiza el formulario de clientes.

    Si la solicitud es de tipo POST, procesa los datos del formulario y guarda o actualiza el cliente en la base de datos.
    Si la solicitud es de tipo GET, muestra el formulario con los datos del cliente si se proporciona un ID válido.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int, opcional): El ID del cliente a editar. Por defecto es None.

    Returns:
        HttpResponse: Un objeto HttpResponse que renderiza el formulario de clientes ('clients/form.html').
        Si la solicitud es de tipo POST y los datos se guardan correctamente, redirige al repositorio de clientes.
        Si se proporciona un ID válido y se encuentra el cliente correspondiente, muestra el formulario con los datos del cliente.
    """
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
    """
    Elimina un cliente de la base de datos.

    Recibe el ID del cliente a eliminar a través de una solicitud POST.
    Busca el cliente correspondiente en la base de datos y lo elimina.
    Luego, redirige al repositorio de clientes.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponseRedirect: Una respuesta de redirección que dirige al usuario al repositorio de clientes.
    """
    client_id = request.POST.get("client_id")
    client = get_object_or_404(Client, pk=int(client_id))
    client.delete()

    return redirect(reverse("clients_repo"))


def pets_repository(request):
    """
    Renderiza la página de repositorio de mascotas.

    Obtiene todas las mascotas de la base de datos y las pasa al template 'repository.html' para su visualización.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el template 'repository.html' con la lista de mascotas.
    """
    pets = Pet.objects.all()
    return render(request, "pets/repository.html", {"pets": pets})


def pets_form(request, id=None):
    """
    Renderiza el formulario de mascotas y maneja la lógica para crear o actualizar una mascota.

    Si la solicitud es un POST, valida los datos recibidos y guarda la mascota en la base de datos si es válida.
    Si la solicitud es GET, muestra el formulario con los datos de la mascota si se proporciona un ID válido.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int, opcional): El ID de la mascota a actualizar. Por defecto es None.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el template 'form.html' con el formulario de mascotas.
    """
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
    """
    Elimina una mascota de la base de datos.

    Se espera que la solicitud POST contenga el ID de la mascota a eliminar.
    La función obtiene el objeto de mascota correspondiente utilizando el ID proporcionado,
    y luego lo elimina de la base de datos.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponseRedirect: Redirecciona al repositorio de mascotas después de eliminar la mascota.
    """
    pet_id = request.POST.get("pet_id")
    pet = get_object_or_404(Pet, pk=int(pet_id))
    pet.delete()

    return redirect(reverse("pets_repo"))


def products_repository(request):
    """
    Renderiza la página del repositorio de productos.

    Obtiene todos los productos de la base de datos y los pasa al template para su renderizado.
    Además, verifica si algún producto tiene un stock de 0 y muestra un mensaje de advertencia si es así.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página del repositorio de productos.
    """
    products = Product.objects.all()
    for product in products:
        if product.stock == 0:
            messages.warning(request, f'El stock del producto "{product.name}" es 0.')
    return render(request, "products/repository.html", {"products": products})


def products_form(request, id=None):
    """
    Renderiza el formulario de productos y procesa los datos enviados por el usuario.

    Si la solicitud es de tipo POST, valida y procesa los datos enviados por el usuario.
    Si la solicitud es de tipo GET, simplemente renderiza el formulario con los datos del producto si se proporciona un ID válido.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int, opcional): El ID del producto. Por defecto es None.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el formulario de productos.
    """
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
    """
    Elimina un producto específico de la base de datos.

    Extrae el ID del producto de la solicitud POST, busca el producto correspondiente en la base de datos y lo elimina.
    Luego redirige al usuario a la página de repositorio de productos.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP de redirección a la página de repositorio de productos.
    """
    product_id = request.POST.get("product_id")
    product = get_object_or_404(Product, pk=int(product_id))
    product.delete()

    return redirect(reverse("products_repo"))

def increment_stock(request, id):
    """
    Incrementa el stock de un producto en 1 unidad.

    Busca un producto específico en la base de datos utilizando su ID. Luego incrementa el stock del producto en 1 unidad
    y guarda los cambios en la base de datos. Finalmente, redirige al usuario a la página de repositorio de productos.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int): El ID del producto que se va a incrementar el stock.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP de redirección a la página de repositorio de productos.
    """
    product = get_object_or_404(Product, pk=id)

    product.stock += 1

    product.save()

    return redirect('products_repo')

def decrement_stock(request, id):
    """
    Decrementa el stock de un producto en 1 unidad, si el stock es mayor que cero.

    Busca un producto específico en la base de datos utilizando su ID. Si el stock del producto es mayor que cero, se
    decrementa en 1 unidad y se guardan los cambios en la base de datos. Luego, redirige al usuario a la página de
    repositorio de productos. Si el stock es cero o menor, la función simplemente redirige al usuario a la página de
    repositorio de productos sin hacer cambios.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int): El ID del producto al que se le va a decrementar el stock.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP de redirección a la página de repositorio de productos.
    """
    product = get_object_or_404(Product, pk=id)

    if (product.stock > 0):
        product.stock -= 1
        product.save()
        return redirect('products_repo')
    else:
        return redirect('products_repo')


def providers_repository(request):
    """
    Renderiza la página de repositorio de proveedores.

    Recupera todos los proveedores de la base de datos y los pasa al template "providers/repository.html" para
    renderizar la página de repositorio de proveedores.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página de repositorio de proveedores.
    """
    providers = Provider.objects.all()
    return render(request, "providers/repository.html", {"providers": providers})


def providers_form(request, id=None):
    """
    Renderiza el formulario de proveedores.

    Si la solicitud es de tipo POST, valida los datos recibidos y guarda o actualiza el proveedor en la base de datos.
    Si la solicitud es de tipo GET, renderiza el formulario de proveedores vacío o con los datos de un proveedor
    existente para su edición.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int, opcional): El ID del proveedor a ser editado. Por defecto es None, lo que indica que se está
            creando un nuevo proveedor.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el formulario de proveedores, ya sea vacío o con datos de
        un proveedor existente.
    """
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
    """
    Elimina un proveedor de la base de datos.

    Recibe una solicitud HTTP POST que contiene el ID del proveedor a eliminar. Busca el proveedor en la base de datos
    por su ID, y si existe, lo elimina. Luego redirige a la página de visualización de proveedores.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud POST.

    Returns:
        HttpResponseRedirect: Una redirección a la página de visualización de proveedores.
    """
    provider_id = request.POST.get("provider_id")
    provider = get_object_or_404(Provider, pk=int(provider_id))
    provider.delete()

    return redirect(reverse("providers_repo"))

def veterinary_repository(request):
    """
    Renderiza la página que muestra todos los veterinarios almacenados en la base de datos.

    Recibe una solicitud HTTP GET y recupera todos los objetos de tipo `Veterinary` de la base de datos.
    Luego renderiza la plantilla 'veterinary/repository.html', pasando la lista de veterinarios como contexto.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud GET.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'veterinary/repository.html' con la lista
        de veterinarios como contexto.
    """
    veterinarians = Veterinary.objects.all()
    return render(request, "veterinary/repository.html", {"veterinarians": veterinarians})

def veterinary_form(request, id=None):
    """
    Renderiza el formulario para agregar o editar un veterinario.

    Si la solicitud HTTP es de tipo POST, se intenta guardar o actualizar la información del veterinario
    según los datos proporcionados en la solicitud. Si el formulario se completa correctamente, se redirige
    a la página del repositorio de veterinarios. Si hay errores en el formulario, se muestra nuevamente el
    formulario con los errores.

    Si la solicitud HTTP es de tipo GET, se renderiza el formulario vacío si no se proporciona un ID,
    o se renderiza el formulario con los datos del veterinario correspondiente al ID proporcionado.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

        id (int, opcional): El ID del veterinario a editar. Por defecto es None.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el formulario de veterinario, ya sea vacío o con los
        datos del veterinario existente, y los errores si corresponde.
    """
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
    """
    Elimina un veterinario de la base de datos.

    Recibe una solicitud HTTP de tipo POST que contiene el ID del veterinario a eliminar.
    Busca el veterinario correspondiente en la base de datos utilizando el ID proporcionado.
    Si se encuentra el veterinario, se elimina de la base de datos. Si no se encuentra, devuelve un error 404.
    Luego, redirige al usuario a la página del repositorio de veterinarios.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP de redirección que lleva al usuario a la página del
        repositorio de veterinarios después de eliminar el veterinario.
    """
    veterinary_id = request.POST.get("veterinary_id")
    veterinary = get_object_or_404(Veterinary, pk=int(veterinary_id))
    veterinary.delete()

    return redirect(reverse("veterinary_repo"))


def meds_repository(request):
    """
    Renderiza la página de repositorio de medicamentos.

    Recupera todos los medicamentos de la base de datos y los pasa al template "meds/repository.html"
    para su renderizado.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página de repositorio de medicamentos
        con la lista de medicamentos recuperada de la base de datos.
    """
    meds = Med.objects.all()
    return render(request, "meds/repository.html", {"meds": meds})

def meds_form(request, id=None):
    """
    Renderiza el formulario de medicamentos y maneja la lógica para agregar o editar medicamentos.

    Si la solicitud es POST, procesa los datos enviados. Si el ID del medicamento está presente en la solicitud,
    se intenta actualizar el medicamento correspondiente; de lo contrario, se intenta guardar un nuevo medicamento.
    Si la operación es exitosa, redirige al usuario al repositorio de medicamentos; de lo contrario, vuelve a renderizar
    el formulario con los errores.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.
        id (int, opcional): El ID del medicamento a editar.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza el formulario de medicamentos, ya sea en blanco o
        prellenado con los datos del medicamento a editar.
    """
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
    """
    Elimina un medicamento específico de la base de datos.

    Extrae el ID del medicamento de la solicitud POST y busca el medicamento correspondiente en la base de datos.
    Si el medicamento existe, lo elimina de la base de datos y redirige al usuario al repositorio de medicamentos.

    Args:
        request (HttpRequest): El objeto HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponseRedirect: Una redirección HTTP a la página de repositorio de medicamentos después de eliminar el medicamento.
    """
    med_id = request.POST.get("med_id")
    med = get_object_or_404(Med, pk=int(med_id))
    med.delete()

    return redirect(reverse("meds_repo"))
