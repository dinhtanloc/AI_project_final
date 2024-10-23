from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    start = models.DateField()
    interval = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol
