from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Create your views here.

@login_required
def vetrina_clienteview(request):
    return render(request, 'vetrine/vetrinaCliente.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def vetrina_amministratoreview(request):
    return render(request, 'vetrine/vetrinaAmministratore.html')