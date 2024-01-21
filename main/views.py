from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import Event, Expense, EventParticipant
from .forms import EventForm
from django.contrib.auth.models import User
from datetime import date
from django.views.generic.list import ListView
from django.urls import reverse


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
            # return redirect('expenseCalculatePage')
            return redirect(reverse('expenseCalculatePage', args=[event.id]))
        
        return render(request, self.template_name, {'form': form})
    
    
    

class DisplayEvent(ListView):
    """
    Display list of created events
    """
    model = Event
    template_name = 'events-overview.html'
    context_object_name = 'events'

    def get_queryset(self, **kwargs):
        events = self.model.objects.filter(user=self.request.user).select_related('user')
        return events
    

class ExpenseView(View):
    template_name = 'expenseCalculatePage.html'

    def get(self, request, event_id, *args, **kwargs):
        # Get the event based on the event_id
        event = get_object_or_404(Event, id=event_id)

        # Check if there are participants for the event
        participants = EventParticipant.objects.filter(event=event)
        if not participants:
            # If no participants, show a button to edit the event
            context = {
                'event': event,
                'edit_button_visible': True,
            }
        else:
            # If participants exist, display the Expenses template logic
            expenses = Expense.objects.filter(event=event)
            context = {
                'event': event,
                'participants': participants,
                'expenses': expenses,
            }

        return render(request, self.template_name, context)

    def post(self, request, event_id, *args, **kwargs):
        # Handle the form submission to add expenses
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        if request.method == 'POST':
            # Loop through the participants and save expenses for each
            for participant in EventParticipant.objects.filter(event=event):
                amount_key = f'amount_{participant.user.username}'
                purpose_key = f'purpose_{participant.user.username}'

                amount = request.POST.get(amount_key)
                purpose = request.POST.get(purpose_key)

                # Check if the amount is provided (not empty)
                if amount:
                    # Create the expense object and save it to the database
                    expense = Expense.objects.create(
                        user=participant.user,
                        event=event,
                        amount=amount,
                        purpose=purpose,
                    )
                    expense.save()

            return redirect(reverse('expenseCalculatePage', args=[event.id]))

        return render(request, self.template_name, {'event': event})