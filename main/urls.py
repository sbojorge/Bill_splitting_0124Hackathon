from django.urls import path
from .views import HomeView, EventView, ExpenseView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('event/', EventView.as_view(), name='new_event'),
    path('expense/<int:event_id>/', ExpenseView.as_view(), name='expenseCalculatePage'),
]