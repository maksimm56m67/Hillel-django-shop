import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from orders.model_forms import OrderModelForm
from orders.models import Order
from django.views.generic import ListView, DetailView
from items.forms import ImportCSVForm, ContactForm, ProductFilterForm
from items.model_forms import ItemModelForm
from django.db.models import OuterRef, Exists
from items.models import Item, FavoriteProduct
from django.views.generic import TemplateView

from django.core.paginator import Paginator
from django.contrib import messages
from items.tasks import send_contact_form
from items.filters import ProductFilter
from django_filters.views import FilterView


def products(request, *args, **kwargs):
    page_number = request.GET.get('page')
    paginator = Paginator(Item.objects.all(), 10)
    pages = paginator.get_page(page_number)
    context = {
        'object_list': pages
    }
    return render(request, context=context, template_name='items/mane.html')

# class ProductsView(FilterView):
#     template_name = 'items/mane.html'
#     model = Item
#     paginate_by = 5
#     filter_form = ProductFilterForm
#     filterset_class = ProductFilter
#     template_name_suffix = 'mane'    


    
#     def filtered_queryset(self, queryset):
#         category_id = self.request.GET.get('category')
#         currency = self.request.GET.get('currency')
#         name = self.request.GET.get('name')
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         if currency:
#             queryset = queryset.filter(currency=currency)
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         return queryset
    
#     def get_queryset(self):
#         qs = self.model.get_products()
#         qs = self.filtered_queryset(qs)
#         if self.request.user.is_authenticated:
#             sq = FavoriteProduct.objects.filter(
#                 product=OuterRef('id'),
#                 user=self.request.user
#             )
#             qs = qs \
#                 .prefetch_related('in_favorites') \
#                 .annotate(is_favorite=Exists(sq))
#         return qs


#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=None, **kwargs)
#         context.update(
#             {'filter_form': self.filter_form}
#         )
#         return context
class ProductsView(FilterView):
    template_name = 'items/mane.html'
    model = Item
    paginate_by = 5
    filterset_class = ProductFilter
    template_name_suffix = 'mane'

    def get_queryset(self):
        qs = self.model.get_products()
        if self.request.user.is_authenticated:
            sq = FavoriteProduct.objects.filter(
                product=OuterRef('id'),
                user=self.request.user
            )
            qs = qs \
                .prefetch_related('in_favorites') \
                .annotate(is_favorite=Exists(sq))
        return qs   

class ProductDetailView(DetailView):
    template_name = 'items/mane.html'
    model = Item
    


class AboutView(FormView):
    template_name = 'about/about.html'
    form_class = ContactForm
    success_url = reverse_lazy('about')
    
    
    @method_decorator(login_required)

    def form_valid(self, form):
        send_contact_form.delay(form.cleaned_data['email'],
                                form.cleaned_data['text'])
        messages.success(self.request, 'Email has been send.')
        return super().form_valid(form) 
    



    
@login_required
def items(request):
           
    context = {
        'Items': Item.objects.all(),
    }
    return render(request, 'items/mane.html', context)



@login_required
def export_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="products.csv"'},
    )
    fieldnames = ['name', 'description','image', 'price', 'category']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for item in Item.objects.iterator():
        writer.writerow(
            {
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'category': item.category,
                'image': item.image.url,
            }
        )
    return response

class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'files/import_csv.html'
    success_url = reverse_lazy('main')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    


@login_required
def favorites(request):
           
    context = {
        'Favorites': FavoriteProduct.objects.filter(user=request.user).all(),
    }

    return render(request, 'items/favoriteproduct_list.html', context)


class FavoriteProductAddOrRemoveView(DetailView):
    model = Item

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        favorite, created = FavoriteProduct.objects.get_or_create(
            items=product,
            user=user
        )
        if not created:
            favorite.delete()
        return HttpResponseRedirect(reverse_lazy('main'))
    