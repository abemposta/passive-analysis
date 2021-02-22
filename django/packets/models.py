from django.db import models

# Create your models here.
class Users(models.Model):
    nombre=models.CharField(max_length=25)
    password=models.CharField(max_length=50)
    token=models.CharField(max_length=100)

    def __unicode__(self):
        return self.token

