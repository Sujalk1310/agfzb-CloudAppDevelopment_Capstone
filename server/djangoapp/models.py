from django.db import models
from django.utils.timezone import now

# CarMake model to save data about a car make
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# CarModel model to save data about a car model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
    ]
    car_type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    year = models.DateField()
    
    def __str__(self):
        return f"{self.car_make.name} - {self.name}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
