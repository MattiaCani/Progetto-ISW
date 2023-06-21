# Create your views here.
from django.conf import settings


from . import forms
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from utente.forms.auth import LoginForm, SignupForm
from utente.models import Utente, Amministratore, Carrello, Cliente
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
                if user.is_superuser or user.is_admin:  # redirect a vetrina diversa a seconda che sia admin o no
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
            new_carrello = Carrello(    # si crea un carrello per ogni cliente
                importoTotale=0.00,
                listaProdotti=None
            )
            new_carrello.save()

            new_cliente = Cliente(
                username=form.cleaned_data['username'],
                nome=form.cleaned_data['nome'],
                cognome=form.cleaned_data['cognome'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                carrello=new_carrello
            )
            new_cliente.isAdmin = False
            new_cliente.save()

            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'registration/signup.html', context={'form': form})


