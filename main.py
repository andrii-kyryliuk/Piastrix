import datetime
from urllib.parse import urlencode
from os import getenv
from flask import Flask, redirect, request, render_template
from tools.piastrixlib import PiastrixClient, PiastrixClientException
from tools.utils import Currency
from tools.loggers import PAYMENT_INFO_LOGGER
from tools.reporter import send_me_report


app = Flask(__name__)

SHOP_ID = getenv("SHOP_ID")
MARKET_SECRET_KEY = getenv("MARKET_SECRET_KEY")
RUB_PAY_WAYS = [
    "payeer_rub",
    "advcash_rub"
]


@app.route('/', methods=['GET'])
def index():
    send_me_report(f'app was opened from {request.remote_addr}')
    return render_template(template_name_or_list='index.html', currency=Currency)


@app.route('/make_payment/', methods=['POST'])
def payment_handler():
    data, response = {}, redirect('/')

    currency = request.form.get("currency")
    amount = request.form.get("amount")
    order_id = datetime.datetime.utcnow().isoformat()
    extra_fields = {
        "description": request.form.get("description")
    }
    client = PiastrixClient(shop_id=SHOP_ID, secret_key=MARKET_SECRET_KEY)

    if currency == Currency.EUR:
        data, url = client.pay(amount, currency, order_id, extra_fields)
        response = redirect(f"{url}?{urlencode(data)}")

    elif currency == Currency.USD:
        data = client.bill(currency, amount, currency, order_id, extra_fields)
        response = redirect(data.get("url"))

    else:
        for pay_way in RUB_PAY_WAYS:
            try:
                data = client.invoice(amount, currency, order_id, pay_way, extra_fields)
                response = render_template('invoice_form.html',
                                           method=data.get('method'),
                                           url=data.get('url'),
                                           params=data.get('data').items())
                break
            except PiastrixClientException as exc:
                data = {"message": exc, "error_code": exc.error_code}

    PAYMENT_INFO_LOGGER.info(f"{data}")
    return response


if __name__ == "__main__":
    app.run()
