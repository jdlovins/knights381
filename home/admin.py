from django.contrib import admin
from home.models import Profile, ShoppingCart, Review, Order, Book
# Register your models here.


admin.site.register(Profile)
admin.site.register(ShoppingCart)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Book)