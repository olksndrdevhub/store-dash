import re
import time

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout, password_validation
from django.http.response import HttpResponse
from django.contrib.auth.password_validation import validate_password

from .models import User


def email_is_valid_with_regex(email: str):
    if not email or email == '':
        return False
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    return True


def email_is_available(email: str, model: type, field: str):
    if model.objects.filter(**{field: email}).exists():
        return False
    return True


# Create your views here.
def profile_view(request):
    '''
    Profile Page
    '''
    context = {}
    template_name = 'profile.html'

    if request.method == 'POST':
        print(request.POST)
        user = request.user
        data = request.POST

        if 'email' in data and data['email'] != user.email:
            email = data['email']
            if not email_is_valid_with_regex(email):
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Email is not valid!"
                )
                context['submitted_email'] = email
                context['email_error'] = "Email is not valid!"
                return render(request, template_name, context)
            if not email_is_available(email, User, 'email'):
                messages.add_message(
                    request,
                    messages.ERROR,
                    "User with email already exists, select another email!"
                )
                context['submitted_email'] = email
                context['email_error'] = "User with this email already exists!"
                return render(request, template_name, context)
            user.email = email

        if 'first_name' in data and data['first_name'] != user.first_name:
            first_name = data['first_name']
            if first_name is None or first_name.strip() == '':
                messages.add_message(
                    request,
                    messages.ERROR,
                    "First Name can not be empty!"
                )
                context['fname_error'] = "First Name can not be empty!"
                return render(request, template_name, context)
            first_name = first_name.strip()
            user.first_name = first_name

        if 'last_name' in data and data['last_name'] != user.last_name:
            last_name = data['last_name']
            if last_name is None or last_name.strip() == '':
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Last Name can not be empty!"
                )
                context['lname_error'] = "Last Name can not be empty!"
                return render(request, template_name, context)
            last_name = last_name.strip()
            user.last_name = last_name

        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'You successfully update your profile!')
    return render(request, template_name, context)


def signout_view(request):
    '''
    Just Sign Out view
    '''
    logout(request)
    response = redirect('signin_view')
    messages.add_message(request, messages.WARNING, 'You was sign out!')
    return response


def signin_view(request):
    '''
    Sign In Page
    '''
    context = {}
    if request.user.is_authenticated:
        return redirect('home_view')
    template_name = 'signin.html'

    response = render(request, template_name, context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'You successfully log in!')
            response = redirect('home_view')
            response['HX-Replace-Url'] = reverse('home_view')
            return response
        messages.add_message(request, messages.ERROR,
                             'Error! Wrong email or password...')
        
        response['HX-Retarget'] = 'form'
        response['HX-Reselect'] = 'form'

    return response


def signup_view(request):
    '''
    Register Page
    '''
    context = {}
    tempalte_name = 'signup.html'
    if request.method == 'POST':
        print(request.POST)
        first_name = request.POST.get('first_name')
        if first_name is None or first_name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "First Name can not be empty!"
            )
            context['fname_error'] = "First Name can not be empty!"
        else:
            first_name = first_name.strip()
            context['submitted_f_name'] = first_name
        last_name = request.POST.get('last_name').strip()
        if last_name is None or last_name.strip() == '':
            messages.add_message(
                request,
                messages.ERROR,
                "Last Name can not be empty!"
            )
            context['lname_error'] = "Last Name can not be empty!"
        else:
            last_name = last_name.strip()
            context['submitted_l_name'] = last_name
        email = request.POST.get('email').strip()
        if email is not None:
            email = email.strip()
            context['submitted_email'] = email
        if not email_is_valid_with_regex(email):
            messages.add_message(
                request,
                messages.ERROR,
                "Email is not valid!"
            )
            context['email_error'] = "Email is not valid!"
        if User.objects.filter(email=email).exists():
            messages.add_message(
                request,
                messages.ERROR,
                "User with email already exists, please Sign in!"
            )
            context['email_error'] = "User with this email already exists, please Sign in!"
        else:
            password = request.POST.get('password')
            if password is not None:
                password = password.strip()
            try:
                validate_password(
                    password,
                )
            except forms.ValidationError as errors:
                for error in errors:
                    messages.add_message(request, messages.ERROR, f'Error: {error}')
                context['password_error'] = "Password is not valid!"
            else:
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Registration success! You can log in now!"
                )
                response = HttpResponse()
                response['HX-Location'] = reverse('signin_view')
                return response
    return render(request, tempalte_name, context)


def hx_send_email_confirmation(request):
    if request.htmx:
        # TODO send an email
        print('send email confirmation')
    return HttpResponse('Success, check your email!')


def hx_update_userpic(request):
    template_name = 'profile.html'

    if request.method == 'POST':
        time.sleep(1)
        user = request.user
        if 'userpic' in request.FILES:
            userpic = request.FILES['userpic']
            user.userpic = userpic
            user.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'You successfully update your profile picture!'
            )
            return render(request, template_name)

    messages.add_message(
        request,
        messages.ERROR,
        'Error! Something went wrong...'
    )
    return render(request, template_name)
