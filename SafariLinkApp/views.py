from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import MemberForm, LoginForm
from SafariLinkApp.models import BusesAvailable, Member
from .daraja import mpesa_payment


def SafariLinkApp(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())
def index_view(request):
    return render(request, 'index.html')
def dashboard_view(request):
    all_buses = BusesAvailable.objects.all()
    return render(request, 'dashboard.html',{'all_buses': all_buses})


def register_view(request):
    if request.method == 'POST':
        form = MemberForm(request.POST or None)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
            messages.error(request, "username taken. Please")
            return render(request, 'registrationForm.html', {'form':form , 'error_message': 'username taken. Please'})
    else:
        form = MemberForm()
        return render(request, 'registrationForm.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            member = Member.objects.filter(username=username, password=password).first()

            if member is not None:
                # Log in the user
                login(request, member)
                return HttpResponseRedirect(reverse('home'))
            else:
                print("Invalid username or password")
                messages.error(request, "Invalid username or password")
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
        else:

            print(form.errors)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
def book_view(request):
           return render(request,'bookingForm.html')
def daraja_view(request):
    buses = BusesAvailable.objects.all()
    user = request.user  # Retrieve the currently logged-in user
    selected_vehicle = request.session.get('selected_vehicle')  # Assuming you stored the selected vehicle in session

    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phoneNo')

        # Perform M-Pesa payment
        response = mpesa_payment(amount, phone_number)

        # You can use the retrieved data (username, email) for further processing if needed
        return JsonResponse(response)
        print(response)
        return render(request, 'home.html', {'buses': buses, 'user': user, 'vehicle': selected_vehicle, 'response_data': response})



    # Handle GET requests if needed
    return render(request, 'daraja.html')
def home_view(request):
    buses = BusesAvailable.objects.all()
    user = Member.objects.latest('username')  # Retrieve the latest user
    selected_vehicle = request.session.get('selected_vehicle')  # Assuming you stored the selected vehicle in session
    return render(request, 'home.html', {'buses': buses, 'user': user, 'vehicle': selected_vehicle})

def book_vehicle(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('booking_receipt'))
    else:
        form = MemberForm()
    return render(request, 'book_vehicle.html', {'form': form})

def booking_receipt(request):
    if request.method == 'POST':

        pass
    else:

        user = Member.objects.latest('id')
        selected_vehicle = request.POST.get('vehicle', 'Not Selected')
        return render(request, 'home.html', {'user': user, 'vehicle': selected_vehicle})

