# Create your models here.
from django.db import models
from django.contrib.auth import logout
from utente.enums import MetodoPagamento
from django.contrib.auth.models import AbstractUser
from vetrine.models import VetrinaAmministratore, Vetrina, ResocontoVendite


class UtenteAuth(AbstractUser):
    nome = models.CharField(max_length=30, default="")
    cognome = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=30, unique=True, default="default@default.com")
    password = models.CharField(max_length=30, unique=True, default="password")
    isAdmin = models.BooleanField
    # problema: django di default fa funzionare il login con username e password, non con l'email,
    # modificarlo è un casino


# non si può usare questa come modello per gli utenti da usare perchè ha abstract=true, che serve per
# farla ereditare a cliente e amministratore
class Utente(models.Model):
    username = models.CharField(max_length=30, default="")
    nome = models.CharField(max_length=30, default="")
    cognome = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=30, unique=True, default="default@default.com")
    password = models.CharField(max_length=30, unique=True, default="password")
    isAdmin = models.BooleanField

    class Meta:
        abstract = True


class Amministratore(Utente):
    adminID = models.PositiveIntegerField()

    def __str__(self):
        return str(self.adminID)


class Prodotto(models.Model):
    pezziVenduti = models.PositiveIntegerField
    disponibilita = models.PositiveIntegerField(default=100)
    # unique necessario per modifica, elimina prodotto
    nome = models.CharField(max_length=30, unique=True)
    codiceSeriale = models.IntegerField(unique=True, default=0, primary_key=True)  # unique
    tipologia = models.CharField(max_length=30)
    descrizione = models.TextField(default="")
    quantitaAcquisto = models.PositiveIntegerField(default=1)
    prezzo = models.FloatField(default=0.0)
    vetrina = models.ForeignKey(Vetrina, on_delete=models.PROTECT, null=True)
    vetrinaAmministratore = models.ForeignKey(VetrinaAmministratore, on_delete=models.CASCADE, null=True)
    resVendite = models.ForeignKey(ResocontoVendite, on_delete=models.PROTECT, null=True)
    carrelloManyToMany = models.ManyToManyField('utente.Carrello')

    def __str__(self):
        return str(self.codiceSeriale)


class Carrello(models.Model):
    possessore = models.CharField(max_length=20, primary_key=True)
    listaProdotti = models.ManyToManyField('utente.Prodotto')
    importoTotale = models.FloatField(default=0.0)

    def __init__(self, possessore, importoTotale=0.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.possessore = possessore
        self.importoTotale = importoTotale

    def __str__(self):
        return self.possessore


class Cliente(Utente):
    carrello = models.OneToOneField(Carrello, on_delete=models.CASCADE, null=True)
    # se il carrello viene eliminato il cliente dovrebbe restare? Ha senso un cliente senza carrello?

    def __str__(self):
        return self.username



class Pagamento(models.Model):
    numerocarta = models.PositiveBigIntegerField(default=1)
    intestatario = models.CharField(max_length=50, default="")
    nomemetodo = models.CharField(max_length=20, choices=MetodoPagamento.choices, default=MetodoPagamento.CREDITO)

    def __init__(self, numerocarta, intestatario, nomemetodo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numerocarta = numerocarta
        self.intestatario = intestatario
        self.nomemetodo = nomemetodo

    def __str__(self):
        return self.numerocarta


class Ordine(models.Model):
    IDcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    carrello = models.OneToOneField(Carrello, on_delete=models.CASCADE, null=True)
    emailCliente = models.EmailField(max_length=30)
    nomeCliente = models.CharField(max_length=30)
    numeroOrdine = models.PositiveIntegerField(unique=True)
    dataOrdine = models.DateTimeField
    indirizzoSpedizione = models.CharField(max_length=50)
    infoPagamento = Pagamento(numerocarta=models.BigIntegerField,
                              intestatario=models.CharField(max_length=50),
                              nomemetodo=models.CharField(max_length=20, choices=MetodoPagamento.choices,
                                                          default=MetodoPagamento.CREDITO))

    def __init__(self, IDcliente=None, carrello=None, emailCliente='', nomeCliente='', numeroOrdine=None,
                 dataOrdine=None, indirizzoSpedizione='', infoPagamento=None, *args, **kwargs):
        super(Ordine, self).__init__(*args, **kwargs)
        self.IDcliente = IDcliente
        self.carrello = carrello
        self.emailCliente = emailCliente
        self.nomeCliente = nomeCliente
        self.numeroOrdine = numeroOrdine
        self.dataOrdine = dataOrdine
        self.indirizzoSpedizione = indirizzoSpedizione
        self.infoPagamento = infoPagamento

    def __str__(self):
        return self.numeroOrdine


