# Generated by Django 5.0.3 on 2024-04-18 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
