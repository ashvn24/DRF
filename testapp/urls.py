from django.urls import path
from .views import *
urlpatterns = [
    path('reg/', CreateUserAPIView.as_view()),
    path('log/', LoginUserAPIView.as_view()),
    path('list/',ListUserPIView.as_view()),
    path('tok/',TokenLogin.as_view())
]
