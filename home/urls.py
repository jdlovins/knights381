from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^account/login/', views.login_user, name='account-login'),
    url(r'^account/register/', views.register_user, name='account-register'),
    url(r'^account/logout/', views.logout_user, name='account-logout'),
    url(r'^account/view', views.user_profile, name='account-profile'),
    url(r'^$', views.index, name='index'),
    url(r'^catalog/', views.catalog, name='catalog'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^cart/', views.cart, name='cart')
]
