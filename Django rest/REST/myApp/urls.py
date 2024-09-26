from django.urls import path 
from .views import get_user,create_user,user_detail,user_interface,user_update,user_delete


urlpatterns = [
    path('users/',get_user, name = 'get_user'),
    path('users/create/',create_user, name = 'create_user'),
    path('users/<int:pk>', user_detail, name = 'user_detail'),
    path('', user_interface, name='user_interface'),
    path('update/<int:pk>', user_update, name='user_update'),
    path('delete/<int:pk>', user_delete, name= 'user_delete')
]
