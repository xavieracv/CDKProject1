# √√√√√√√√√√√√√

import json
import boto3
from os import environ
#this will return the value for a certain column int he dynamodb table
def handler(event, context):
    #retreive_account_detail(event, customer_id , required_info)
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)
    
    inputs = json.loads( event["pathParameters"]["input"] )
    detail = inputs["required_info"]
    id = inputs["customer_id"]
    
    response = table.get_item(
    
        Key  = { 'customer_id' : id },

    )

    if 'Item' not in response:
        return Exception("Customer ", id ," does not exist.")
        exit
    
    detail = response['Item'][detail]
    #print(detail)
    return detail
