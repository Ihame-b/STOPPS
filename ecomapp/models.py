from tokenize import String
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Admin(models.Model):
    """
    Super Admin Model
    
    Represents the main administrative users with full system access.
    These users can access all admin pages and Linfox pages.
    
    Note: There are two types of admin users:
    1. Super Admin (this model) - General system administrators
    2. LinfoxUser - Linfox-specific administrators (also has admin access)
    
    Both can login from /admin-login/ or /linfox-login/ and have the same access level.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True, default="kk 310st")
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True, default="kigali")
    county = models.CharField(verbose_name="County",max_length=100, null=True, blank=True, default="Rwanda")
    post_code = models.CharField(verbose_name="Post Code",max_length=8, null=True, blank=True, default="00000")
    has_profile = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.user.username
    def __str__(self):
        return f'{self.user}'

class LinfoxUser(models.Model):
    """
    Linfox User Model (Admin)
    
    Represents Linfox-specific administrative users.
    These users have admin access and can access all admin pages and Linfox pages.
    
    Note: There are two types of admin users:
    1. Super Admin (Admin model) - General system administrators
    2. LinfoxUser (this model) - Linfox-specific administrators (also has admin access)
    
    Both can login from /admin-login/ or /linfox-login/ and have the same access level.
    A user can have both Admin and LinfoxUser profiles simultaneously.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="linfox")
    mobile = models.CharField(max_length=20)
    

    def __str__(self):
        return self.user.username   

class ProductOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="productowner")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username              


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="customers", null=True, blank=True, default=None)
    joined_on = models.DateTimeField(auto_now_add=True)
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True, default="kk 310st")
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True, default="kigali")
    county = models.CharField(verbose_name="County",max_length=100, null=True, blank=True, default="Rwanda")
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True, default="kk 330st")
    town = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True, default="kigali")
    county = models.CharField(verbose_name="County",max_length=100, null=True, blank=True, default="Rwanda")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    productowner=models.CharField(User.get_full_name, max_length=300)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)   
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Cart: " + str(self.id)


Company = (
    ("LINFOX", "linfox"),
    ("KBS", "kbs"),
    ("OTHERS", "others"),
)
CARGO_STATUS = (
    ("Cargo Available", "Cargo Available"),
    ("Cargo Not Available", "Cargo Not Available"),
  
)

class Cargo(models.Model):
        CampanyName = models.CharField(max_length=20, choices=Company, default="Linfox")
        driverName=models.CharField(max_length=20, default="bob")
        # driverphone=models.CharField(max_length=20, default="0788558866")
        #driverEmail=models.EmailField(default="ihamegrbt@gmail.com")
        joined_on = models.DateTimeField(auto_now_add=True)
        address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True, default="kk 310st")
        image = models.ImageField(upload_to="products", default=0)
        price = models.PositiveIntegerField(default=0)
        view_count = models.PositiveIntegerField(default=0)
        cargo_status = models.CharField(max_length=50, choices=CARGO_STATUS, default="Cargo Available")
        created_by = models.ForeignKey(LinfoxUser, on_delete=models.CASCADE, null=True, blank=True, related_name='cargo_items', verbose_name="Created By")

  
        def __str__(self):
            return "Cardo: " + str(self.id)     

class LinfoxImage(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")
    

    def __str__(self):
        return self.cargo.CampanyName              


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    # driver= models.ForeignKey(Cargo.driverName,max_length=300,on_delete=models.CASCADE, default=Cargo.objects.first().pk)

    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)



METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("MOMO", "momo"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
    
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)


# Chat Models
class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chats')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='chats')
    product_owner = models.ForeignKey(ProductOwner, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['product', 'customer']

    def __str__(self):
        return f"Chat: {self.product.title} - {self.customer.full_name}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"


# Email Verification Token Model
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Email Verification Token"
        verbose_name_plural = "Email Verification Tokens"
    
    def __str__(self):
        return f"Verification for {self.user.email} - {'Verified' if self.is_verified else 'Pending'}"
