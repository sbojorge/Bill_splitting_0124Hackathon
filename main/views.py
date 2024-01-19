from django.shortcuts import render
from django.contrib import messages
from django.views import View

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