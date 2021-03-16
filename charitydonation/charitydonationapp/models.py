from django.db import models
from django.contrib.auth.models import User


TYPES = (
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna"),
)


class Category(models.Model):
    """
    - name
    """

    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Institution(models.Model):
    """
    - name
    - description
    - type (pole typu choices; możliwe typy: fundacja, organizacja pozarządowa, zbiórka lokalna; domyślnie fundacja)
    - categories (relacja wiele do wielu, do tabeli Category)
    """

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=1)
    categories = models.ManyToManyField(Category, default=None)


    def __str__(self):
        return f"{self.name} ({TYPES[self.type - 1][1]})"


class Donation(models.Model):
    """
    - quantity (liczba worków)
    - categories (relacja ManyToMany do modelu Category)
    - institution (klucz obcy do modelu Institution)
    - address (ulica plus numer domu)
    - phone_number (numer telefonu)
    - city
    - zip_code
    - pick_up_date
    - pick_up_time
    - pick_up_comment
    - user (klucz obcy do tabeli user; domyślna tabela zakładana przez django; może być Nullem, domyślnie Null).
    """

    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, default=None)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.quantity} by {self.user}"