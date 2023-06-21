from django.contrib import admin
# credenziali superuser
# username: roberta, password: Berdjango

# Register your models here.
from .models import Amministratore, Pagamento, Carrello, Ordine, Cliente


admin.site.register(Pagamento)
admin.site.register(Carrello)
admin.site.register(Ordine)
admin.site.register(Cliente)
admin.site.register(Amministratore)


