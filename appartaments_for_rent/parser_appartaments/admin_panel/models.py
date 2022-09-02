
from django.db import models
from datetime import datetime 
from django.utils import timezone

# {self.title}\t{self.price}\t{self.date}\t{self.url}

class Apartment(models.Model):
    """Model of appartaments"""
    title = models.TextField(
        verbose_name="Заголовок объявления",
        max_length=200
    )
    price = models.PositiveIntegerField(verbose_name='Цена в BYN')
    date = models.DateField(verbose_name='Дата объявления', default=datetime.now)
    url = models.URLField(verbose_name='Ссылка на объявление', max_length=100)
    val = models.TextField(verbose_name="Валюта", default='BYN', blank=True)
    
    def __str__(self):
        return f'{" ".join(self.title.split()[:6])}'

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        ordering = ['-date']
    

