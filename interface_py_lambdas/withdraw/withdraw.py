import json
import boto3
from os import environ


#permissions:
#special permission policy to call retrieve_account_info and retrieve_account_info
#write to dynamo db table

#this function will check if the balance is enough in the user's account, then move the money 
#from the user's account to the teller or cashier account, from which it will be cashed out

def handler(event, context ):
    #withdraw(event, customer_id, amount_withdraw):
    
    inputs = json.loads( event["pathParameters"]["input"] )
    customer_id = inputs["customer_id"]
    amount_withdraw = int(inputs["amount_withdraw"])
    #print("Withdrawing ",amount_withdraw," from user: ",customer_id)
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)

    lambda_client = boto3.client('lambda')

    #check if balance is sufficient
    response = table.get_item(
        Key  = { 'customer_id' : customer_id }
    )
    if 'Item' not in response:
        Exception("Customer ", customer_id," does not exist.")
        exit
    curr_balance = int(response['Item']["balance"])

    if ( curr_balance < amount_withdraw ):
        print("Insufficient balance for withdrawal. Try a smaller amount.")
        exit 

    else:

        input_params = {
            'user_withdraw':customer_id,
            'user_deposit':"Teller",
            'amount' : amount_withdraw
        }

        transfer_to_teller = lambda_client.invoke(
            #arn for transfer_balance lambda
            FunctionName = 'BankProjectStack-fnTransferBalance5434F395-9eAB3w8Pjw5g',
            InvocationType = 'Event',
            Payload = bytes(json.dumps(input_params),encoding="utf-8")
        )

        #this is just a fake way, now value is withdrawn from teller

        response = table.update_item(

            Key={
                    'customer_id': "Teller",
                },
            UpdateExpression="SET balance = balance - :val",
            ExpressionAttributeValues={
                    ':val': amount_withdraw
                },
            ReturnValues="NONE"
        )

        return response
