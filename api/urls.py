from django.urls import path

from . import views

urlpatterns = [
    path("", views.IdentifyView.as_view()),
]
