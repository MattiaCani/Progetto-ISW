# Generated by Django 4.2.2 on 2023-06-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='amministratore',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='cliente',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]