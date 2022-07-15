from django.db import models
from django.forms import CharField

class FileInfo(models.Model):
    file_name = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.file_name} ({self.format})' 

# Create your models here.
class Book(models.Model):
    dateAdded = models.DateTimeField(auto_now_add=True)
    bookName = models.CharField(max_length=100)
    bookURL = models.URLField(max_length=1000)
    PDFfile = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='pdf_file')
    EPUBfile = models.ForeignKey(FileInfo, on_delete=models.CASCADE, related_name='epub_file')

    def __str__(self) -> str:
        return f'Book: {self.bookName} \n URL: {self.bookURL} \n PDF File: {self.PDFfile} \n EPUB File: {self.EPUBfile} \n Date Added: {self.dateAdded}'