# Generated by Django 4.0.5 on 2022-07-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikidthConverter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booklist',
            name='fileName',
            field=models.CharField(default='sample_book', max_length=100),
        ),
    ]
