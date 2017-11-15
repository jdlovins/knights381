from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    cart_itemName = models.CharField(default='', blank=False, max_length=50)
    cart_itemPrice = models.DecimalField(default='', blank=False, max_digits=5, decimal_places=2)
    cart_shippingPrice = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=2)
    cart_salesTax = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=2)
    cart_numOfItems = models.IntegerField(default=0, blank=False)
    cart_subTotal = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=2)
    cart_discounts = models.DecimalField(default=0, blank=True, max_digits=5, decimal_places=2)
    cart_grandTotal = models.DecimalField(default=0, blank=False, max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_date = models.DateField(blank=False)
    review_rating = models.DecimalField(max_digits=2,decimal_places=1, blank=False)
    review_name = models.CharField(max_length=30, blank=False)
    review_content = models.CharField(max_length=500, blank=True)


# TODO: Add validation to model fields in back or front end. Not necessary for prototype
# TODO: Possibly add shipping related information instead of just billing. This includes implementing "Same as shipping"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    steam_id = models.CharField(default='', blank=True, max_length=20)

    # Billing Fields.
    address = models.CharField(default='', blank=True, max_length=70)
    phone_num = models.IntegerField(default='', blank=True)
    city = models.CharField(default='', blank=True, max_length=50)
    zip_code = models.IntegerField(default='', blank=True)

    STATE_CHOICES = (
        ('AK', 'Alabama'),
        ('AL', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
    )

    state = models.CharField(choices=STATE_CHOICES, default='AK', max_length=2)

    # Payment Fields

    card_num = models.IntegerField(default='',blank=True)
    card_name = models.CharField(max_length=30,blank=True)

    # - Most likely an easier way to implement this using regex but this should work for now.

    MONTH_CHOICES = (
        ('12', 'December'),
        ('11', 'November'),
        ('10', 'October'),
        ('9', 'September'),
        ('8', 'August'),
        ('7', 'July'),
        ('6', 'June'),
        ('5', 'May'),
        ('4', 'April'),
        ('3', 'March'),
        ('2', 'February'),
        ('1', 'January')
    )

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
