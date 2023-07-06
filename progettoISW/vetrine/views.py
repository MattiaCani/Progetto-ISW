from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm
from vetrine.models import VetrinaAmministratore, Vetrina
from utente.forms.forms_ordini import QuantitaProdottoVetrina
from utente.models import Prodotto
from django.db.models import Q  # classe per effettuare query complesse al DB


def carica_vetrina(request, tipo_vetrina):
    elenco_prodotti = tipo_vetrina.prodotto_set.all()
    elenco_tipologie = elenco_prodotti.values('tipologia').distinct()
    message = 'Nessun prodotto attualmente in vendita :('

    # Applicazione dei filtri
    tipologia = request.GET.get('tipologia')
    disponibilita = request.GET.get('disponibilita')
    prezzo_min = request.GET.get('prezzo_min')
    prezzo_max = request.GET.get('prezzo_max')

    if tipologia:
        elenco_prodotti = elenco_prodotti.filter(tipologia=tipologia)
    if disponibilita:
        elenco_prodotti = elenco_prodotti.filter(disponibilita__=disponibilita)
    if prezzo_min:
        elenco_prodotti = elenco_prodotti.filter(prezzo__gte=prezzo_min)  # maggiore o uguale
    if prezzo_max:
        elenco_prodotti = elenco_prodotti.filter(prezzo__lte=prezzo_max)  # minore o uguale

    # Ricerca dei prodotti
    search_query = request.GET.get('search_query')
    if search_query:
        elenco_prodotti = elenco_prodotti.filter(
            Q(nome__icontains=search_query) | Q(descrizione__icontains=search_query))

    # Azzeramento filtri
    reset_filters = request.GET.get('reset_filters')
    if reset_filters:
        elenco_prodotti = get_object_or_404(Vetrina).prodotto_set.all()

    context = {
        'elenco_prodotti': elenco_prodotti,
        'elenco_tipologie': elenco_tipologie,
        'tipologia_filtrata': tipologia,
        'error_message': message
    }

    return context


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def vetrina_cliente_view(request):
    context = carica_vetrina(request, get_object_or_404(Vetrina))
    context['form_quantita'] = QuantitaProdottoVetrina()
    return render(request, "vetrine/vetrina.html", context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def vetrina_amministratore_view(request):
    context = carica_vetrina(request, get_object_or_404(VetrinaAmministratore).vetrina)
    return render(request, "vetrine/vetrinaAmministratore.html", context=context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def nuovo_prodotto_view(request):
    if request.method == 'POST':
        form = NuovoProdottoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('vetrinaAmministratore')

    else:
        form = NuovoProdottoForm()

    return render(request, 'prodotti/aggiungiProdotto.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def rimuovi_prodotto_view(request, codice_seriale):
    get_object_or_404(Prodotto, codice_seriale=codice_seriale).delete()
    return redirect('vetrinaAmministratore')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def modifica_prodotto_view(request, codice_seriale):
    prodotto = get_object_or_404(Prodotto, codice_seriale=codice_seriale)

    if request.method == 'POST':
        # Ottenere i dati dal form di modifica e applicare le modifiche al prodotto
        form = ModificaProdottoForm(request.POST, instance=prodotto)

        if form.is_valid():
            form.save()

            return redirect('vetrinaAmministratore')

    else:
        form = ModificaProdottoForm(initial={
            'nome': prodotto.nome,
            'tipologia': prodotto.tipologia,
            'descrizione': prodotto.descrizione,
            'prezzo': prodotto.prezzo,
            'disponibilita': prodotto.disponibilita,
        }, instance=prodotto)

    return render(request, 'prodotti/modificaProdotto.html', {'form': form})
