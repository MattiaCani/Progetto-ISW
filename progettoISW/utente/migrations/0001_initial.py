# Generated by Django 4.2.2 on 2023-06-17 16:38

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amministratore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=30)),
                ('cognome', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='default@default.com', max_length=30, unique=True)),
                ('password', models.CharField(default='password', max_length=30, unique=True)),
                ('adminID', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Carrello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importoTotale', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=30)),
                ('cognome', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='default@default.com', max_length=30, unique=True)),
                ('password', models.CharField(default='password', max_length=30, unique=True)),
                ('carrello', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.carrello')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numerocarta', models.PositiveBigIntegerField(default=1)),
                ('intestatario', models.CharField(default='', max_length=50)),
                ('nomemetodo', models.CharField(choices=[('Carta di credito', 'Credito'), ('Carta di debito', 'Debito')], default='Carta di credito', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ResocontoVendite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VetrinaAmministratore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listaProdotti', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Vetrina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listaProdotti', models.CharField(max_length=2000)),
                ('filtro', models.CharField(choices=[('NoFiltro', 'No Filtro'), ('PerTipologia', 'Per Tipologia'), ('PerPrezzo', 'Per Prezzo'), ('PerNumeroVendite', 'Per Nvendite'), ('PerDisponibilità', 'Per Disponibilita')], default='NoFiltro', max_length=20)),
                ('vetrina', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.vetrinaamministratore')),
            ],
        ),
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('tipologia', models.CharField(max_length=30)),
                ('quantitaAcquisto', models.PositiveIntegerField(default=1)),
                ('resVendite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='utente.resocontovendite')),
                ('vetrina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='utente.vetrina')),
                ('vetrinaAmministratore', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.vetrinaamministratore')),
            ],
        ),
        migrations.CreateModel(
            name='Ordine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailCliente', models.EmailField(max_length=30)),
                ('nomeCliente', models.CharField(max_length=30)),
                ('numeroOrdine', models.PositiveIntegerField(unique=True)),
                ('indirizzoSpedizione', models.CharField(max_length=50)),
                ('IDcliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.cliente')),
                ('carrello', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.carrello')),
            ],
        ),
        migrations.AddField(
            model_name='carrello',
            name='listaProdotti',
            field=models.ManyToManyField(to='utente.prodotto'),
        ),
        migrations.CreateModel(
            name='UtenteAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nome', models.CharField(default='', max_length=30)),
                ('cognome', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='default@default.com', max_length=30, unique=True)),
                ('password', models.CharField(default='password', max_length=30, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
