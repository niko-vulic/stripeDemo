import stripe

keyFile = open('api_key.txt', 'r')
stripe.api_key = keyFile.readline().rstrip()

emailFile = open('email.txt', 'r')
EMAIL = emailFile.readline().rstrip()

BAG_DESC = 'SmartTrash Bags (10)'
BAG_PRICE = 2999
BAG_IMG = 'https://i.imgur.com/bJLvY3H.png'

BIN_DESC = 'SmartBin'
BIN_PRICE = 19999
BIN_IMG = 'https://i.imgur.com/dnu8gbl.png'

BAG_DESC_RECUR = 'SmartTrash Subscription'
BAG_PRICE_RECUR = 1499


def get_product_and_price(input_desc, input_price, input_img, force_new=False, is_recurring=False):
    print("Product {prod} and price {price} setup".format(prod=input_desc, price=input_price))
    item_prod, item_price = None, None
    all_products = stripe.Product.list()
    all_prices = stripe.Price.list()

    item_exists = list(filter(lambda x: x.name == input_desc, all_products))
    if force_new or not item_exists:
        print("--Creating {desc} product via API".format(desc=input_desc))
        if input_img:
            item_prod = stripe.Product.create(name=input_desc, images=[input_img])
        else:
            item_prod = stripe.Product.create(name=input_desc)
    else:
        print("--Product already exists, retrieved from list API")
        item_prod = item_exists[0]

    price_exists = list(filter(lambda x: x.unit_amount == input_price, all_prices))
    if force_new or not price_exists:
        print("--Creating {desc} price via API".format(desc=input_price))
        if not is_recurring:
            item_price = stripe.Price.create(product=item_prod.id, unit_amount=input_price, currency='usd')
        else:
            item_price = stripe.Price.create(product=item_prod.id, unit_amount=input_price, currency='usd', recurring={'interval': 'month'})
    else:
        print("--Price already exists, retrieved from list API")
        item_price = price_exists[0]

    print("--Product ID:" + str(item_prod.id) + ", price ID:" + str(item_price.id))
    return item_prod, item_price


def query_price(input_price):
        item_price = None
        all_prices = stripe.Price.list()
        price_exists = list(filter(lambda x: x.unit_amount == input_price, all_prices))

        if price_exists:
            item_price = price_exists[0]

        return item_price

# Hardcoded customer creation
def cust_setup():
    customerA = stripe.Customer.create(name='Niko', email=EMAIL, description='First Client')
    customerB = stripe.Customer.create(name='Adam', email=EMAIL, description='Nextdoor Neighbor')
    customerC = stripe.Customer.create(name='Bani', email=EMAIL, description='Spouse')

    customers = [customerA, customerB, customerC]
    print("Customers created:" + str([cust.id for cust in customers]))
    return customers


def send_invoice(customers, invoice_items):
    invoiceList = []

    for cust in customers:
        for item in invoice_items:
            stripe.InvoiceItem.create(customer=cust.id, price=item.id)
        invoice = stripe.Invoice.create(customer=cust.id, auto_advance=True)
        print("Invoice {inv} sent for customer {cust}".format(inv=invoice.id, cust=cust.id))
        invoiceList.append(invoice)

    return invoiceList


def setup_subscription(customer_id, price_id):
    sub = stripe.Subscription.create(customer=customer_id, items=[{'price': price_id}], payment_behavior="default_incomplete")
    print("Subscription {sub} setup for customer {cust}".format(sub=sub.id, cust=customer_id))


def complete_setup(force_new=False):
    # Returns item_prod, item_price
    bin = get_product_and_price(BIN_DESC, BIN_PRICE, BIN_IMG, force_new)
    bag = get_product_and_price(BAG_DESC, BAG_PRICE, BAG_IMG, force_new)
    ongoing_sub = get_product_and_price(BAG_DESC_RECUR, BAG_PRICE_RECUR, None, force_new, True)

    # Setup customers from hard-coded dummy data
    customers = cust_setup()

    # Setup the items for the first invoice and send to all customers
    first_invoice_items = [bin[1], bag[1]]
    invoices = send_invoice(customers, first_invoice_items)

    # Manually create any subscriptions via:
    # setup_subscription('cus_KJiN8uwPz7XFYP', 'price_1Jf4qpIlYoX5Aj60jJMvNUna')


if __name__ == '__main__':
    pass
