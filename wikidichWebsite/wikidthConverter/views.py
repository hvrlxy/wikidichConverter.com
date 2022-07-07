from email.policy import default
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from wikidichConverter.convert import *
from wikidichConverter.parse_mainpage import *

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


def generate_file(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            file_format = form.cleaned_data['file_format']
            book_name = book_name = ParseMainPage(url).get_book_name()
            file_name = book_name + '.' + file_format
            if file_format == 'pdf':
                convert_pdf(url, "static/pdfs/" + file_name)
            return HttpResponse("<h1>Generating file for " + url + "</h1>")
    else:
        form = LinkForm()
    return render(request, 'wikidthConverter/download.html', {'file_name': file_name})