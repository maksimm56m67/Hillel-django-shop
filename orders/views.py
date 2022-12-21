from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, TemplateView

from orders.forms import UpdateCartOrderForm, RecalculateCartForm, ApplyDiscountForm
from orders.mixins import GetCurrentOrderMixin


class CartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'order/order.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'order': self.get_object(),
             'products_relation': self.get_queryset()}
        )
        return context

    def get_queryset(self):
        return self.get_object().get_products_through()


class UpdateCartView(GetCurrentOrderMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateCartOrderForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'cart' if kwargs['action'] == 'remove' else 'main')


class RecalculateCartView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('cart')

    def post(self, request, *args, **kwargs):
        form = RecalculateCartForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class ApplyDiscountView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('cart')

    def post(self, request, *args, **kwargs):
        form = ApplyDiscountForm(request.POST, order=self.get_object())
        if form.is_valid():
            form.apply()
        return self.get(request, *args, **kwargs)
    

        