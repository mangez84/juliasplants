from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    filter_name = models.CharField(max_length=254)

    def __str__(self):
        return str(self.name)

    def get_filter_name(self):
        return self.filter_name


class Plant(models.Model):
    name = models.CharField(max_length=254)
    botanical_name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)
