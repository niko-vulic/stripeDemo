#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe
import apiDemo.stripeDemo
# This is a sample test API key. Sign in to see examples pre-filled with your key.

keyFile = open('../api_key.txt', 'r')
stripe.api_key = keyFile.readline().rstrip()

PRICE_ID_BAG = 'price_1JfR2AIlYoX5Aj60q4rHIjDC'
PRICE_ID_BIN = stripeDemo.queryPrice(19999)

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: replace this with the `price` of the product you want to sell
                    'price': PRICE_ID_BAG,
                    'quantity': 1,
                },
                {
                    'price' : PRICE_ID_BIN,
                    'quantity': 1,
                }
            ],
            payment_method_types=[
              'card',
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)
