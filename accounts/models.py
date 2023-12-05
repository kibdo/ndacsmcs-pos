from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
from datetime import datetime


class CustomUser(AbstractUser):
    is_salesman = models.BooleanField(default=False)
    date_added = models.CharField('Date Added', max_length=100)
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
