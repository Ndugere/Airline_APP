from django.urls import path
from . import views

urlpatterns = [
    #passengers routes
    path("passengers", views.list_passengers, name = "list_passengers"),

    #flights routes
    path("", views.index, name= "index"),
    path("<int:flight_id>", views.details, name="details"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/remove_passenger", views.remove_passenger, name= "remove_passenger")
]