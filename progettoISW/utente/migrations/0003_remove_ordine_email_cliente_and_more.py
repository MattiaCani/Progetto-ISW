# Generated by Django 4.2.2 on 2023-07-07 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0002_alter_ordine_numero_ordine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordine',
            name='email_cliente',
        ),
        migrations.RemoveField(
            model_name='ordine',
            name='nome_cliente',
        ),
        migrations.AlterField(
            model_name='ordine',
            name='numero_carta',
            field=models.PositiveBigIntegerField(),
        ),
    ]