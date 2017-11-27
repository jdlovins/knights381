from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import STATE_CHOICES, MONTH_CHOICES

# Create your models here.


class Book(models.Model):
    book_name = models.CharField(default='', blank=False, max_length=50)
    book_author = models.CharField(default='anonymous', blank=False, max_length=50)
    book_illustrator = models.CharField(default='', blank=True, max_length=50)
    book_publisher = models.CharField(default='', blank=False, max_length=50)
    book_datePublished = models.DateTimeField(default='', blank=True)
    book_numOfPages = models.IntegerField(default='', blank=True)
    book_hardback = models.BooleanField(default=False, blank=False)
    book_retailPrice = models.DecimalField(default=0, blank=False, max_digits=5,decimal_places=2)

    def __str__(self):
        return f'{self.book_name} - {self.book_author}'


class Order(models.Model):
    order_number = models.IntegerField(default='', blank=False)
    order_numOfItems = models.IntegerField(default='', blank=False)
    order_totalAmount = models.DecimalField(default=0, blank=False, decimal_places=2, max_digits=5)
    order_shippingAddress = models.CharField(default='In-Store purchase', blank=False, max_length=100)
    order_shippingZipCode = models.IntegerField(default='', blank=False)
    order_paid = models.BooleanField(default=False, blank=False)
    order_shipped = models.BooleanField(default=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order_number}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return f'Shopping cart for: {self.user.username}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_date = models.DateField(blank=False)
    review_rating = models.DecimalField(max_digits=2,decimal_places=1, blank=False)
    review_name = models.CharField(max_length=30, blank=False)
    review_content = models.CharField(max_length=500, blank=True)


# TODO: Add validation to model fields in back or front end. Not necessary for prototype
# TODO: Possibly add shipping related information instead of just billing. This includes implementing "Same as shipping"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Billing Fields.
    address = models.CharField(default='', blank=True, max_length=70)
    phone_num = models.IntegerField(default=0, blank=True)
    city = models.CharField(default='', blank=True, max_length=50)
    zip_code = models.IntegerField(default=0, blank=True)
    state = models.CharField(choices=STATE_CHOICES, default='AK', max_length=2)
    # Payment Fields
    card_num = models.IntegerField(default=0,blank=True)
    card_name = models.CharField(max_length=30,blank=True)
    # - Most likely an easier way to implement this using regex but this should work for now.
    exp_month = models.CharField(choices=MONTH_CHOICES, max_length=2, default=12)
    exp_year = models.IntegerField(default=2017)

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
