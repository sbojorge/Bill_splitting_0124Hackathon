from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Event, Expense
from .forms import EventForm
from django.contrib.auth.models import User


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

# class EventView(View):
#     template_name = 'new-event.html'

#     def get(self, request, *args, **kwargs):
#         users = User.objects.all()  # Query all users
        
#         context = {
#             'users': users,
#         }
#         return render(request, self.template_name, context)

class EventView(View):
    template_name = 'new-event.html'

    def get(self, request, *args, **kwargs):
        form = EventForm()
        users = User.objects.all()
        context = {
            'users': users,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('home')
        
        return render(request, self.template_name, {'form': form})