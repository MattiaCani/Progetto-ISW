from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from vetrine.forms.nuovoProdotto import nuovoProdottoForm
from vetrine.forms.modificaProdotto import modificaProdottoForm
from vetrine.models import VetrinaAmministratore, Vetrina
from utente.models import Prodotto
from django.db.models import Q #classe per effettuare query complesse al DB

# Create your views here.
@login_required
def vetrina_clienteview(request):
    prodotti = Prodotto.objects.all()

    # Applicazione dei filtri
    tipologia = request.GET.get('tipologia')
    disponibilita = request.GET.get('disponibilita')
    prezzo_min = request.GET.get('prezzo_min')
    prezzo_max = request.GET.get('prezzo_max')

    if tipologia:
        prodotti = prodotti.filter(tipologia=tipologia)
    if disponibilita:
        prodotti = prodotti.filter(disponibilita=disponibilita)
    if prezzo_min:
        prodotti = prodotti.filter(prezzo__gte=prezzo_min) #maggiore o uguale
    if prezzo_max:
        prodotti = prodotti.filter(prezzo__lte=prezzo_max) #minore o uguale

    # Ricerca dei prodotti
    search_query = request.GET.get('search_query')
    if search_query:
        prodotti = prodotti.filter(Q(nome__icontains=search_query) | Q(descrizione__icontains=search_query))

    # Azzeramento filtri
    reset_filters = request.GET.get('reset_filters')
    if reset_filters:
        prodotti = Prodotto.objects.all()

    if prodotti.count() == 0:
        message = 'Nessun prodotto attualmente in vendita :('

    return render(request, 'vetrine/vetrinaCliente.html', {'prodotti': prodotti})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def vetrina_amministratoreview(request):
    prodotti = Prodotto.objects.all()


    if prodotti.count() == 0:
        message = 'Non hai ancora inserito prodotti'

    return render(request, 'vetrine/vetrinaAmministratore.html', {'prodotti': prodotti})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def nuovo_prodottoview(request):
    if request.method == 'POST':
        form = nuovoProdottoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            codiceSeriale = form.cleaned_data['codiceSeriale']
            tipologia = form.cleaned_data['tipologia']
            descrizione = form.cleaned_data['descrizione']
            disponibilita = form.cleaned_data['disponibilita']
            prezzo = form.cleaned_data['prezzo']


            # Creazione del nuovo prodotto
            nuovo_prodotto = Prodotto.objects.create(
                nome=nome,
                codiceSeriale=codiceSeriale,
                tipologia=tipologia,
                descrizione=descrizione,
                disponibilita=disponibilita,
                prezzo=prezzo
            )
            vetrina_amministratore = VetrinaAmministratore.objects.get(vetrinaidadmin="Vetrina Amministratore")

            vetrina_cliente = Vetrina.objects.get_or_create(
                vetrinaid="Vetrina Clienti",
                vetrina=vetrina_amministratore)
            vetrina_cliente = Vetrina.objects.get(vetrinaid="Vetrina Clienti")
            nuovo_prodotto.vetrina = vetrina_cliente
            nuovo_prodotto.vetrinaAmministratore = vetrina_amministratore
            nuovo_prodotto.save()



            return redirect(
                'vetrinaAmministratore')  # Redireziona alla vista della vetrina amministratore dopo l'inserimento del prodotto

    else:
        form = nuovoProdottoForm()

    return render(request, 'prodotti/aggiungiProdotto.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def rimuovi_prodotto_view(request, nomeprodotto):
    prodotto = Prodotto.objects.get(nome=nomeprodotto)
    prodotto.delete()
    message = 'Prodotto eliminato'
    return redirect('vetrinaAmministratore')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def modifica_prodotto_view(request, nomeprodotto):
    prodotto = Prodotto.objects.get(nome=nomeprodotto)

    if request.method == 'POST':
        # Ottenere i dati dal form di modifica e applicare le modifiche al prodotto
        form = modificaProdottoForm(request.POST)
        if form.is_valid():
            prodotto.nome = form.cleaned_data['nome']
            prodotto.codiceSeriale = form.cleaned_data['codiceSeriale']
            prodotto.tipologia = form.cleaned_data['tipologia']
            prodotto.descrizione = form.cleaned_data['descrizione']
            prodotto.prezzo = form.cleaned_data['prezzo']
            prodotto.disponibilita = form.cleaned_data['disponibilita']
            prodotto.save()
            return redirect('vetrinaAmministratore')
    else:
        form = modificaProdottoForm(initial={
            'nome': prodotto.nome,
            'tipologia': prodotto.tipologia,
            'codiceSeriale': prodotto.codiceSeriale,
            'descrizione': prodotto.descrizione,
            'prezzo': prodotto.prezzo,
            'disponibilita': prodotto.disponibilita,
        })

    return render(request, 'prodotti/modificaProdotto.html', {'form': form})
