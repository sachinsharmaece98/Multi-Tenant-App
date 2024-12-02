from django.db import models
class User(models.Model):
    
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=13,
        blank=True,
        null=True,
    )
    