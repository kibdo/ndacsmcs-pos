from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone

# Create your models here.

# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True)
#     firstname = models.TextField()
#     middlename = models.TextField(blank=True,null= True)
#     lastname = models.TextField()
#     gender = models.TextField(blank=True,null= True)
#     dob = models.DateField(blank=True,null= True)
#     contact = models.TextField()
#     address = models.TextField()
#     email = models.TextField()
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
#     date_hired = models.DateField()
#     salary = models.FloatField(default=0)
#     status = models.IntegerField()
#     date_added = models.DateTimeField(default=timezone.now)
#     date_updated = models.DateTimeField(auto_now=True)

# def __str__(self):
#     return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    units = models.FloatField(default=1)
    sold_by = models.CharField(max_length=20, default='Unit')

    @property
    def total_stock_price(self):
        total_price = self.price * self.units
        if self.units <= 0:
            total_price = 0
        return int(total_price)

    def __str__(self):
        return self.code + " - " + self.name


class Sales(models.Model):
    is_credit = models.BooleanField(default=False)
    client_name = models.CharField(max_length=200, default=None)
    cooperative_number = models.CharField(max_length=100, default=None)
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    interest_rate = models.IntegerField(default=0)
    interest = models.IntegerField(default=0)

    def __str__(self):
        return self.code


class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)


class Settings(models.Model):
    interest_rate = models.IntegerField(default=9)
