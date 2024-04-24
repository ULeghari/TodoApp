from django.urls import path
from .views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    ToDoListCreateAPIView,
    ToDoDetailAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),

    path('todos/', ToDoListCreateAPIView.as_view(), name='todo-list-create'),
    path('todos/<str:name>/', ToDoDetailAPIView.as_view(), name='todo-detail'),
]
