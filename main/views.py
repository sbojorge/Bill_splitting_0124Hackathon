from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .models import User, Event, Expense

# Create your views here.
class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # # Add the success message
        # messages.success(
        #     request,
        #     "Hello, welcome to the page!",
        #     extra_tags="alert alert-success alert-dismissible ",
        # )
        context = {
        }
        return render(request, self.template_name, context)

class EventView(View):
    template_name = 'new-event.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all()  # Query all users
        
        context = {
            'users': users,
        }
        return render(request, self.template_name, context)