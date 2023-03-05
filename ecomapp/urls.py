from django.views.generic import TemplateView
from django.urls import path
from .views import (
    HomeView, AboutView, ContactView, ProductDetailView, AddCartView, 
    MyCartView, ManageCartVie,ClearCartView, CheckoutView,
    CustomerRegistrationView, CustomerLoginView, CustomerLogoutView,
    CustomerProfileView,)

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
    path("checkout/", CheckoutView.as_view(), name='checkout' ),
    path("register/",CustomerRegistrationView.as_view(), name="customerregistration"),
    path("login",CustomerLoginView.as_view() , name="customerlogin"),
    path("logout/",CustomerLogoutView.as_view() , name="logout"),
    path("profile/", CustomerProfileView.as_view(), name="profile")
]