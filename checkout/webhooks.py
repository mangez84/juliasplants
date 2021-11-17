import json
import time
from django.conf import settings
from django.db import DatabaseError
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import stripe
from plants.models import Plant
from profiles.models import UserProfile
from .models import Order, OrderItem


class StripeWebhookHandler:
    """
    Handle Stripe webhooks.
    Code was copied from:
    https://github.com/ckz8780/boutique_ado_v1/tree/master/checkout
    Minor changes have been made to the code.
    """

    def __init__(self, request):
        self.request = request

    @staticmethod
    def _send_confirmation_email(order):
        """Send the user a confirmation email."""
        cust_email = order.email
        subject = render_to_string(
            'checkout/emails/confirmation_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/emails/confirmation_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    @staticmethod
    def handle_event(event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook recieved: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        stripe_pid = intent.id
        cart = intent.metadata.cart
        billing_details = intent.charges.data[0].billing_details

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=stripe_pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook recieved: {event["type"]} | '
                    f'SUCCESS: Verified order already in database.'
                ),
                status=200
            )

        try:
            profile = UserProfile.objects.get(
                user__username=intent.metadata.user)
        except UserProfile.DoesNotExist:
            profile = None

        order = None
        try:
            order = Order.objects.create(
                first_name=billing_details.name.split(' ')[0],
                last_name=billing_details.name.split(' ')[1],
                email=billing_details.email,
                address=billing_details.address.line1,
                city=billing_details.address.city,
                postcode=billing_details.address.postal_code,
                country=billing_details.address.country,
                phone_number=billing_details.phone,
                total_cost=intent.metadata.total_cost,
                stripe_pid=stripe_pid,
                profile=profile,
            )
            for cart_item in json.loads(cart):
                plant = Plant.objects.get(id=cart_item['plant'])
                order_item = OrderItem(
                    order=order,
                    plant=plant,
                    quantity=cart_item['quantity'],
                    total=cart_item['total'],
                )
                order_item.save()
        except DatabaseError as error:
            if order:
                order.delete()
            return HttpResponse(
                content=(
                    f'Webhook recieved: {event["type"]} | ERROR {error}.'
                ),
                status=500
            )
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook recieved: {event["type"]} | '
                f'SUCCESS: Created order in webhook.'
            ),
            status=200)

    @staticmethod
    def handle_payment_intent_payment_failed(event):
        """Handle the payment_intent.payment_failed webhook from Stripe."""
        return HttpResponse(
            content=f'Webhook recieved: {event["type"]}',
            status=200
        )


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listen for webhooks from Stripe.
    Code was copied from:
    https://github.com/ckz8780/boutique_ado_v1/tree/master/checkout
    Minor changes have been made to the code.
    """
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret)
    except ValueError as error:
        # Invalid payload
        return HttpResponse(content=error, status=400)
    except stripe.error.SignatureVerificationError as error:
        # Invalid signature
        return HttpResponse(content=error, status=400)
    except stripe.error.StripeError as error:
        return HttpResponse(content=error, status=400)

    # Set up a webhook handler
    handler = StripeWebhookHandler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
