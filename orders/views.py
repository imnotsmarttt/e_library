from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView

from .forms import OrderCreateForm
from .models import OrderItem, Order

from cart.cart import Cart


class OrderCreate(CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     item=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return HttpResponseRedirect(reverse('order_created', kwargs={'pk': order.id}))


class OrderCreated(DetailView):
    template_name = 'orders/order_created.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.get_object().id)
        return context