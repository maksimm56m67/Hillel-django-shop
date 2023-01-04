from django.urls import path
from items import views


urlpatterns = [
    path('', views.ProductsView.as_view(), name='main'),# http://127.0.0.1:8000/
    path('items/<uuid:pk>/', views.ProductDetailView.as_view(), name='product_detail'), # http://127.0.0.1:8000/items/<uuid:pk>/
    
    path('favorites/', views.favorites, name='favorites'), # http://127.0.0.1:8000/favorites/
    path('favorites/<uuid:pk>/', views.login_required(views.FavoriteProductAddOrRemoveView.as_view()), name='add_or_remove_favorite'), # http://127.0.0.1:8000/favorites/<uuid:pk>/
    path('ajax-favorites/<uuid:pk>/',views.login_required(views.AJAXFavoriteProductAddOrRemoveView.as_view()), name='ajax_add_or_remove_favorite'),# http://127.0.0.1:8000/ajax-favorites/<uuid:pk>/
    
    path('about/', views.AboutView.as_view(), name='about'), # http://127.0.0.1:8000/about/
    path('csv/', views.export_csv, name='export_csv'),  # http://127.0.0.1:8000/csv/
    path('import/csv/', views.ImportCSV.as_view(), name='import_csv'), # http://127.0.0.1:8000/import/csv/
]