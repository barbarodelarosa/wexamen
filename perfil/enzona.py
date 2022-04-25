
import json
from os import access, name
from wexamen import settings
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_connect():
    # import requests
    headers = {
        'Authorization': 'Basic %s' %(settings.KEY_ACCESS_TOKEN,),
        # 'Authorization': f'Basic {settings.KEY_ACCESS_TOKEN}',
    }
    data = {
        'grant_type': 'password',
        'username': 'brosa17',
        # 'username': str(settings.CONSUMER_USER),
        # 'password': str(settings.CONSUMER_PASSWORD),
        'password': 'Barva2021',
        'scope':'enzona_business_payment'
    }
    try:
        response = requests.post('https://api.enzona.net/token', headers=headers, data=data, verify=False)
        print("RESPONSE HEADER")
        print(response)
        return response
    except:
        return "Error al conectarse con ENZONA"

def get_header_bearer_token():
    connect = test_connect()
   
    if connect.status_code == 200:
        connect_json = connect.json()
        access_token = connect_json['access_token']
        headers = {
            'accept'       : 'application/json',
            'Content-Type' : 'application/json',
            'Authorization': 'Bearer %s' %(access_token),
        }
        return headers

def payment_orders(description="", currency="CUP", amount=0, merchant_op_id=0000000000):
    """Function for create pay order"""
    headers = get_header_bearer_token()
       
    url = f'{settings.URL_API_ENZONA}/payment-orders'
   
    json_data =  {
        "description": description,
        "currency": currency,
        "amount": amount,
        "merchant_op_id": merchant_op_id

    }
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)
    
    return response


def payments_store(funding_source_uuid="", description="", currency="", payment_password="", amount=0, total=0, items=[],):
    """Function for pay a product, Add product in items """
    headers = get_header_bearer_token()
    
    
    url = f'{settings.URL_API_ENZONA}/payments/store'
    print(url)
    json_data = {
        "funding_source_uuid": "string",
        "description": "string",
        "currency": "string",
        "payment_password": "string",
        "amount": {
            "total": 0.05
        },
        "items": [
        {
            "vendor_identity_code": "string",
            "product_id": "string",
            "quantity": 1,
            "price": 0.03
        }
        ]
    }
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)
    
    return response


    

############################################################################
def post_payments(description="",  currency="CUP", amount={}, merchant_op_id=123456789123,
    invoice_number=1212, return_url="https://mymerchant.cu/return", cancel_url="https://mymerchant.cu/return", terminal_id=12121, items=[{}], buyer_identity_code="" ):
    """Function for create pay"""
    headers = get_header_bearer_token()
    

    url = f'{settings.URL_API_ENZONA}/payments'
  
    
    json_data = {
        "description": "",
        "currency": "",
        "amount": {
            "total": "1.00",
            "details": {
            "shipping": "0.00",
            "tax": "0.00",
            "discount": "0.00",
            "tip": "0.00"
            }
        },
        "items":   [{
                'name': 'Prueba',
                'description': 'Prueba de producto',
                'quantity': 1,
                'price': '1.00',
                'tax': '0.00'
            }],
        "merchant_op_id": 123456789123,
        "invoice_number": 1212,
        "return_url": "http://127.0.0.1:8000/",
        "cancel_url": "http://127.0.0.1:8000/",
        "terminal_id": 12121,
        "buyer_identity_code": ""
        }


    json_data['description']=description
    json_data['currency']=currency
    json_data['amount']=amount #OK
    json_data['items']=items
    json_data['merchant_op_id']=merchant_op_id
    json_data['invoice_number']=invoice_number
    json_data['return_url']=return_url
    json_data['cancel_url']=cancel_url
    json_data['terminal_id']=terminal_id
    json_data['buyer_identity_code']=buyer_identity_code


    print("json_data**************")

    print(json_data)
    print("headers**************")

    print(headers)
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)

    return response

###############################################################################

