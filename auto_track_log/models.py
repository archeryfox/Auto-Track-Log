from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description


class User(models.Model):
    login = models.CharField(max_length=50,unique=False)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)  # Пример поля роли пользователя

    def __str__(self):
        return self.login


class CostCalculation(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    maintenance_costs = models.IntegerField()
    fuel_costs = models.IntegerField()


class ServiceSchedule(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    work_scope = models.CharField(max_length=150)


class Vehicle(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    num = models.IntegerField()
    year_of_release = models.IntegerField()
    colour = models.CharField(max_length=50)
    engine_power = models.IntegerField()
    fuel_rate = models.IntegerField()
    mileage = models.IntegerField()

    def __str__(self):
        return f"{self.brand} {self.model} {self.num}"
