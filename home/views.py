from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, UserForm, ProfileForm, ContactForm
from .decorators import custom_login_required
from .models import Profile, Book, ShoppingCart
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    if request.user.is_authenticated():
        pass

    next_url = request.GET.get('next')

    signup_form = SignUpForm()
    login_form = LoginForm()
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form, 'next': next_url})


def login_user(request):
    if request.user.is_authenticated():
        redirect(index)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')

            user = authenticate(username=user_name, password=password)

            if user is not None:
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                login(request, user)
            else:
                messages.error(request, "Username or Password is invalid, please try again.")

        else:
            messages.error(request, form.errors)

    next_url = request.POST.get('next')

    if next_url is not None:
        return redirect(next_url)
    else:
        return redirect(index)


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user_name = form.cleaned_data.get('user_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(user_name, email, password)
            user.save()
            login(request, user)

            return redirect(index)
        else:
            # for e in form.errors:
            # for ee in form[e].errors:
            messages.error(request, form.errors)

    return redirect(index)


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect(index)


@custom_login_required
def user_profile(request):
    signup_form = SignUpForm()
    login_form = LoginForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(index)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'account/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'signup_form': signup_form,
        'login_form': login_form,
    })


def catalog(request):
    signup_form = SignUpForm()
    login_form = LoginForm()
    return render(request, 'catalog.html', {'signup_form': signup_form,
                                            'login_form': login_form})


def contact(request):
    signup_form = SignUpForm()
    login_form = LoginForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
    else:
        contact_form = ContactForm()

    book_list = Book.objects.all()

    return render(request, 'contact.html', {'form': contact_form, 'signup_form': signup_form, 'login_form': login_form,
                                            'book_list': book_list})


@login_required()
def cart(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        if book_id is not None:
            book = Book.objects.get(id=book_id)
            item_exist = ShoppingCart.objects.filter(user_id=request.user.id, book=book).first()
            if item_exist is not None:
                item_exist.quantity += 1
                item_exist.save()
            else:
                cart_item = ShoppingCart(user_id=request.user.id, book=book, quantity=1)
                cart_item.save()

    total_cart = ShoppingCart.objects.filter(user_id=request.user.id).all()

    total_price = 0
    for item in total_cart:
        total_price += (item.book.book_retailPrice * item.quantity)

    return render(request, 'cart.html', {'cart_items': total_cart, 'total_price': total_price})
