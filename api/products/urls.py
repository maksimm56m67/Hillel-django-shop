from django.urls import path

from api.products.views import ProductsViewList, ProductsViewRetrieve, ProductList

urlpatterns = [
    path('products/', ProductsViewList.as_view()), #http://127.0.0.1:8000/api/v1/products/
    path('products/<uuid:pk>/', ProductsViewRetrieve.as_view()), #http://127.0.0.1:8000/api/v1/products/<uuid:pk>/
    path('products/filter/', ProductList.as_view()) #http://127.0.0.1:8000/api/v1/products/filter/
]