from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db import models



class Event(models.Model):
    '''
    Event model
    '''
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='images/') # here cloudinary imagefield
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    event_locked = models.BooleanField(default=False)
    date_lock = models.DateField(null=True, blank=True)
    total_expenses = models.FloatField()
    budget = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    left_to_pay = models.FloatField()

    def __str__(self):
        return self.title


class Expense(models.Model):
    '''
    Expense model
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.FloatField()
    purpose = models.CharField(max_length=200)
    receipt = models.BooleanField(default=False)
    # receipt_image = models.ImageField(upload_to='receipt_images/', blank=True, null=True) # here cloudinary imagefield
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.purpose} - {self.amount}"

