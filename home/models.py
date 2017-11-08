from django.db import models

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

