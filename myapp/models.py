from django.db import models

# Create your models here.
class Individual(models.Model):
    name = models.CharField(max_length = 100)
    birthdate = models.DateField()
    score = models.IntegerField()
    grade = models.CharField(max_length = 1) #assuming that grades are single characters

    def __str__(self):
        return self.name


