from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator

# Create your models here.


class Blog(models.Model):
    content = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(300)], max_length=300)
    title = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(50)], max_length=50)
    secret_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title




