# √√√√√√√√√√√√√


import json
import boto3
from os import environ
#permissions:
#write to dynamo db bank table

#will be called when the user withdraws money, to increase balance through deposit
# the balance_change must be a positive number, to decrease it must be negative

def handler(event, context ):
    #deposit(event, customer_id , amount )
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)
    
    inputs = json.loads( event["pathParameters"]["input"] )
    customer_id = inputs["customer_id"]
    amount = int(inputs["amount"])

    response = table.update_item(

        Key={
                'customer_id': customer_id,
            },
        UpdateExpression="set balance = balance + :val",
        ExpressionAttributeValues={
                ':val': amount
            },
        ReturnValues = "UPDATED_NEW"
    )

    return response