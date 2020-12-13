import stripe

stripe.api_key = 'sk_test_51HrzKyG1Bl4N34TFcw02kWTmjSRvscHTulw3NhAjXgqK5dfwLtyOoOBLatBLRhsNT1uJFoZYJid0kzzusxczvO7u00qKYCWb4R'

stripe.PaymentIntent.create(
          amount=1000,
            currency='usd',
              payment_method_types=['card'],
                receipt_email='jenny.rosen@example.com',
                )

