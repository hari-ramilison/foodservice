from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
class Customer(models.Model):
    cust_name = models.CharField(max_length=50, verbose_name='Customer name')
    organization = models.CharField(max_length=100, blank=True, verbose_name='Organization')
    role = models.CharField(max_length=100, verbose_name='Role')
    email = models.EmailField(max_length=100, verbose_name='Email')
    bldgroom = models.CharField(max_length=100, verbose_name='Building room')
    address = models.CharField(max_length=200, verbose_name='Address')
    account_number = models.IntegerField(blank=False, null=False, verbose_name='Account number')
    city = models.CharField(max_length=50, verbose_name='City')
    state = models.CharField(max_length=50, verbose_name='State')
    zipcode = models.CharField(max_length=10, verbose_name='Zip code')
    phone_number = models.CharField(max_length=50, verbose_name='Phone number')
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_name)

# Create your models here.
class Service(models.Model):
    cust_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='services', verbose_name='Customer name')
    service_category = models.CharField(max_length=100, verbose_name='Service category')
    description = models.TextField(verbose_name='Description')
    location = models.CharField(max_length=200, verbose_name='Location')
    setup_time = models.DateTimeField(
        default=timezone.now, verbose_name='Setup time')
    cleanup_time = models.DateTimeField(
        default=timezone.now, verbose_name='Clean up time')
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Service Charge')
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_name)

class Product(models.Model):
    cust_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products', verbose_name='Customer name')
    product = models.CharField(max_length=100, verbose_name='Product')
    p_description = models.TextField(verbose_name='Description')
    quantity = models.IntegerField(verbose_name='Quantity')
    pickup_time = models.DateTimeField(
        default=timezone.now, verbose_name='Pickup time')
    charge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Charge')
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_name)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)