def get_payments(merchant_uuid="",limit="",offset="",merchant_op_filter="",status_filter="",start_date_filter="",end_date_filter="",order_filter=""):
    """Funcion para obtener un lista de pagos"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments'
    print(url)
    params = {
        'merchant_uuid':merchant_uuid,
        'limit':limit,
        'offset':offset,
        'merchant_op_filter':merchant_op_filter,
        'status_filter':status_filter,
        'start_date_filter':start_date_filter,
        'end_date_filter':end_date_filter,
        'order_filter':order_filter,
    }
    response = requests.get(url=url, headers=headers, params=params, verify=False)
    print(response)
    print(headers)
    return response

##################################################################################

def get_payment_by_uuid(transaction_uuid):
    """Funcion para obtener los detalles de un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}'
  
    
    response = requests.get(url=url, headers=headers, verify=False)
   
    return response

###################################################################################

def payment_complete(transaction_uuid):
    """Funcion para completar un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/complete'
   
    response = requests.post(url=url, headers=headers, verify=False)

    return response

#####################################################################################

def payment_cancel(transaction_uuid):
    """Funcion para cancelar un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/cancel'
   
    
    response = requests.post(url=url, headers=headers, verify=False)

    return response

#########################################################################################

def payment_checkout(uuid):
    """Funcion para chequear un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/checkout/{uuid}'

    
    response = requests.get(url=url, headers=headers, verify=False)

    return response

########################################################################################

def payment_confirm(transaction_uuid, payment_password, funding_source_uuid):
    """Funcion para confirmar un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/confirm'
    json_data = {
        "payment_password": payment_password,
        "funding_source_uuid": funding_source_uuid
    }

    
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)
 
    return response


##########################################################################################

def payment_refund(transaction_uuid, total, description):
    """Funcion para cancelar un pago"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/refund'
    payload = {
        "amount": {
            "total": total
        },
        "description": description
    }

    
    response = requests.post(url=url, headers=headers, json=payload, verify=False)
  
    return response

###################################################################################
def get_payment_refund(transaction_uuid):
    """ Obtine los detalles de una devolucion realizada"""
    headers = get_header_bearer_token()

    url = f'{settings.URL_API_ENZONA}/payments/refund/{transaction_uuid}'
   
    
    response = requests.get(url=url, headers=headers, verify=False)
 
    return response

########################################################################################

def get_list_payments_refunds(merchant_uuid="",limit="",offset="",status_filter="",start_date_filter="",end_date_filter="",order_filter=""):
    """ Obtine las devoluciones realizadas """
    headers = get_header_bearer_token()
    params ={
        'merchant_uuid':merchant_uuid,
        'limit':limit,
        'offset':offset,
        'status_filter':status_filter,
        'start_date_filter':start_date_filter,
        'end_date_filter':end_date_filter,
        'order_filter':order_filter,
    }
    url = f'{settings.URL_API_ENZONA}/payments/refunds'
 
    
    response = requests.get(url=url, headers=headers, params=params, verify=False)
  
    return response

#########################################################################################

def get_detail_payments_refunds(transaction_uuid, limit="", offset="", status_filter="",start_date_filter="",end_date_filter="",order_filter=""):
    """ Obtine la lista de devoluciones realizadas a un pago"""
    headers = get_header_bearer_token()
    params ={
        'transaction_uuid':transaction_uuid,
        'limit':limit,
        'offset':offset,
        'status_filter':status_filter,
        'start_date_filter':start_date_filter,
        'end_date_filter':end_date_filter,
        'order_filter':order_filter,
    }
    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/refunds'
   

    
    response = requests.get(url=url, headers=headers, params=params, verify=False)
   
    return response

#########################################################################################

def payments_recive_code(funding_source_uuid,amount,vendor_identity_code,description,currency,payment_password):
    """ Permite crear un codigo de recivo """
    headers = get_header_bearer_token()
    json_data ={
        "funding_source_uuid":funding_source_uuid,
        "amount":amount,
        "vendor_identity_code":vendor_identity_code,
        "description":description,
        "currency":currency,
        "payment_password":payment_password,
    }
    url = f'{settings.URL_API_ENZONA}/payments/vendor/code'
  
    
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)
 
    return response


#################################################################################
"""



