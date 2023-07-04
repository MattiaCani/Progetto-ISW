from django.contrib import admin

# Register your models here.

from .models import Vetrina, VetrinaAmministratore, ResocontoVendite


class ShopAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        count = Vetrina.objects.all().count()
        if count == 0:
            return True

        return False


class ShopAdminAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        count = VetrinaAmministratore.objects.all().count()
        if count == 0:
            return True

        return False


admin.site.register(Vetrina, ShopAdmin)
admin.site.register(VetrinaAmministratore, ShopAdminAdmin)
admin.site.register(ResocontoVendite)
