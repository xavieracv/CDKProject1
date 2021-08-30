



#√√√√√√√√√√√√
import json
import boto3
from os import environ

#permissions:
#read/write to lambda db table
def handler( event ,  context):
    #remove_account( event ,  customer_id)
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)
    
    print("event pathParameters input: ",event["pathParameters"]["input"])
    inputs = json.loads(  event["pathParameters"]["input"]  )
    customer_id = inputs["customer_id"]

    response = table.get_item(
        Key = { 'customer_id' : customer_id }
        )

    if 'Item' not in response:
        return Exception("Account does not exist.")
        exit
    else:

        if float(response["Item"]["balance"]) > 0.0 :
            return Exception("Remove all user funds before terminating account.")
        
        else:
            response = table.delete_item(
                Key = { 'customer_id' : customer_id }
            )
            return "Success. Account tied to user ", customer_id ," has been removed."
