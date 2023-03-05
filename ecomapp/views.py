from django.views import View
from django.views.generic import FormView, TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import CheckoutForm, CustomerRegistrationForm
from .models import Product, Cart, CartProduct

class HomeView(ListView):
    model = Product
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


#Add cart view
class AddCartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_obj = get_object_or_404(Product, pk=kwargs['prod_id'])
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = get_object_or_404(Cart, pk=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cp_obj = this_product_in_cart.last()
                
                cp_obj.quantity += 1
                cp_obj.subtotal += product_obj.selling_price
                cp_obj.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            else:
                cp_obj = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
                )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cp_obj = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
                )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
        return context


class MyCartView(TemplateView):
    template_name = 'my_cart.html'

    def get_context_data(self, **kwargs): 
        context =  super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = get_object_or_404(Cart, id=cart_id)
            # context['products'] = cart_obj.cartproduct_set.all()
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context
    


class ManageCartVie(View):
    def get(self, request, *args, **kwargs):
        cp_id = kwargs['cp_id']
        action = request.GET.get('action')
        cp = CartProduct.objects.get(id=cp_id)
        cart_obj = cp.cart

        if action == 'add':
            cp.quantity += 1
            cp.subtotal += cp.rate
            cp.save()
            cart_obj.total += cp.rate
            cart_obj.save()

        elif action == 'dec':
            cp.quantity -= 1
            cp.subtotal -= cp.rate
            cp.save()
            cart_obj.total -= cp.rate
            cart_obj.save()
            if cp.quantity == 0:
                cp.delete()

        elif action == 'remove':
            cart_obj.total -= cp.subtotal
            cart_obj.save()
            cp.delete()
        else:
            pass
        return redirect("ecomapp:my-cart")



class ClearCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:my-cart")
    
class CheckoutView(CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('ecomapp:home')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        cart_id =self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context
        
    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj 
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("ecomapp:home")
        
        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = "c_registration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = get_user_model().objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class CustomerLoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            print(form.cleaned_data,'***************************')
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect("ecomapp:home")
        return render(request, 'login.html', {'form':form})

# Alternate way of logging in
# class CustomerLoginView(FormView):
#     template_name = 'login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy("ecomapp:home")

#     def form_valid(self, form):
#         user = authenticate(self.request, **form.cleaned_data)
#         if user is not None and user.customer:
#             login(self.request, user)
#         return super().form_valid(form)

class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")