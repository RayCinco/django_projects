from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100,null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null = True)
    quantity = models.PositiveIntegerField(null = True)
    product_image = models.ImageField(default='product.jpg',upload_to='Vegetable_Images')
    description = models.TextField(blank = True,null = True)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    date_updated = models.DateTimeField(auto_now=True)      # Automatically updated on save

    def __str__(self):
        return f'{self.name}-{self.quantity}'
    
    def formatted_date(self):
        return self.date_added.strftime("%B %d, %Y")
    
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    user = models.ForeignKey(User,models.CASCADE,null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null = True)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    order_notes = models.TextField(blank = True, null = True)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} ordered by {self.user.username}'
    

class OrderHistory(models.Model):
    #Delicates
    user = models.CharField(max_length=100, default='user')
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(max_length=50, choices=[('added', 'Added'), ('updated', 'Updated'),('purchased', 'Purchased')], default='added')


    def __str__(self):
        return f'History of {self.product_name}-{self.quantity}-P{self.price_per_item} bought by {self.customer_name} added by {self.user}  on {self.timestamp.strftime("%B %d, %Y")} ( {self.movement_type})'
    
    def formatted_date(self):
        return self.timestamp.strftime("%B %d, %Y")
    
class ProductHistory(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    movement_type = models.CharField(max_length=50, choices=[('added', 'Added'), ('updated', 'Updated'),], default='added')

    def __str__(self):
        return f'History of {self.name} on {self.date_added.strftime("%B %d, %Y")} ( {self.movement_type})'
    
    def formatted_date(self):
        return self.date_added.strftime("%B %d, %Y")