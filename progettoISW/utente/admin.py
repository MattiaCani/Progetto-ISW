import json

from django.contrib import admin
from .models import Carrello, Ordine, Prodotto, Utente, ProdottoCarrello
from django.utils.safestring import mark_safe


class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['importo_totale']
    list_display = ['possessore', 'importo_totale']


class ProductCartAdmin(admin.ModelAdmin):
    readonly_fields = ['importo_totale_prodotto']
    list_display = ['utente', 'prodotto', 'quantita_acquisto']


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informazioni", {"fields": ["nome", "codice_seriale", "tipologia", "descrizione"]}),
        ("Caratteristiche", {"fields": ["pezzi_venduti", "disponibilita", "prezzo", "vetrina", "resoconto_vendite"]}),
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
        ("Credenziali", {"fields": ["cliente", "get_email", "get_name"]}),
        ("Ricevuta", {"fields": ["numero_ordine", "indirizzo_spedizione", "data_ordine", "numero_carta", "intestatario", "nome_metodo"]}),
        ("Prodotti", {"fields": ['dati_carrello', 'importo_totale']})
    ]

    readonly_fields = ['dati_carrello', 'importo_totale', 'get_email', 'get_name']
    list_display = ['numero_ordine', 'cliente', 'data_ordine']

    def dati_carrello(self, instance):

        if instance.carrello is not None:
            return mark_safe('<pre>{}</pre>'.format(json.dumps(json.loads(instance.carrello), sort_keys=True, indent=2)))

    dati_carrello.short_description = 'Dati carrello'

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.cliente.email

    @admin.display(description='Nome cliente')
    def get_name(self, obj):
        return obj.cliente.first_name

    def has_add_permission(self, request):
        count = Ordine.objects.all().count()
        if count == -1:
            return True

        return False


admin.site.register(Utente, UsersAdmin)
admin.site.register(Carrello, CartAdmin)
admin.site.register(Prodotto, ProductAdmin)
admin.site.register(ProdottoCarrello, ProductCartAdmin)
admin.site.register(Ordine, OrdersAdmin)
