from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

category_choices = (
    ('S' , 'Shirt'),
    ('SW' , 'SportWear'),
    ('OW' , 'OutWear'),
)

label_choices = (
    ('P' , 'primary'),
    ('S' , 'secondary'),
    ('D' , 'danger')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True , null=True)
    category = models.CharField(choices=category_choices , max_length=2)
    label = models.CharField(choices=label_choices , max_length=1)
    description = models.TextField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('core:ItemDetails' , kwargs={
            'slug' : self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:AddToCart' , kwargs= {
            'slug' : self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('core:RemoveFromCart' , kwargs= {
            'slug' : self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, blank=True , null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_total_saved_price(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_finale_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress' , on_delete=models.SET_NULL , blank=True , null=True )
    payment = models.ForeignKey('Payment' , on_delete=models.SET_NULL , blank=True , null=True )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total =0
        for item in self.items.all():
            total += item.get_finale_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    countries = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    tran_id = models.CharField(max_length=200)
    amount = models.CharField(max_length=20)