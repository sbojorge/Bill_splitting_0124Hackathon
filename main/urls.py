from django.urls import path
from .views import HomeView, EventView, DisplayEvent

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
<<<<<<< Updated upstream
    path('index/',DisplayEvent.as_view(), name='index'),
=======
    path('', EventView.as_view(), name='new_event'),
>>>>>>> Stashed changes
]