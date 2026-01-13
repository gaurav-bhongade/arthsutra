from django.urls import path
from .views import login_view, logout_view, user_list, user_create, user_update, user_delete

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:user_id>/update/', user_update, name='user_update'),
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),
]
