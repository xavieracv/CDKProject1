# √√√√√√√√√√√√√


import json
import boto3
from os import environ

#permissions:
#special permission policy to call retrieve_account_info and retrieve_account_info
dynamodb = boto3.resource('dynamodb')
table_name = environ.get("TABLE_NAME")
table = dynamodb.Table(table_name)
#moves money from one account to another


def handler(event, context):
    #transfer_balance(event, user_withdraw, user_deposit, amount)

    lambda_client = boto3.client('lambda')

    inputs = json.loads( event["pathParameters"]["input"] )
    user_withdraw = inputs["user_withdraw"]
    user_deposit = inputs["user_deposit"]
    amount = int(inputs["amount"])

#check if balance is sufficient
    response = table.get_item(
        Key  = { 'customer_id' : user_withdraw }
    )
    if 'Item' not in response:
        return Exception("Customer ", user_withdraw," does not exist.")
        
    curr_balance = float(response['Item']["balance"])
    if ( curr_balance < amount ):
        return Exception("Insufficient balance to complete transfer.")


    else:

        #withdraw from user 1's account
        withdraw = table.update_item(
            Key = {
                    'customer_id': user_withdraw,
                },
            UpdateExpression="set balance = balance - :val",
            ExpressionAttributeValues={
                    ':val': amount
                },
            ReturnValues="UPDATED_NEW"
        )
        #deposit into user 2's account

        deposit = table.update_item(

            Key = {
                'customer_id':user_deposit,
            },
            UpdateExpression = 'set balance = balance + :val',
            ExpressionAttributeValues={
                ':val': amount
                },
            ReturnValues = "UPDATED_NEW"
        )

        print("Transfer successful.")
        return True