from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Airport, Flight, Passenger
# Create your views here.

### Views about Passengers
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

def edit_passenger(request, passenger_id):
    passenger_to_edit = Passenger.objects.get(pk = passenger_id)
    if request.method == "POST":
        passenger_to_edit.name = request.POST["new_name"]
        passenger_to_edit.save()
        return HttpResponseRedirect(reverse("list_passengers"))
    return render(request, "flights/edit_passenger.html", {
        "passenger": passenger_to_edit
    })

### views about Airports
def list_airports(request):
    return render(request, "flights/list_airport.html", {
        "airports": Airport.objects.all()
    })
def add_airport(request):
    if request.method == "POST":
        code, city = request.POST["code"], request.POST["city"]
        if code and city:
            Airport.objects.create(code = code, city = city)
        return HttpResponseRedirect(reverse("list_airports"))

def delete_airport(request, airport_id):
    if request.method == "POST":
        airport_to_delete = Airport.objects.get(pk = airport_id)
        if airport_to_delete:
            airport_to_delete.delete()
        return HttpResponseRedirect(reverse("list_airports"))

def edit_airport(request, airport_id):
    airport_to_edit = get_object_or_404(Airport, pk= airport_id)
    if request.method ==  "POST":
        code = request.POST.get("code")
        city = request.POST.get("city")
        if code and city:
            airport_to_edit.code = code
            airport_to_edit.city = city
            airport_to_edit.save()
            return HttpResponseRedirect(reverse("list_airports"))
        return render(request, "flights/edit_airport.html", {
            "airport": airport_to_edit,
            "messege": "Both code and city are required"
        })
    return render(request, "flights/edit_airport.html", {
        "airport": airport_to_edit
    })


### Views about Flights
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