=======================================================================
https://apisandbox.enzona.net/payment/v1.0.0/ #POST Permite pagar un producto

payload = {
  "funding_source_uuid": "string",
  "description": "string",
  "currency": "string",
  "payment_password": "string",
  "amount": {
    "total": 0.05
  },
  "items": [
    {
      "vendor_identity_code": "string",
      "product_id": "string",
      "quantity": 1,
      "price": 0.03
    }
  ]
}

codes
200 = "Pago creado correctamente."
{
  "status": "string",
  "mensaje": "string"
}
400 = "Sintaxis inválida en la petición."
401 = "No autenticado."

=========================================================================

=========================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments #POST Permite crear un pago

payload = {
  "description": "string",
  "currency": "CUP",
  "amount": {
    "total": "4.00",
    "details": {
      "shipping": "1.00",
      "tax": "0.00",
      "discount": "0.00",
      "tip": "0.00"
    }
  },
  "items": [
    {
      "name": "string",
      "description": "string",
      "quantity": 1,
      "price": "3.00",
      "tax": "0.00"
    }
  ],
  "merchant_op_id": 123456789123,
  "invoice_number": 1212,
  "return_url": "https://mymerchant.cu/return",
  "cancel_url": "https://mymerchant.cu/cancel",
  "terminal_id": 12121,
  "buyer_identity_code": ""
}
===================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments #GET Obtiene un listado de pagos realizados
params =
merchant_uuid
limit
offset
merchant_op_filter
status_filter
start_date_filter
end_date_filter
order_filter
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/asdasdasdsadsds #GET Obtienes los Detalles de un pago realizado
params =
transaction_uuid    #*required
===================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/assdsdsdssddsds/complete #POST Permite completar un pago
params =
transaction_uuid    #*required
payload = {}
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/asdasdsds/cancel #POST Permite cancelar un pago
params =
transaction_uuid    #*required
payload = {}
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/checkout/assdsds #GET Permite realizar el checkout de un pago
params =
uuid   #*required
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/asdasasa/confirm #POST Permite confirmar un pago
params =
transaction_uuid   #*required
payload = {
  "payment_password": "string",
  "funding_source_uuid": "string"
}
=======================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/saf%20sdfsdfddf/refund #POST Permite Realizar la Devolucion de un pago
params =
transaction_uuid    #*required
payload = {
  "amount": {
    "total": "string"
  },
  "description": "string"
}
=====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/refund/%3Cazsxsasdasd #GET Permite obtener los detalles de una devolucion realizada
params =
transaction_uuid     #*required
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/refunds #GET Obtine una lista de devoluciones realizadas
params =
merchant_uuid
limit
offset
status_filter
start_date_filter
end_date_filter
order_filter
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/asdasdasdsds/refunds #GET Obtine una lista de devoluciones de un pago
params =
transaction_uuid      #*required
limit
offset
status_filter
start_date_filter
end_date_filter
order_filter
====================================================================
https://apisandbox.enzona.net/payment/v1.0.0/payments/vendor/code #POST Permite crear un recieve code (Codigo de recibo)
payload = {
  "funding_source_uuid": "string",
  "amount": "string",
  "vendor_identity_code": "string",
  "description": "string",
  "currency": "string",
  "payment_password": "string"
}
"""




def confirm_payment_orders(transaction_uuid):
    """Confirmar y completar pagor"""
    headers = get_header_bearer_token()
       
    url = f'{settings.URL_API_ENZONA}/payments/{transaction_uuid}/complete'
   
    json_data =  {}
    response = requests.post(url=url, headers=headers, json=json_data, verify=False)
    print("response.json()   PYMENTS COMPLETE")
    print(response)
    return response