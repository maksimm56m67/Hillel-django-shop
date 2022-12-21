from django.urls import path, re_path

from orders import views


urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'), #http://127.0.0.1:8000/order/cart/
    re_path(r'cart/(?P<action>add|remove|clear|pay)/', views.UpdateCartView.as_view(),name='update_cart'), #http://127.0.0.1:8000/order/cart/
    path('recalculate/', views.RecalculateCartView.as_view(), name='recalculate_cart'), #http://127.0.0.1:8000/order/recalculate/
    path('apply-discount/', views.ApplyDiscountView.as_view(),name='apply_discount'), #http://127.0.0.1:8000/order/apply-discount/
]
