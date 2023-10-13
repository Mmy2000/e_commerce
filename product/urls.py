from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('<slug:slug>',views.ProductDetail.as_view(),name='product_detail'),
    path('category/<str:slug>' , views.ProductByCategory.as_view() , name='product_by_category'),
    path('color/<str:slug>' , views.ProductByColor.as_view() , name='product_by_color'),
    path('size/<str:slug>' , views.ProductBysize.as_view() , name='product_by_size'),
]