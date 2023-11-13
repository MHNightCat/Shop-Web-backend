import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "./sdk/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

order_params = {
    'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
    'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    'PaymentType': 'aio',
    'TotalAmount': 2000, #要改
    'TradeDesc': '訂單測試', #要改
    'ItemName': '商品1#商品2', #要改
    'ReturnURL': 'https://www.ecpay.com.tw/return_url.php', #要改
    'ChoosePayment': 'ALL',
    'ClientBackURL': 'https://www.ecpay.com.tw/client_back_url.php',
    'ItemURL': 'https://www.ecpay.com.tw/item_url.php', #要改
    'Remark': '交易備註', #要改
    'OrderResultURL': 'https://www.ecpay.com.tw/order_result_url.php', #要改
    'NeedExtraPaidInfo': 'Y', #要改
    'EncryptType': 1,
}

extend_params_1 = {
    'ExpireDate': 7,
    'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
    'ClientRedirectURL': '',
}

extend_params_2 = {
    'StoreExpireDate': 15,
    'Desc_1': '',
    'Desc_2': '',
    'Desc_3': '',
    'Desc_4': '',
    'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
    'ClientRedirectURL': '',
}

extend_params_3 = {
    'BindingCard': 0,
    'MerchantMemberID': '',
}

extend_params_4 = {
    'Redeem': 'N',
    'UnionPay': 0,
}

# 建立實體
ecpay_payment_sdk = module.ECPayPaymentSdk(
    MerchantID='2000132',
    HashKey='5294y06JbISpM5x9',
    HashIV='v77hoKGq4kWxNNIS'
)

# 合併延伸參數
order_params.update(extend_params_1)
order_params.update(extend_params_2)
order_params.update(extend_params_3)
order_params.update(extend_params_4)

try:
    # 產生綠界訂單所需參數
    final_order_params = ecpay_payment_sdk.create_order(order_params)

    # 產生 html 的 form 格式
    action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
    # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
    print(final_order_params)
    html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
    print(html)
except Exception as error:
    print('An exception happened: ' + str(error))