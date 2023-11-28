from django.urls import path
from . import views 

app_name = 'accounts'

urlpatterns = [
    path('signup' , views.signup , name='signup'),
    path('profile/' , views.profile , name='profile'),
    path('profile/edit' , views.edit_profile , name='edit_profile'),
    path('favorite/' , views.user_favourites , name='user_favourites'),
    path('orders/' , views.orders , name='orders'),
    path('order_detail/<int:order_id>/' , views.order_detail , name='order_detail'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
]