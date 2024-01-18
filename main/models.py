from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db import models



class Trip(models.Model):
    '''
    Trip model
    '''
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='images/') # here cloudinary imagefield
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    trip_concluded = models.BooleanField(default=False)
    total_expenses = models.FloatField()
    budget = models.FloatField()
    left_to_pay = models.FloatField()

    def __re__(self):
        return self.title


class Expense(models.Model):
    '''
    Expense model
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount = models.FloatField()
    purpose = models.CharField(max_length=200)
    receipt = models.BooleanField(default=False)
    # receipt_image = models.ImageField(upload_to='receipt_images/', blank=True, null=True) # here cloudinary imagefield
    paid = models.BooleanField(default=False)

    def __re__(self):
        return f"{self.user.username} - {self.purpose} - {self.amount}"

