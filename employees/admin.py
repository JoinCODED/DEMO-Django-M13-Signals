from django.contrib import admin

from employees import models

to_register = [
    models.Department,
    models.Employee,
]

admin.site.register(to_register)
