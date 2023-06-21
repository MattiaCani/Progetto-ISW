from django.contrib import admin

# Register your models here.

from .models import Vetrina, VetrinaAmministratore, ResocontoVendite, Prodotto

admin.site.register(Prodotto)
admin.site.register(Vetrina)
admin.site.register(VetrinaAmministratore)
admin.site.register(ResocontoVendite)