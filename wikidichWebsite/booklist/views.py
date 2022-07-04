from django.shortcuts import render

books = ['book1', 'book2', 'book3']

# Create your views here.
def index(request):
    return render(request, 'booklist/index.html', {'books': books})
