# Generated by Django 4.2.2 on 2023-06-30 11:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('vetrine', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Utenti',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Carrello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importo_totale', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name_plural': 'Carrelli',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_carta', models.PositiveBigIntegerField(default=1)),
                ('intestatario', models.CharField(default='', max_length=50)),
                ('nome_metodo', models.CharField(choices=[('Carta di credito', 'Credito'), ('Carta di debito', 'Debito')], default='Carta di credito', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Pagamenti',
            },
        ),
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('pezzi_venduti', models.PositiveIntegerField(default=0)),
                ('disponibilita', models.PositiveIntegerField(default=100)),
                ('nome', models.CharField(max_length=30, unique=True)),
                ('codice_seriale', models.IntegerField(default=0, primary_key=True, serialize=False, unique=True)),
                ('tipologia', models.CharField(max_length=30)),
                ('descrizione', models.TextField(default='')),
                ('prezzo', models.FloatField(default=0.0)),
                ('resVendite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='vetrine.resocontovendite')),
                ('vetrina', models.ForeignKey(default='Vetrina', null=True, on_delete=django.db.models.deletion.PROTECT, to='vetrine.vetrina')),
            ],
            options={
                'verbose_name_plural': 'Prodotti',
            },
        ),
        migrations.CreateModel(
            name='ProdottoCarrello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantita_acquisto', models.IntegerField(default=1)),
                ('prodotto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.prodotto')),
                ('utente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ordine',
            fields=[
                ('email_cliente', models.EmailField(max_length=30)),
                ('nome_cliente', models.CharField(max_length=30)),
                ('numero_ordine', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('indirizzo_spedizione', models.CharField(max_length=50)),
                ('carrello', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='utente.carrello')),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Ordini',
            },
        ),
        migrations.AddField(
            model_name='carrello',
            name='lista_prodotti',
            field=models.ManyToManyField(to='utente.prodottocarrello'),
        ),
        migrations.AddField(
            model_name='carrello',
            name='possessore',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
