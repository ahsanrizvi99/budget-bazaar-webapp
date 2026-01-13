from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=50, blank=True, null=True) 
    website = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None)

    FRUIT = 'Fruit'
    VEGETABLE = 'Vegetable'
    MEAT = 'Meat'
    FISH = 'Fish'
    TEA = 'Tea'
    RICE = 'Rice'
    OIL = 'Oil'
    EGGS = 'Eggs'
    SPICES = 'Spices'
    JUICE = 'Juice'

    CATEGORY_CHOICES = [
        (FRUIT, 'Fruit'),
        (VEGETABLE, 'Vegetable'),
        (MEAT, 'Meat'),
        (FISH, 'Fish'),
        (TEA, 'Tea'),
        (RICE, 'Rice'),
        (EGGS, 'Eggs'),
        (SPICES, 'Spices'),
        (JUICE, 'Juice'),
    ]

    def __str__(self):
        return self.name
