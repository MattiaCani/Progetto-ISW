# Generated by Django 4.2.2 on 2023-07-08 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vetrine', '0003_resocontovendite_totale_vendite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resocontovendite',
            name='totale_vendite',
        ),
    ]
