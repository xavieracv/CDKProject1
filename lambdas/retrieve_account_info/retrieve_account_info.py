# √√√√√√√√√√√√√


import json
import boto3
from os import environ
#this will return the value for a certain column int he dynamodb table
def handler(event, context ):
    #retreive_account_info(event, customer_id )
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)
    
    inputs = json.loads( event["pathParameters"]["input"] )
    customer_id = inputs["customer_id"]

    response = table.get_item(
        
        Key = { 'customer_id' : customer_id },

        )

    if 'Item' not in response:
        Exception("Customer ", customer_id ," does not exist.")
        exit
    
    detail = response['Item']

    return detail