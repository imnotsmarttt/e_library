from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView

from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created

from cart.cart import Cart
from catalog.models import Product


class OrderCreate(CreateView):
    """Оформление заказа"""
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        if cart.coupon:
            order.discount = cart.coupon.discount
            order.coupon = cart.coupon
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     item=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])

            # При желании можно списывать автоматически кол-во продукта со склада
            # product = Product.objects.get(id=item['product'].id)
            # product.count_of_product -= item['quantity']
            # product.save()
        cart.clear()
        # Запуск асинхронной задачи для отправки email пользователю
        order_created.delay(order.id)
        return HttpResponseRedirect(reverse('order_created', kwargs={'pk': order.id}))


class OrderCreated(DetailView):
    """Представление генерирующее детальную информацию после оформления заказа"""
    template_name = 'orders/order_created.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.get_object().id)
        return context
