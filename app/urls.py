from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),

    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    path("productos/", view=views.products_repository, name="products_repo"),
    path("productos/nuevo/", view=views.products_form, name="products_form"),
    path("productos/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("productos/eliminar/", view=views.products_delete, name="products_delete"),
    path("productos/incrementar/<int:id>/", view=views.increment_stock, name="increment_stock"),
    path("productos/decrementar/<int:id>/", view=views.decrement_stock, name="decrement_stock"),
    path("proveedores/", view=views.providers_repository, name="providers_repo"),
    path("proveedores/nuevo/", view=views.providers_form, name="providers_form"),
    path("proveedores/editar/<int:id>/", view=views.providers_form, name="providers_edit"),
    path("proveedores/eliminar/", view=views.providers_delete, name="providers_delete"),
    path("veterinarios/", view=views.veterinary_repository, name="veterinary_repo"),
    path("veterinarios/nuevo/", view=views.veterinary_form, name="veterinary_form"),
    path("veterinarios/editar/<int:id>/", view=views.veterinary_form, name="veterinary_edit"),
    path("veterinarios/eliminar/", view=views.veterinary_delete, name="veterinary_delete"),
    path("mascotas/", view=views.pets_repository, name="pets_repo"),
    path("mascotas/nuevo/", view=views.pets_form, name="pets_form"),
    path("mascotas/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("mascotas/eliminar/", view=views.pets_delete, name="pets_delete"),
    path("medicinas/", view=views.meds_repository, name="meds_repo"),
    path("medicinas/nuevo/", view=views.meds_form, name="meds_form"),
    path("medicinas/editar/<int:id>/", view=views.meds_form, name="meds_edit"),
    path("medicinas/eliminar/", view=views.meds_delete, name="meds_delete"),
]
