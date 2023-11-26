from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('search/' , views.Search.as_view() , name = 'search'),
    path('<slug:product_slug>/',views.product_detail ,name='product_detail'),
    path('<int:id>/like_or_dislike',views.like_or_unlike , name='like'),
    path('category/<str:slug>/' , views.ProductByCategory.as_view() , name='product_by_category'),
    path('tags/<str:slug>/' , views.ProductByTags.as_view() , name='product_by_tags'),
    path('brand/<str:slug>/' , views.ProductByBrand.as_view() , name='product_by_brand'),
    path('color/<str:slug>/' , views.ProductByColor.as_view() , name='product_by_color'),
    path('size/<str:slug>/' , views.ProductBysize.as_view() , name='product_by_size'),
    path('submit_review/<int:product_id>/',views.submit_review ,name='submit_review'),
]