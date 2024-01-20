from django.contrib import admin
from .models import Event, Expense, EventParticipant

# Register your models here.
admin.site.register(Event)
admin.site.register(Expense)
admin.site.register(EventParticipant)
