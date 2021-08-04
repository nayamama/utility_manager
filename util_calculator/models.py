import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


class Utility(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Bill(models.Model):
    pub_date = models.DateTimeField('data filled', default=timezone.now())
    bill_date = models.DateField(blank=False)
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        blank=False,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return "The remaining amount is " + str(self.amount) + " at " + str(self.bill_date)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Payment(models. Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField(blank=False)
    amount = models.DecimalField(
        max_digits=10,
        blank=False,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return "I paid " + str(self.amount) + " at " + str(self.payment_date)
