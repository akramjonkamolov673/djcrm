from http.client import HTTPResponse
from smtplib import SMTPResponseException
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Record
from .forms import addrecord
import requests
from bs4 import BeautifulSoup
import pandas as pd

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.http import HttpResponse

# Create your views here.


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have login successfully!')
            return redirect('home')
        else:
            messages.success(request, 'Login error!!!')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have logout successfully!')
    return redirect('home')


def Register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request, "Please confirm your email address to complete the registration")
            return redirect('home')

        else:
            messages.success(request,'Something is wrong')
            form = SignUpForm()
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html',{'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(
            request, 'You should be authenticated to enter this page!!!')
        return redirect('home')


def delete_record(request, pk):
    delete_record = Record.objects.get(id=pk)
    delete_record.delete()
    messages.success(request, 'Record deleted successfully!!!')
    return redirect('home')


def add_record(request):
    form = addrecord()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = addrecord(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Record added succesfully.....')
                return redirect('home')
    else:
        messages.success(request, "You must have to login to add record!")
        return redirect('home')
    return render(request, 'addrecord.html', {'form': form})


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = addrecord(request.POST or None,request.FILES or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated succesfully.....')
            return redirect('home')
        return render(request, 'update.html', {'form': form})
    else:
        messages.success(
            request, 'You are  not login! please login to update records')
        return redirect('home')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def Change_Password(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(
                request, 'Your password has be changed succesfully.....')
            return redirect('home')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'Change_Password.html', {'fm': fm})