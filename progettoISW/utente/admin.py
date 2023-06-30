from django.contrib import admin
# credenziali superuser
# username: roberta, password: Berdjango

# Register your models here.
from .models import Pagamento, Carrello, Ordine, Prodotto, Utente, ProdottoCarrello


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


admin.site.register(Utente, UsersAdmin)
admin.site.register(Carrello, CartAdmin)
admin.site.register(Prodotto, ProductAdmin)
admin.site.register(ProdottoCarrello, ProductCartAdmin)

admin.site.register(Pagamento)
admin.site.register(Ordine)
