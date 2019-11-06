from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def privacy_law(request):
    return render(request, 'privacy_law.html')
