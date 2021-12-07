from django.db import models

class Register(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=15)
    phone=models.IntegerField()
    address=models.TextField()
    city=models.CharField(max_length=500)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.IntegerField()

class Category(models.Model):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='cimage')
    category_description=models.TextField()
    def __str__(self):
        return self.category_name

class Product(models.Model):
    category_name=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=500)
    product_price=models.IntegerField()
    product_dis1=models.TextField()
    product_dis2=models.TextField()
    product_image1=models.ImageField(upload_to='images')
    product_image2=models.ImageField(upload_to='images')
    product_image3=models.ImageField(upload_to='images')
    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.IntegerField()
    total=models.IntegerField()
        

class Slider(models.Model):
    slider_image=models.ImageField(upload_to='slider')
    slider_text=models.CharField(max_length=1000)

class Contact(models.Model):
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.IntegerField()
    phone1=models.IntegerField()
    phone2=models.IntegerField(blank=True)
    email1=models.EmailField()
    email2=models.EmailField(blank=True)

class SendMsg(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    msg=models.TextField()

class AddAddress(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    name=models.CharField(max_length=500)
    phone=models.IntegerField()
    email=models.EmailField()
    add=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.IntegerField()

step=(('Pending','Pending'),('Accepted','Accepted'),('Out for Delivery','Out for Delivery'),('Delivered','Delivered'))
class Order(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    address=models.ForeignKey(AddAddress,on_delete=models.CASCADE)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    quantity=models.IntegerField()
    total=models.IntegerField()
    status=models.CharField(choices=step,max_length=100,default='Pending')