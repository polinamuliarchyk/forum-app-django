from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('account', views.user_account, name='account'),
    path('settings/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='user_delete'),
]