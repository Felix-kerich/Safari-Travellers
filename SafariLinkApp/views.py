import json
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import MemberForm, LoginForm
from SafariLinkApp.models import BusesAvailable, Member, Notifications, MpesaTransaction
from .daraja import mpesa_payment

def safariLinkApp(request):
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
            messages.success(request,'Registered Successfully you can now login')
            return render(request, 'login.html', {'form': form, 'success_message': 'Registered Successfully you can now login'})
            # return HttpResponseRedirect(reverse('login'))
        else:
            print(form.errors)
            messages.error(request, "username taken. Please")
            return render(request, 'registrationForm.html', {'form':form , 'error_message': 'username taken. Please'})
    else:
        form = MemberForm()
        return render(request, 'registrationForm.html', {'form': form})
@csrf_exempt
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
                print("User:", user)
                print(f"Successfully logged in as {username}")  # Add debug print
                messages.success(request, f"Successfully logged in as {username}")
                return render(request, 'home.html', {'buses': buses, 'user': user})
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


# @login_required  # Add login_required decorator to ensure only logged-in users can access this view
def home_view(request):
    # Retrieve the currently logged-in user
    user = request.user

    return render(request, 'home.html', {'user': user})
def book_view(request):
        all_buses = BusesAvailable.objects.all()
        return render(request, 'bookingForm.html', {'all_buses': all_buses})

@csrf_exempt
def daraja_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        vehicle = request.POST.get('vehicle')
        amount = request.POST.get('amount_paid')
        phone_number = request.POST.get('phoneNo')

        response = mpesa_payment(amount, phone_number)

        if response.get('ResponseCode') == '0':
            # Update user's amount_paid field
            user = Member.objects.get(username=username)
            user.vehicle = vehicle
            user.amount_paid = amount
            user.save()

            # return JsonResponse(response)

            messages.success(request, f"{ username } your payment is being verified")
            # return render(request, 'home.html')
            # return HttpResponseRedirect(login_view)
            return HttpResponseRedirect(reverse('home'))
        else:
            return JsonResponse(response)

    return render(request, 'daraja.html')


def booking_receipt(request):
    user = request.user

    return render(request, 'home.html', {'user': user})
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def contact_view(request):
    return render(request, 'contact.html')
def notifications_view(request):
    notifications = Notifications.objects.all()
    return render(request, 'notifications.html', {'notifications' : notifications} )
def e_citizen_view(request):
    return render(request,'e-citizen.html')

@csrf_exempt
def callback_view(request):
    if request.method == 'POST':  # Change to POST method
        # Get the raw request body
        stk_callback_response = request.body.decode('utf-8')

        log_file = "Mpesastkresponse.json"
        with open(log_file, "a") as log:
            log.write(stk_callback_response)

        data = json.loads(stk_callback_response)

        # Extract relevant information
        merchant_request_id = data.get('Body', {}).get('stkCallback', {}).get('MerchantRequestID')
        checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        amount = float(
            data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[0].get('Value'))
        transaction_id = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[1].get(
            'Value')
        user_phone_number = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])[
            4].get('Value')

        # Check if the transaction was successful
        if result_code == 0:  # Change to integer comparison
            # Store the transaction details in the database
            MpesaTransaction.objects.create(
                MerchantRequestID=merchant_request_id,
                CheckoutRequestID=checkout_request_id,
                ResultCode=result_code,
                Amount=amount,
                MpesaReceiptNumber=transaction_id,
                PhoneNumber=user_phone_number

            )

            return JsonResponse({'message': 'Transaction successful'})

    return JsonResponse({'error': 'Method not allowed'})
