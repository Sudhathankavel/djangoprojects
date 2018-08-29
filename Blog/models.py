from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Blog(models.Model):
    content = models.CharField(validators=[MinLengthValidator(10)], max_length=300)
    # content = models.CharField(min_length=10, max_length=300)
    title = models.CharField(validators=[MinLengthValidator(10)], max_length=50)
    # title = models.CharField(min_length=10, max_length=50)
    secret_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title




