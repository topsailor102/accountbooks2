from django.db import models
from django.urls import \
    reverse  # Used to generate URLs by reversing the URL patterns


class Sector(models.Model):
    """Model representing a expense sector"""

    name = models.CharField(max_length=200, help_text="expense area")

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Way(models.Model):
    """Model representing a way used for purchase."""

    WAY_KIND = (
        ("CASH", "Cash"),
        ("CITI", "CreditCard(Citi)"),
        ("N26", "N26"),
        ("ING", "ING"),
        ("BGL", "BGL"),
    )

    name = models.CharField(
        max_length=20,
        choices=WAY_KIND,
        blank=False,
        default="N26",
        help_text="purchase method",
    )

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Expense(models.Model):
    """Model representing each expense."""

    dateinfo = models.DateField(auto_now=False, null=True, blank=True)
    place = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    way = models.ForeignKey(
        "Way", on_delete=models.SET_NULL, null=True, help_text="choose a method"
    )
    summary = models.TextField(
        max_length=1000, default="summary for spending", help_text="describe details"
    )
    isfixed = models.BooleanField()
    sector = models.ForeignKey(
        "Sector", on_delete=models.SET_NULL, null=True, help_text="expense area"
    )
    creationinfo = models.DateField(auto_now=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.place

    def get_absolute_url(self):
        """Returns the url to access a detail record for this expense."""
        return reverse("expense-detail", args=[str(self.id)])

    class Meta:
        ordering = ["-dateinfo", "creationinfo", "sector"]

    def update_details(self):
        """Returns the url to access a detail record for this expense."""
        return reverse("expense-update", args=[str(self.id)])
