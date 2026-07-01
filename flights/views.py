from django.shortcuts import render
from .models import Airport, Flight, Passenger
# Create your views here.

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
        "passengers": Passenger.objects.filter(flights= flight)
    })