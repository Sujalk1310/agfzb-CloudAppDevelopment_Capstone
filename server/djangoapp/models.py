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


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name



class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"DealerReview ID: {self.id}\n" \
               f"Dealership: {self.dealership}\n" \
               f"Name: {self.name}\n" \
               f"Purchase: {self.purchase}\n" \
               f"Review: {self.review}\n" \
               f"Purchase Date: {self.purchase_date}\n" \
               f"Car Make: {self.car_make}\n" \
               f"Car Model: {self.car_model}\n" \
               f"Car Year: {self.car_year}\n" \
               f"Sentiment: {self.sentiment}"

