from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length= 5)
    city = models.CharField(max_length= 64)

    def __str__(self):
        return f"City: {self.city} Code: ({self.code})"
    
class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.origin} , {self.destination}, {self.duration}"
    
class Passenger(models.Model):
    name = models.CharField(max_length= 120)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"Passenger's Name: {self.name}"