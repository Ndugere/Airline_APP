from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path("<int:flight_id>", views.details, name="details"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/remove_passenger", views.remove_passenger, name= "remove_passenger")
]