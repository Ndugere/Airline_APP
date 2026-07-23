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
        passenger_name = request.POST.get("passenger_name", "").strip()
        if not passenger_name:
            return render(request, "flights/passengers.html", {
                "passengers": Passenger.objects.all(),
                "message": "Passenger name is required."
            })
        if len(passenger_name) > 120:
            return render(request, "flights/passengers.html", {
                "passengers": Passenger.objects.all(),
                "message": "Passenger name must be at most 120 characters."
            })
        Passenger.objects.create(name = passenger_name)
        return HttpResponseRedirect(reverse("list_passengers"))

def delete_passenger(request, passenger_id):
    if request.method == "POST":
        passenger_to_delete = get_object_or_404(Passenger, pk = passenger_id)
        passenger_to_delete.delete()
        return HttpResponseRedirect(reverse("list_passengers"))

def edit_passenger(request, passenger_id):
    passenger_to_edit = get_object_or_404(Passenger, pk = passenger_id)
    if request.method == "POST":
        new_name = request.POST.get("new_name", "").strip()
        if not new_name:
            return render(request, "flights/edit_passenger.html", {
                "passenger": passenger_to_edit,
                "message": "Passenger name is required."
            })
        if len(new_name) > 120:
            return render(request, "flights/edit_passenger.html", {
                "passenger": passenger_to_edit,
                "message": "Passenger name must be at most 120 characters."
            })
        passenger_to_edit.name = new_name
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
        code = request.POST.get("code", "").strip()
        city = request.POST.get("city", "").strip()
        if not code or not city:
            return render(request, "flights/list_airport.html", {
                "airports": Airport.objects.all(),
                "message": "Both code and city are required."
            })
        if len(code) > 5:
            return render(request, "flights/list_airport.html", {
                "airports": Airport.objects.all(),
                "message": "Airport code must be at most 5 characters."
            })
        if len(city) > 64:
            return render(request, "flights/list_airport.html", {
                "airports": Airport.objects.all(),
                "message": "City must be at most 64 characters."
            })
        Airport.objects.create(code = code, city = city)
        return HttpResponseRedirect(reverse("list_airports"))

def delete_airport(request, airport_id):
    if request.method == "POST":
        airport_to_delete = get_object_or_404(Airport, pk = airport_id)
        airport_to_delete.delete()
        return HttpResponseRedirect(reverse("list_airports"))

def edit_airport(request, airport_id):
    airport_to_edit = get_object_or_404(Airport, pk= airport_id)
    if request.method ==  "POST":
        code = request.POST.get("code", "").strip()
        city = request.POST.get("city", "").strip()
        if not code or not city:
            return render(request, "flights/edit_airport.html", {
                "airport": airport_to_edit,
                "message": "Both code and city are required"
            })
        if len(code) > 5:
            return render(request, "flights/edit_airport.html", {
                "airport": airport_to_edit,
                "message": "Airport code must be at most 5 characters."
            })
        if len(city) > 64:
            return render(request, "flights/edit_airport.html", {
                "airport": airport_to_edit,
                "message": "City must be at most 64 characters."
            })
        airport_to_edit.code = code
        airport_to_edit.city = city
        airport_to_edit.save()
        return HttpResponseRedirect(reverse("list_airports"))
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
    flight = get_object_or_404(Flight, pk = flight_id)
    return render(request, "flights/details.html", {
        "flight": flight,
        "passengers": Passenger.objects.filter(flights= flight),
        "non_passengers": Passenger.objects.exclude(flights = flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = get_object_or_404(Flight, pk = flight_id)
        passenger_id = safe_int(request.POST.get("passenger"))
        if passenger_id is None:
            return HttpResponseRedirect(reverse("details", args=(flight_id,)))
        passenger = get_object_or_404(Passenger, pk = passenger_id)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("details", args=(flight_id,)))

def remove_passenger(request, flight_id):
    if request.method == "POST":
        flight = get_object_or_404(Flight, pk = flight_id)
        passenger_id = safe_int(request.POST.get("passenger"))
        if passenger_id is None:
            return HttpResponseRedirect(reverse("details", args=(flight_id,)))
        passenger = get_object_or_404(Passenger, pk = passenger_id)
        passenger.flights.remove(flight)
        return HttpResponseRedirect(reverse("details", args=(flight_id,) ))
    

def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def add_flight(request):
    if request.method == "POST":
        origin_id = safe_int(request.POST.get("origin_id"))
        destination_id = safe_int(request.POST.get("destination_id"))
        duration = safe_int(request.POST.get("duration"))

        if origin_id and destination_id and duration and origin_id != destination_id and duration > 0:
            origin = get_object_or_404(Airport, pk=origin_id)
            destination = get_object_or_404(Airport, pk=destination_id)
            Flight.objects.create(origin=origin, destination=destination, duration=duration)
            return HttpResponseRedirect(reverse("index"))

        return render(request, "flights/add_flight.html", {
            "message": "Invalid input: duration must be positive and origin/destination must differ.",
            "airports": Airport.objects.all()
        })

    return render(request, "flights/add_flight.html", {
        "airports": Airport.objects.all(),
        "message": ""
    })

def delete_flight(request, flight_id):
    if request.method =="POST":
        flight_to_delete = get_object_or_404(Flight, pk=flight_id)
        flight_to_delete.delete()
    return HttpResponseRedirect(reverse("index"))


