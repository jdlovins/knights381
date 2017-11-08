from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Books(models.Model):
    book_name = models.CharField(default='', blank=False, max_length=50)
    book_author = models.CharField(default='anonymous', blank=False, max_length=50)
    book_illustrator = models.CharField(default='', blank=True, max_length=50)
    book_publisher = models.CharField(default='', blank=False, max_length=50)
    book_datePublished = models.DateTimeField(default='', blank=True)
    book_numOfPages = models.IntegerField(default='', blank=True)
    book_hardback = models.BooleanField(default=False, blank=False)
    book_retailPrice = models.DecimalField(default=0, blank=False, decimal_places=2)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    steam_id = models.CharField(default='', blank=True, max_length=20)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

