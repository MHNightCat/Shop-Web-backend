def individual_products(product) -> dict:
    return {
        'mongodb_id': str(product['_id']),
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'describe': product['describe'],
        'category': product['category'],
        'image': product['image'],
        'plural_options': product['plural_options'],
        'remaining': product['remaining'],
        'payment': product['payment'],
        'transport': product['trasport'],
        'sell': product['sell'],
        'updateAt': product['updateAt'],
    }


def list_products(products) -> list:
    return[individual_products(product) for product in products]
