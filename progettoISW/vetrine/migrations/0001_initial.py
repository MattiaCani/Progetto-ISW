# Generated by Django 4.2.2 on 2023-07-07 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResocontoVendite',
            fields=[
                ('ID_resoconto', models.CharField(default='Resoconto', max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Resoconti',
            },
        ),
        migrations.CreateModel(
            name='Vetrina',
            fields=[
                ('ID_vetrina', models.CharField(default='Vetrina', max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Vetrine',
            },
        ),
        migrations.CreateModel(
            name='VetrinaAmministratore',
            fields=[
                ('ID_vetrina_admin', models.CharField(default='Vetrina Amministratore', max_length=30, primary_key=True, serialize=False)),
                ('vetrina', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='vetrine.vetrina')),
            ],
            options={
                'verbose_name_plural': 'Vetrine Amministratore',
            },
        ),
    ]
