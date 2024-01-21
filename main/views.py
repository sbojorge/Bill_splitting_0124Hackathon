from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import EventForm
from .models import Event, Expense, EventParticipant


# Create your views here.
class HomeView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)


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
                
                # ignore duplicated entries
                temp_members = []
                for member in members:
                    if member not in temp_members:
                        temp_members.append(member)
                members = temp_members
                for member in members:
                    if member != '':
                        print(member)
                        user = User.objects.filter(username=member).first()
                        print(user)
                        # Add the member to the event's members list
                        event_participant = EventParticipant.objects.create(
                            user=user,
                            event=event,)
            messages.success(request, 'Event was created successfully.')
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



class UpdateEventView(UpdateView):
    model = Event
    form_class = EventForm  # Reuse EventForm
    template_name = 'event-edit.html' 

    def get(self, request, *args, **kwargs):
        # First, call the base implementation to get the context
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        all_users = User.objects.all()
        all_users_usernames = [user.username for user in all_users]

        # Get existing members and add to context
        existing_members = EventParticipant.objects.filter(event=self.object).select_related('user')
        existing_members_usernames = [participant.user.username for participant in existing_members]
        context['users'] = all_users_usernames
        temp_members = existing_members_usernames + [''] * (10 - len(existing_members_usernames))
        context['input_users'] = [temp_members[i] for i in range(10)]

        return render(request, self.template_name, context)

    def get_success_url(self):
        # Redirect to a specific page on successful update
        return reverse_lazy('index')

    def form_valid(self, form):
        # Handle the event update logic
        event = form.save(commit=False)

        # Manually update the title
        event.title = form.cleaned_data['eventName']
        event = form.save()

        # Process members based on form data
        current_members_usernames = [
            form.cleaned_data.get(f'member{i+1}') for i in range(10)
            if form.cleaned_data.get(f'member{i+1}')
        ]

        # Ignore duplicated user entries

        temp_current_member = []
        for member in  current_members_usernames:
            if member not in temp_current_member:
                temp_current_member.append(member)
        current_members_usernames = temp_current_member

        # Get existing members for the event
        existing_members = EventParticipant.objects.filter(event=event)
        existing_members_usernames = [participant.user.username for participant in existing_members]

        # Remove members who are no longer in the form
        for participant in existing_members:
            if participant.user.username not in current_members_usernames:
                participant.delete()

        # Add new members from the form
        for username in current_members_usernames:
            if username not in existing_members_usernames:
                user = User.objects.filter(username=username).first()
                if user:
                    EventParticipant.objects.create(user=user, event=event)
        
        messages.success(self.request, 'Event was updated successfully.')
        return super().form_valid(form)

    def get_queryset(self):
        # Allow update to the event creator only
        return Event.objects.filter(user=self.request.user)



def delete_event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Ensure the user is allowed to delete the event
    if event.user != request.user:
        raise Http404("You are not allowed to delete this event.")

    event.delete()
    messages.success(request, 'Event was deleted successfully.')
    return HttpResponseRedirect(reverse('index'))  




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


def error_404(request, exception):
    """ A view to render a custom page for 404 errors """
    return render(request, '404.html')


class ContactView(View):
    template_name = 'contactPage.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)
