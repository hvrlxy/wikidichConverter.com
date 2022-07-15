from email.policy import default
import mimetypes
import unicodedata
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from ftfy import fix_encoding
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


books = ['book1', 'book2', 'book3']

# Create your views here.
def index(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            file_format = form.cleaned_data['file_format']
            book_name = ParseMainPage(url).get_book_name()
            book_name = 'sample_book'
            book_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/' + book_name + '.pdf')
            convert_pdf(url,book_path)
            books.append(book_name)
            return render(request, "wikidthConverter/index.html", {"form": LinkForm(), "book_path": book_name})
        else:
            return render(request, "wikidthConverter/index.html", {"form": form, "book_path": None})    
    return render(request, "wikidthConverter/index.html", {"form": LinkForm(), "book_path": None})


# Create your views here.
def all_books(request):
    return render(request, 'wikidthConverter/booklist.html', {'books': books})

def download_file(request, file_path):
    print("this is the book name", file_path)
    file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/' + file_path + '.pdf')
    file_name = file_path.split('/')[-1]
    fl = open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    return response
