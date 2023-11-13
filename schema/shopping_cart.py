def individual_shopping_cart_iteam(product) -> dict:
    return {
            'mongodb_id': str(product['_id']),
            'id': product['id'],
            'sub': product['sub'],
            'iteam_id': product['iteam_id'],
            'amount': product['amount'],
    }
    
def list_shopping_cart_iteam(iteams) -> list:
    return[individual_shopping_cart_iteam(iteam) for iteam in iteams]