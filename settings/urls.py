from django.urls import path
from . views import home , CategoryList ,news_letters_subscribe , BrandList , contact
from . footer import home_search

app_name = 'settings'

urlpatterns = [
    path('', home ,name = 'home'),
    path('search' , home_search , name = 'home_search'),
    path('category', CategoryList.as_view() ,name = 'category_list'),
    path('brand', BrandList.as_view() ,name = 'brand_list'),
    path( 'contact',contact , name='contact' ),
    path('newsletter/' , news_letters_subscribe , name = 'newsletter'),
]