from . import views
from django.urls import path

urlpatterns = [
    path('users', views.list_users, name="list-users"),
    path('manage_users', views.manage_users, name="manage_users-page"),
    path('save_user', views.save_user, name="save-user-page"),
    path('delete_user', views.delete_user, name="delete-user"),
]
