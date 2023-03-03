from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, redirect

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