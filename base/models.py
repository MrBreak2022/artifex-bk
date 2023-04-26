import os
import random
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()   
from django.core.validators import MinValueValidator, MaxValueValidator  
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 2541783232)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "img/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

 
class Product(models.Model):

    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(1)], null=True)
    _id = models.AutoField(primary_key=True)
    selleremail = models.CharField(max_length=200, null=True, blank=True)
    bidding = models.BooleanField(default=False)

    def __str__(self):
        
        return f"{self.name} - {self.seller}"
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    paymentMethod = models.CharField(max_length=200,null=True,blank=True)
    taxPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    totalPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    _id =  models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.totalPrice} - {self.user}"

class OrderItem (models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    qty = models.IntegerField(null=True,blank=True,default=0)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    image = models.CharField(max_length=200,null=True,blank=True)
    _id =  models.AutoField(primary_key=True,editable=False)
    selleremail = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)





