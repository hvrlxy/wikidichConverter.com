from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "wikidthConverter/index.html")

def greet(request, name):
    return HttpResponse(f"Hello, {name}!")