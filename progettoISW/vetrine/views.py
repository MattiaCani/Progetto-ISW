from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from vetrine.forms.forms_prodotti import NuovoProdottoForm, ModificaProdottoForm
from vetrine.models import VetrinaAmministratore, Vetrina, ResocontoVendite
from utente.forms.forms_ordini import QuantitaProdottoVetrina
from utente.models import Prodotto, Ordine, Carrello
from django.db.models import Q  # classe per effettuare query complesse al DB
from django.contrib import messages


def carica_vetrina(request, tipo_vetrina):
    elenco_prodotti = tipo_vetrina.prodotto_set.all()

    elenco_tipologie = elenco_prodotti.values('tipologia').distinct()
    elenco_disponibilita = ['Ultime scorte', 'Disponibile', 'Illimitata']

    if not request.user.is_superuser:
        elenco_prodotti = tipo_vetrina.prodotto_set.exclude(disponibilita=0)

    disponibilita, tipologia, elenco_prodotti = tipo_vetrina.aggiungi_filtro(request, elenco_prodotti)
    elenco_prodotti = tipo_vetrina.ricerca_prodotto(request, elenco_prodotti)
    elenco_prodotti = tipo_vetrina.azzera_filtri(request, elenco_prodotti)


    context = {
        'elenco_prodotti': elenco_prodotti,
        'elenco_tipologie': elenco_tipologie,
        'elenco_disponibilita': elenco_disponibilita,
        'tipologia_filtrata': tipologia,
        'disponibilita_filtrata': disponibilita,
    }

    if not request.user.is_superuser:
        carrello = get_object_or_404(Carrello, possessore=request.user)
        prodotti = [pc.prodotto for pc in carrello.lista_prodotti.all()]
        context['carrello'] = prodotti

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
        form_nuovo_prodotto = NuovoProdottoForm(request.POST)

        if form_nuovo_prodotto.is_valid():
            form_nuovo_prodotto.save()
            return redirect('vetrina_amministratore')
    else:
        form_nuovo_prodotto = NuovoProdottoForm()

    return render(request, 'prodotti/aggiungiProdotto.html', {'form_nuovo_prodotto': form_nuovo_prodotto})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def rimuovi_prodotto_view(request, codice_seriale):
    get_object_or_404(Prodotto, codice_seriale=codice_seriale).delete()
    return redirect('vetrina_amministratore')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def modifica_prodotto_view(request, codice_seriale):
    prodotto = get_object_or_404(Prodotto, codice_seriale=codice_seriale)

    if request.method == 'POST':
        # Ottenere i dati dal form di modifica e applicare le modifiche al prodotto
        form = ModificaProdottoForm(request.POST, instance=prodotto)

        if form.is_valid():
            form.save()

            return redirect('vetrina_amministratore')

    else:
        form = ModificaProdottoForm(initial={
            'nome': prodotto.nome,
            'tipologia': prodotto.tipologia,
            'descrizione': prodotto.descrizione,
            'prezzo': prodotto.prezzo,
            'disponibilita': prodotto.disponibilita,
        }, instance=prodotto)

    return render(request, 'prodotti/modificaProdotto.html', {'form_modifica_prodotto': form})


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def resoconto_vendite_view(request):
    ordini = Ordine.objects.all()

    resoconto_vendite = get_object_or_404(ResocontoVendite)

    elenco_prodotti = resoconto_vendite.prodotto_set.all()

    elenco_tipologie = elenco_prodotti.values('tipologia').distinct()
    elenco_disponibilita = ['Ultime scorte', 'Disponibile', 'Illimitata']

    disponibilita, tipologia, elenco_prodotti = Vetrina.aggiungi_filtro(request, elenco_prodotti)
    elenco_prodotti = Vetrina.ricerca_prodotto(request, elenco_prodotti)
    elenco_prodotti = Vetrina.azzera_filtri(request, elenco_prodotti)

    boh = sum(prodotto.guadagno_totale for prodotto in elenco_prodotti)

    context = {
        'ordini': ordini,
        'prodotti': elenco_prodotti,
        'resoconto_vendite': resoconto_vendite,
        'elenco_tipologie': elenco_tipologie,
        'elenco_disponibilita': elenco_disponibilita,
        'tipologia_filtrata': tipologia,
        'disponibilita_filtrata': disponibilita,
        'resoconto_totale': boh
    }

    return render(request, 'vetrine/resocontoVendite.html', context)


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def dettaglio_ordine_view(request, numero_ordine):
    ordine = get_object_or_404(Ordine, numero_ordine=numero_ordine)

    return render(request, 'vetrine/dettaglioOrdine.html', {'ordine': ordine})
