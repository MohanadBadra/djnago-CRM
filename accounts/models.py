from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='profile.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def create_customer(sender, instance, created, **kwargs):
    if created and instance.groups.all()[0].name == 'customer':
        print('daaaaaaaaaaaaaad', instance.groups.all())
        Customer.objects.create(user=instance, name=instance)
        print("________CREATED_________")
        
post_save.connect(create_customer, sender=User)

class Tag(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Out  door", "Out  door"),
    )
    name = models.CharField(max_length=800)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=80, choices=CATEGORY)
    description = models.CharField(max_length=800, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out of delivery", "Out of delivery"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS)
    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.product.name