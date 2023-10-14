from django.urls import path
from . views import home , CategoryList 
from . footer import home_search

app_name = 'settings'

urlpatterns = [
    path('', home ,name = 'home'),
    path('category', CategoryList.as_view() ,name = 'category_list'),
]