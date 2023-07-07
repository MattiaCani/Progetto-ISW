from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
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

    if not request.user.is_superuser:
        elenco_prodotti = tipo_vetrina.prodotto_set.exclude(disponibilita=0)

    tipologia, elenco_prodotti = tipo_vetrina.aggiungi_filtro(request, elenco_prodotti)
    elenco_prodotti = tipo_vetrina.ricerca_prodotto(request, elenco_prodotti)
    elenco_prodotti = tipo_vetrina.azzera_filtri(request, elenco_prodotti)

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
