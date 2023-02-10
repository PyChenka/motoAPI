from django.db import models


class Bike(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    made_year = models.IntegerField()
    current_owner = models.ForeignKey('Owner', on_delete=models.PROTECT, related_name='current_bikes')
    previous_owners = models.ManyToManyField('Owner', through='Ownership', related_name='previous_bikes')

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    date_purchase = models.DateField(null=True)
    date_sale = models.DateField(null=True)

    def __str__(self):
        return f'{self.owner} {self.bike}'

