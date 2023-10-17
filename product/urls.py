from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('<slug:slug>',views.ProductDetail.as_view(),name='product_detail'),
    path('category/<str:slug>' , views.ProductByCategory.as_view() , name='product_by_category'),
    path('brand/<str:slug>' , views.ProductByBrand.as_view() , name='product_by_brand'),
    path('color/<str:slug>' , views.ProductByColor.as_view() , name='product_by_color'),
    path('size/<str:slug>' , views.ProductBysize.as_view() , name='product_by_size'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase-cart-item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease-cart-item'),
    path('fetch-cart-count/', views.fetch_cart_count, name='fetch-cart-count'),
    path('create-order/', views.create_order, name='create-order'),
    path('handle-payment/', views.handle_payment, name='handle-payment'),
    path('cart/checkout/', views.checkout, name='checkout'),

]