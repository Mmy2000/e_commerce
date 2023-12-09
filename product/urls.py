from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('orderd_by_rating',views.product_list_orderd_by_rating,name='product_list_orderd_by_rating'),
    path('product_list_orderd_by_created',views.product_list_orderd_by_created , name='product_list_orderd_by_created'),
    path('search/' , views.Search.as_view() , name = 'search'),
    path('<slug:product_slug>/',views.product_detail ,name='product_detail'),
    path('<int:id>/like_or_dislike',views.like_or_unlike , name='like'),
    path('category/<int:id>/' , views.ProductByCategory.as_view() , name='product_by_category'),
    path('tags/<str:slug>/' , views.ProductByTags.as_view() , name='product_by_tags'),
    path('brand/<str:slug>/' , views.ProductByBrand.as_view() , name='product_by_brand'),
    path('submit_review/<int:product_id>/',views.submit_review ,name='submit_review'),
    path('&product_by_price/' , views.product_by_price , name = 'product_by_price'),
    path('&product_by_variation/' , views.product_by_variation , name = 'product_by_variation'),
]