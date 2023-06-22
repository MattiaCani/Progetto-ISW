# Create your views here.
from django.conf import settings

from . import forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from utente.forms.auth import LoginForm, SignupForm
from utente.models import Utente, Amministratore, Carrello, Cliente
from vetrine.models import VetrinaAmministratore, Vetrina,Filtro
import datetime


def logoutview(request):
    logout(request)
    return redirect('login')


def loginview(request):
    form = forms.auth.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.auth.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Ciao {user.username}!'
                if not VetrinaAmministratore.objects.count() == 1:
                # se non esiste già crea una vetrina amministratore, a prescindere da chi faccia accesso
                    vetrina = VetrinaAmministratore(
                        vetrinaidadmin="Vetrina Amministratore",
                    )
                    vetrina.save()

                if user.is_superuser:  # redirect a vetrina diversa a seconda che sia admin o no
                    if Amministratore.objects.filter(username=user.username).exists():
                        return redirect('vetrinaAmministratore')
                    else:
                        current_datetime = datetime.datetime.now()
                        new_amministratore = Amministratore(
                            username=user.username,
                            nome="",
                            cognome="",
                            password=user.password,
                            # datetime corrente sottoforma di int come adminID, precisione al secondo
                            adminID=int(current_datetime.strftime("%Y%m%d%H%M%S"))
                        )
                        new_amministratore.isAdmin = True
                        new_amministratore.save()
                        return redirect('vetrinaAmministratore')
                else:
                    return redirect('vetrinaCliente')
            else:
                message = 'Login fallito'
    return render(
        request, 'registration/login.html', context={'form': form, 'message': message})


def signupview(request):
    form = forms.auth.SignupForm()
    if request.method == 'POST':
        form = forms.auth.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            # login(request, user)
            if not VetrinaAmministratore.objects.count() == 1:
                # se non esiste già crea una vetrina amministratore, a prescindere da chi si registri
                vetrina = VetrinaAmministratore(
                    vetrinaidadmin="Vetrina Amministratore",
                )
                vetrina.save()

            new_carrello = Carrello(  # si crea un carrello per ogni cliente
                possessore="Carrello",
                importoTotale=0.00
            )

            new_cliente = Cliente(
                username=form.cleaned_data['username'],
                nome=form.cleaned_data['nome'],
                cognome=form.cleaned_data['cognome'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                carrello=new_carrello
            )
            new_cliente.isAdmin = False
            new_carrello.possessore = "Carrello di "+str(new_cliente.username)
            new_carrello.save()
            new_cliente.carrello = new_carrello
            new_cliente.save()

            if not Vetrina.objects.count() == 1:
                vetrina_admin = VetrinaAmministratore.objects.get()
                vetrina_clienti = Vetrina(
                    vetrinaid="Vetrina Clienti",
                    vetrina=vetrina_admin
                )
                vetrina_clienti.save()

            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'registration/signup.html', context={'form': form})
