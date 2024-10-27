from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('animal_predict/', views.predict_animal_sign),
    path('gpt_search/', views.gpt_search),
]

