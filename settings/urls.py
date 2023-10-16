from django.urls import path
from . views import home , CategoryList ,news_letters_subscribe

app_name = 'settings'

urlpatterns = [
    path('', home ,name = 'home'),
    path('category', CategoryList.as_view() ,name = 'category_list'),
    path('newsletter/' , news_letters_subscribe , name = 'newsletter'),
]