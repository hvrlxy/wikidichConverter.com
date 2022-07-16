import os
import re
import sys
from email.policy import default
import mimetypes
import unicodedata
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from ftfy import fix_encoding
from wikidichConverter.convert import *
from wikidichConverter.parse_mainpage import *
from django.conf import settings
from django.conf import settings
from .models import FileInfo, Book
import datetime as dt

class LinkForm(forms.Form):
    url = forms.URLField(label='Book\'s URL', max_length=10000)
    CHOICES = [('pdf', 'PDF'), ('epub', 'EPUB')]
    file_format = forms.ChoiceField(choices = CHOICES, label='Output Format', required=False)


patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    """
    Cre: https://sangnd.wordpress.com/2014/01/03/python-chuyen-tieng-viet-co-dau-thanh-khong-dau/
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def book_in_database(book_name: str):
    '''
    This function checks if the book is in the database.
    book_name: the name of the book
    Return: True if the book is in the database, False otherwise
    '''
    book = Book.objects.filter(bookName=book_name)
    if book:
        return True
    else:
        return False

# Create your views here.
def index(request):
    '''
    This is the main page of the website.
    '''
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            file_format = form.cleaned_data['file_format']
            book_name = convert(ParseMainPage(url).get_book_name()).replace(' ', '_')

            md_path = os.path.join(settings.MEDIA_ROOT, 'md/' + book_name + '.md')
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/' + book_name + '.pdf')
            epub_path = os.path.join(settings.MEDIA_ROOT, 'epubs/' + book_name + '.epub')

            # Check if the book is in the database
            if not book_in_database(book_name):
                convert_md(url,md_path)
                convert_pdf(md_path,pdf_path)
                convert_epub(md_path,epub_path)

                # save the file info to the database
                pdf_file = FileInfo(file_name=book_name, format='pdf')
                pdf_file.save()
                epub_file = FileInfo(file_name=book_name, format='epub')
                epub_file.save()

                # save the book to the database
                book = Book(dateAdded=dt.datetime.now(), bookName=book_name.replace('_', ' '), bookURL=url, PDFfile=pdf_file, EPUBfile=epub_file)
                book.save()

            # redirect to the download page
            return render(request, "wikidthConverter/index.html", {"form": LinkForm(), "book_path": book_name})
        else:
            return render(request, "wikidthConverter/index.html", {"form": form, "book_path": None})    
    return render(request, "wikidthConverter/index.html", {"form": LinkForm(), "book_path": None})


# Create your views here.
def all_books(request):
    '''
    This is the page that shows all the books that have been converted.
    '''
    books = Book.objects.all()
    return render(request, 'wikidthConverter/booklist.html', {'books': books})

def download_file(request, file_path: str, file_format: str):
    '''
    This is the page that shows the download link of the book.
    file_path: the path of the file
    file_format: the format of the file
    '''
    print("this is the book name", file_path)
    if file_format == 'pdf':
        file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/' + file_path + '.pdf')
    else:
        file_path = os.path.join(settings.MEDIA_ROOT, 'epubs/' + file_path + '.epub')
    file_name = file_path.split('/')[-1]
    fl = open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    return response
