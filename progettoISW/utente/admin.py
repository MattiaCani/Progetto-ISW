import json

from django.contrib import admin

from .models import Carrello, Ordine, Prodotto, Utente, ProdottoCarrello
from django.utils.safestring import mark_safe


class CartAdmin(admin.ModelAdmin):
    list_display = ['possessore', 'importo_totale']


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ['utente', 'prodotto', 'quantita_acquisto']


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informazioni", {"fields": ["nome", "codice_seriale", "tipologia", "descrizione"]}),
        ("Caratteristiche", {"fields": ["pezzi_venduti", "disponibilita", "prezzo"]}),
    ]
    list_display = ['nome', 'codice_seriale', 'prezzo', 'disponibilita']


class UsersAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Credenziali", {"fields": ["username", "password", "email", "first_name", "last_name"]}),
        ("Permessi", {"fields": ["is_superuser", "is_staff", "is_active"]}),
        ("Attività", {"fields": ["date_joined", "last_login"]}),
    ]
    list_display = ['username', 'is_superuser', 'email']


class OrdersAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Credenziali", {"fields": ["cliente", "email_cliente", "nome_cliente"]}),
        ("Ricevuta", {"fields": ["numero_ordine", "indirizzo_spedizione", "data_ordine", "numero_carta", "intestatario", "nome_metodo"]}),
        ("Prodotti", {"fields": ['dati_carrello']})
    ]
    readonly_fields = ['dati_carrello']
    list_display = ['numero_ordine', 'cliente', 'data_ordine']

    def dati_carrello(self, instance):
        formatted_json = json.dumps(json.loads(instance.carrello), sort_keys=True, indent=2)

        formatted_html = '<pre>{}</pre>'.format(formatted_json)
        return mark_safe(formatted_html)

    dati_carrello.short_description = 'Dati carrello'


admin.site.register(Utente, UsersAdmin)
admin.site.register(Carrello, CartAdmin)
admin.site.register(Prodotto, ProductAdmin)
admin.site.register(ProdottoCarrello, ProductCartAdmin)

admin.site.register(Ordine, OrdersAdmin)