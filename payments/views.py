# import stripe.api_resources
# from requests import Response
#
# from rest_framework.decorators import api_view
#
# stripe.api_key = "sk_test_51HrzKyG1Bl4N34TFcw02kWTmjSRvscHTulw3NhAjXgqK5dfwLtyOoOBLatBLRhsNT1uJFoZYJid0kzzusxczvO7u00qKYCWb4R"
#
#
# @api_view(['POST'])
# def test_payment(request):
#
#     test_payment_intent = stripe.PaymentIntent.create(
#     amount=1000, currency='pln',
#     payment_method_types=['card'],receipt_email='test@example.com')
#     return Response(status_code)