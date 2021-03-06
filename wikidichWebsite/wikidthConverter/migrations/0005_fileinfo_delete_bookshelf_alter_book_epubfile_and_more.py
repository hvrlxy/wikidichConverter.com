# Generated by Django 4.0.5 on 2022-07-15 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikidthConverter', '0004_bookshelf_remove_book_filename_book_epubfile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='BookShelf',
        ),
        migrations.AlterField(
            model_name='book',
            name='EPUBfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epub_file', to='wikidthConverter.fileinfo'),
        ),
        migrations.AlterField(
            model_name='book',
            name='PDFfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdf_file', to='wikidthConverter.fileinfo'),
        ),
    ]
