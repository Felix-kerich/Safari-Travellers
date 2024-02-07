from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import MemberForm, LoginForm
from SafariLinkApp.models import BusesAvailable, Member
from .daraja import mpesa_payment
from django.contrib.auth.decorators import login_required

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
                buses = BusesAvailable.objects.all()
                # user =Member.objects.latest('username')
                user = request.user  # Retrieve the currently logged-in user
                selected_vehicle = request.session.get('selected_vehicle')  # Assuming you stored the selected vehicle in session
                print("User:", user)
                print(f"Successfully logged in as {username}")  # Add debug print
                messages.success(request, f"Successfully logged in as {username}")
                return render(request, 'home.html', {'buses': buses, 'user': user, 'vehicle': selected_vehicle})
                # return HttpResponseRedirect(reverse('home'))
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
        all_buses = BusesAvailable.objects.all()
        return render(request, 'bookingForm.html', {'all_buses': all_buses})

@csrf_exempt  # Add csrf_exempt decorator to your view
def daraja_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        vehicle = request.POST.get('vehicle')
        amount = request.POST.get('amount_paid')
        phone_number = request.POST.get('phoneNo')

        # Assuming mpesa_payment returns a dictionary with a 'success' key indicating success or failure
        response = mpesa_payment(amount, phone_number)

        if response.get('ResponseCode') == '0':
            # Update user's amount_paid field
            user = Member.objects.get(username=username)
            user.vehicle = vehicle
            user.amount_paid = amount
            user.save()

            # Redirect to booking receipt page
            return redirect('home')
        else:
            return JsonResponse(response)

    return render(request, 'daraja.html')



@login_required  # Add login_required decorator to ensure only logged-in users can access this view
def home_view(request):
    # Retrieve the currently logged-in user
    user = request.user

    return render(request, 'home.html', {'user': user})
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
    user = request.user

    return render(request, 'home.html', {'user': user})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))