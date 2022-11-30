from django.urls import path
from .views import (
    home,
)


app_name = 'profiles'

urlpatterns = [
    path('', home, name='home'),
]
