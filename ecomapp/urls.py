from django.urls import path
from .views import (
    HomeView, AboutView, ContactView, ProductDetailView, AddCartView, MyCartView, ManageCartVie, ClearCartView)

app_name = 'ecomapp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about-page"),
    path("contact/", ContactView.as_view(), name="contact-page"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("addcart/<int:prod_id>/",AddCartView.as_view(), name="add-cart"),
    path("mycart/",MyCartView.as_view(), name="my-cart"),
    path('manage-cart/<int:cp_id>/', ManageCartVie.as_view(), name="manage-cart"),
    path("empty-cart/", ClearCartView.as_view(), name='empty-cart' ),
    
]