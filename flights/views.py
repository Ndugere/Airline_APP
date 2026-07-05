from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Airport, Flight, Passenger
# Create your views here.


def list_passengers(request):
    return render(request, "flights/passengers.html", {
        "passengers": Passenger.objects.all()
    })

def add_passenger(request):
    if request.method == "POST":
        passenger_name = request.POST["passenger_name"]
        Passenger.objects.create(name = passenger_name)
        return HttpResponseRedirect(reverse("list_passengers"))

def delete_passenger(request, passenger_id):
    if request.method == "POST":
        passenger_to_delete = Passenger.objects.get(pk = passenger_id)
        passenger_to_delete.delete()
        return HttpResponseRedirect(reverse("list_passengers"))



def index(request):
    return render( request,
        "flights/index.html", {
            "flights": Flight.objects.all()
        }
    )

def details(request, flight_id):
    flight = Flight.objects.get(pk = flight_id)
    return render(request, "flights/details.html", {
        "flight": Flight.objects.get(pk = flight_id),
        "passengers": Passenger.objects.filter(flights= flight),
        "non_passengers": Passenger.objects.exclude(flights = flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk = flight_id)
        passenger = Passenger.objects.get(pk = int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("details", args=(flight_id,)))

def remove_passenger(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk = flight_id)
        passenger = Passenger.objects.get(pk = int(request.POST["passenger"]))
        passenger.flights.remove(flight)
        return HttpResponseRedirect(reverse("details", args=(flight_id,) ))

