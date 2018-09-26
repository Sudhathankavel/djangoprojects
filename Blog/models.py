from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.CharField(validators=[MinLengthValidator(10)], max_length=300)
    title = models.CharField(validators=[MinLengthValidator(10)], max_length=50)
    secret_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title








