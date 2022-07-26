from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_employee = models.BooleanField()


class Department(models.Model):
    name = models.CharField(max_length=30)


class Employee(models.Model):
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="employees",
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
    )

    def __str__(self) -> str:
        return str(self.user)
