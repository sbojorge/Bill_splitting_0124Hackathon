from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Event, Expense, EventParticipant
from .forms import EventForm
from django.contrib.auth.models import User
from datetime import date
from django.views.generic.list import ListView


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
            current_date = date.today()
            print(form.cleaned_data, current_date)
            
            # Create the event object and save it to the database
            # check if the event already exists for the user by checking name and date
            if Event.objects.filter(user=request.user, title=form.cleaned_data['eventName'], date=current_date).exists():
                messages.error(request, 'Event already exists for the user and date.')
                return redirect('new_event')
            else:
                event = Event.objects.create(
                    title=form.cleaned_data['eventName'],
                    date=current_date,
                    user=request.user,)
                event.save()
                members = []
                for i in range(10):
                    member_event = form.cleaned_data[f'member{i+1}']
                    if member_event != '':
                        members.append(member_event)
                for member in members:
                    if member != '':
                        print(member)
                        user = User.objects.filter(username=member).first()
                        print(user)
                        # Add the member to the event's members list
                        event_participant = EventParticipant.objects.create(
                            user=user,
                            event=event,)
            return redirect('home')
        
        return render(request, self.template_name, {'form': form})
    

class DisplayEvent(ListView):
    """
    Display list of created events
    """
    model = Event
    template_name = 'events-overview.html'
    context_object_name = 'events'

    def get_queryset(self, **kwargs):
        events = self.model.objects.filter(user=self.request.user)
        return events