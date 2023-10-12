from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('<slug:slug>',views.ProductDetail.as_view(),name='product_detail'),
]