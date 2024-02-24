import base64
from datetime import datetime

import requests

from requests.auth import HTTPBasicAuth


def mpesa_payment(amount, phone_number):
    # Safaricom Developer Portal Credentials
    consumer_key = 'IWw4FAjmtDGWWwUzFWSLIPUtLyZhsYxmPC8TdbvZC2QAGraY'
    consumer_secret = 'YJw6GASORyg5ytGo3FAUQUiGlLV458Z23kGBNA2tOrdXjXZ0wuVcJGXdVn23A7Bq'

    # M-Pesa Shortcode and Passkey
    shortcode = '174379'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    # API Endpoints
    access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    payment_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    # Get access token
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    try:
        response.raise_for_status()
        access_token = response.json()['access_token']
    except requests.exceptions.HTTPError as err:
        print(f"Error obtaining access token: {err}")
        return {"error": "Access token retrieval failed"}

    # Format phone number in international format
    international_phone_number = phone_number

    # Calculate Lipa Na M-Pesa Online password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    lipa_na_mpesa_online_password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode('utf-8')

    # Prepare STK push request payload
    payload = {
        "BusinessShortCode": shortcode,
        "Password": lipa_na_mpesa_online_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": international_phone_number,
        "PartyB": shortcode,
        "PhoneNumber": international_phone_number,
        "CallBackURL": "https://389e-102-215-32-244.ngrok-free.app/callback/",
        "AccountReference": "SafariLink Travellers",
        "TransactionDesc": "Payment of X"
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Send STK push request
    response = requests.post(payment_url, json=payload, headers=headers)

    return response.json()
