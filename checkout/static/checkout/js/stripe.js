/* 
The code below has been copied from:
https://github.com/ckz8780/boutique_ado_v1/blob/master/checkout/static/checkout/js/stripe_elements.js
Minor changes have been made to the code.
*/

let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();
let style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
let card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
let form = document.getElementById('form-checkout');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#form-checkout-submit').attr('disabled', true);

    // From using {% csrf_token %} in the form
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let data = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
    };
    let url = '/checkout/modify_stripe_data/';
    $.post(url, data).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.first_name.value.concat(' ', form.last_name.value)),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.address.value),
                        line2: null,
                        city: $.trim(form.city.value),
                        country: $.trim(form.country.value),
                        state: null,
                    }
                }
            },
            shipping: {
                name: $.trim(form.first_name.value.concat(' ', form.last_name.value)),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address.value),
                    line2: null,
                    city: $.trim(form.city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: null,
                }
            },
        }).then(function (result) {
            if (result.error) {
                let errorDiv = document.getElementById('card-errors');
                let html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({
                    'disabled': false
                });
                $('#form-checkout-submit').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // Just reload the page, the error will be in django messages
        location.reload();
    });
});