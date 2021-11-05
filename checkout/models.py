import uuid
from django.db import models
from django_countries.fields import CountryField
from plants.models import Plant


class Order(models.Model):
    order_uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False,
        null=False, blank=False
    )
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label='Select Country', null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def __str__(self):
        return str(self.order_uuid)


class OrderItem(models.Model):
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='orderitems'
    )
    plant = models.ForeignKey(
        Plant, null=False, blank=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f'{self.quantity} x {self.plant.name} '
            f'in order {self.order.__str__()}'
        )
