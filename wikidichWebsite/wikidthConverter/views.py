from email.policy import default
from django.shortcuts import render
from django.http import HttpResponse
from django import forms

class LinkForm(forms.Form):
    url = forms.URLField(label='Book\'s URL', max_length=10000)
    CHOICES = [('pdf', 'PDF'), ('epub', 'EPUB')]
    file_format = forms.ChoiceField(choices = CHOICES, label='Output Format', required=False)
    # epub = forms.BooleanField(label='EPUB', required=False)


books = ['book1', 'book2', 'book3']

# Create your views here.
def index(request):
    return render(request, "wikidthConverter/index.html", {"form": LinkForm()})


# Create your views here.
def all_books(request):
    return render(request, 'wikidthConverter/booklist.html', {'books': books})