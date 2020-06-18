from django.urls import path
from .views import *

app_name = 'basic_app'

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logut/', user_logut, name="logout"),
    path('special/', special_view, name="special"),
]
