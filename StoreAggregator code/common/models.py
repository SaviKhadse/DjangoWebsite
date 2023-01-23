from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=30, null=False)

    def __str__(self) -> str:
        return self.country_name
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Country'


class State(models.Model):
    state_name = models.CharField(max_length=30, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.state_name
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'State'


class City(models.Model):
    city_name = models.CharField(max_length=30, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.city_name
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'City'

