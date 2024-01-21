from django.urls import path
from .views import HomeView, EventView, DisplayEvent, ExpenseView, UpdateEventView, delete_event_view, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('event/', EventView.as_view(), name='new_event'),
    path('index/', DisplayEvent.as_view(), name='index'),
    path('expense/<int:event_id>/', ExpenseView.as_view(), name='expenseCalculatePage'),
    path('event/edit/<int:pk>/', UpdateEventView.as_view(), name='edit_event'),
    path('event/delete/<int:pk>/', delete_event_view, name='delete_event'),    path('contact/', ContactView.as_view(), name='contactPage'),
    ]