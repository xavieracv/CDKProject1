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
    
    all_items = table.scan()
    users = []

    for i in all_items["Items"]:
        users.append(i["customer_id"])
    
    return users
