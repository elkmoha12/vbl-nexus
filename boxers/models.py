from django.db import models

class Club(models.Model):
    naam = models.CharField(max_length=100)
    stad = models.CharField(max_length=100)

    def __str__(self):
        return self.naam

class Boxer(models.Model):
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    geboortedatum = models.DateField(null=True, blank=True)
    gewichtsklasse = models.CharField(max_length=50, blank=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True)
    overwinningen = models.IntegerField(default=0)
    verlies = models.IntegerField(default=0)
    gelijkspel = models.IntegerField(default=0)
    rusttijd_tot = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"
    
class Combat(models.Model):
    RESULTAAT_CHOICES = [
        ('overwinning', 'Overwinning'),
        ('verlies', 'Verlies'),
        ('gelijkspel', 'Gelijkspel'),
    ]
    boxer = models.ForeignKey(Boxer, on_delete=models.CASCADE, related_name='combats')
    tegenstander = models.CharField(max_length=100)
    datum = models.DateField()
    evenement = models.CharField(max_length=200, blank=True)
    resultaat = models.CharField(max_length=20, choices=RESULTAAT_CHOICES)
    notities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.boxer} vs {self.tegenstander} - {self.resultaat}"
    
       