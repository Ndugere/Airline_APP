from django.urls import path
from . import views

urlpatterns = [
    #passengers routes
    path("passengers", views.list_passengers, name = "list_passengers"),
    path("add_passenger", views.add_passenger, name="add_passenger"),
    path("delete_passenger/<int:passenger_id>", views.delete_passenger, name = "delete_passenger"),
    path("edit_passenger/<int:passenger_id>", views.edit_passenger, name="edit_passenger"),

    #Airports routes
    path("airports", views.list_airports, name="list_airports"),
    path("add_airport", views.add_airport, name= "add_airport"),

    #flights routes
    path("", views.index, name= "index"),
    
    path("<int:flight_id>", views.details, name="details"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/remove_passenger", views.remove_passenger, name= "remove_passenger")
]