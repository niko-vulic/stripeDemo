import stripe

def create_price(prod_id, price):
    price = stripe.Price.create(
        product=prod_id,
        unit_amount=price,
        currency='usd',
    )
    return price

if __name__ == '__main__':

    keyFile = open('api_key.txt', 'r')
    stripe.api_key =  keyFile.readline().rstrip()

    desc_bag = 'SmartTrash Bags (10)'
    desc_bin = 'SmartBin'
    prod_bag, prod_bin = None, None
    price_bag, price_bin = None, None

    all_products = stripe.Product.list()

    bag_exists = list(filter(lambda x: x.name == desc_bag, all_products))
    if not(bag_exists):
        print("Creating SmartBags product")
        prod_bag = stripe.Product.create(name=desc_bag)
        price_bag = stripe.Price.create(product=prod_bag.id, unit_amount=2999, currency='usd')
        #, recurring={'interval': 'month'})

    bin_exists = list(filter(lambda x: x.name == desc_bin, all_products))
    if not (bin_exists):
        print("Creating SmartBin product")
        prod_bin = stripe.Product.create(name=desc_bin)
        price_bin = stripe.Price.create(product=prod_bin.id, unit_amount=19999, currency='usd')
        #create_price(prod_bin.id, 19999)






    #prod_bag = create_product('SmartTrash Bags (10)')

    #print("Prod is: " + str(prod_bin))
    #print("Price is: " + str(price_bin))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
