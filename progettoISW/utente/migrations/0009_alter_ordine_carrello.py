# Generated by Django 4.2.2 on 2023-07-11 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0008_alter_prodotto_prezzo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordine',
            name='carrello',
            field=models.JSONField(null=True),
        ),
    ]
