import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializer import SessionSerializer
import requests
from django.shortcuts import redirect

SSLCZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'


# SSLCZ_SESSION_API = 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'

@api_view(['POST'])
def get_ssl_session(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        post_data = {
            "store_id": os.environ.get('STORE_ID'),
            "store_passwd": os.environ.get('STORE_PASS'),
            "total_amount": data['total_amount'],
            "currency": "BDT",
            "tran_id": data["transId"],
            "success_url": data['successUrl'],
            "fail_url": data['failUrl'],
            "cancel_url": data['cancelUrl'],
            "ipn_url": data['ipnUrl'],
            "cus_name": data['name'],
            "cus_email": data['email'],
            "cus_add1": data['address'],
            "cus_add2": data['address'],
            "cus_city": data['city'],
            "cus_state": data['city'],
            "cus_postcode": data['postalCode'],
            "cus_country": data['country'],
            "cus_phone": data['phone'],
            "cus_fax": data['phone'],
            "ship_name": data['name'],
            "ship_add1": data['address'],
            "ship_add2": data['address'],
            "ship_city": data['city'],
            "ship_state": data['city'],
            "ship_postcode": data["postalCode"],
            "ship_country": data['country'],
            "multi_card_name": "mastercard,visacard,amexcard",
            "value_a": "ref001_A",
            "value_b": "ref002_B",
            "value_c": "ref003_C",
            "value_d": "ref004_D",
            "shipping_method": "YES",
            "product_name": "credit",
            "product_category": "general",
            "product_profile": "general"
        }

        response = requests.post(SSLCZ_SESSION_API, post_data)

        if response.status_code == 200:
            print(response)
            session_key = response.json().get("sessionkey")
            gateway_url = response.json().get("GatewayPageURL")
            return Response({"session": session_key, "gatewayPageUrl": gateway_url})

        else:
            return Response({"error": "Failed to create session"}, status=response.status_code)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def success(request):
    data = request.data
    print("____success___")
    print(data)
    return redirect('http://localhost:5173/payment/success')


@api_view(['POST'])
def fail(request):
    data = request.data
    print("____fail___")
    print(data)
    return redirect('http://localhost:5173/payment/fail')


@api_view(['POST'])
def cancel(request):
    data = request.data
    print("____cancel___")
    print(data)
    return redirect('http://localhost:5173/payment/cancel')
