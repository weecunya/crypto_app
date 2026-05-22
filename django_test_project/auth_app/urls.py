from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),


    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),


    path('projects/', views.projects_list, name='projects_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),


    path('users/', views.admin_users_list, name='admin_users_list'),
    path('users/<int:user_id>/role/', views.admin_change_role, name='admin_change_role'),
]