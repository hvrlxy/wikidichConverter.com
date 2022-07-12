from email.policy import default
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from wikidichConverter.convert import *
from wikidichConverter.parse_mainpage import *
import os
from django.conf import settings
from django.conf import settings

# book_url = "pdfs/sample_book.pdf"
# is_file = os.path.exists(os.path.join(settings.MEDIA_ROOT, book_url))

class LinkForm(forms.Form):
    url = forms.URLField(label='Book\'s URL', max_length=10000)
    CHOICES = [('pdf', 'PDF'), ('epub', 'EPUB')]
    file_format = forms.ChoiceField(choices = CHOICES, label='Output Format', required=False)
    # epub = forms.BooleanField(label='EPUB', required=False)


books = ['book1', 'book2', 'book3']

# Create your views here.
def index(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            file_format = form.cleaned_data['file_format']
            book_name = ParseMainPage(url).get_book_name()
            book_name = book_name.replace(' ', '_')
            convert_pdf(url, os.path.join(settings.MEDIA_ROOT, 'pdfs/' + book_name + '.pdf'))
            books.append(book_name)
        else:
            return render(request, "wikidthConverter/index.html", {"form": form})    
    return render(request, "wikidthConverter/index.html", {"form": LinkForm()})


# Create your views here.
def all_books(request):
    return render(request, 'wikidthConverter/booklist.html', {'books': books})
