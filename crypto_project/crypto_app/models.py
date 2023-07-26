from django.db import models


class CryptoData(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    percent_change_1h = models.CharField(max_length=100)
    percent_change_24h = models.CharField(max_length=100)
    percent_change_7d = models.CharField(max_length=100)
    market_cap = models.CharField(max_length=100)
    volume_24h = models.CharField(max_length=100)
    circulating_supply = models.CharField(max_length=100)

    def __str__(self):
        return self.name
