# views.py

from django.shortcuts import render


def home(request):
    # Asumiendo que tienes un template llamado 'home.html'
    return render(request, "home.html")
