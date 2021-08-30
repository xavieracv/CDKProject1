

#√√√√√√√√√√
import json
from os import environ
import boto3

#permissions:
#read/write to bank dynamodb table
def handler(event, context):
    #change_userID(event, customer_id , new_id ):
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)
    
    inputs = json.loads( event["pathParameters"]["input"] )
    new_id = inputs["new_id"]
    #first lets check if the new user_ID is available

    available = table.get_item(

        Key = { 'customer_id' : new_id }

    )

    if 'Item' in available:

        Exception("New ID: ",new_id," is already taken.")
        exit

    #this will copy the existing item
    #balance,name,dob,ssn
    customer_id = inputs["customer_id"]
    response = table.get_item(

        Key = { 'customer_id' : customer_id }

    )

    #create new item usiong the same credentials with the new ID
    new_item = {

        'customer_id' : new_id,
        'balance'     : response['Item']['balance'],
        'Name'        : response['Item']['Name'],
        'D.O.B'       : response['Item']['D.O.B'],
        'SSN'         : response['Item']['SSN']

    }
    
    response = table.put_item( 
        Item = new_item ,
        #only add to the table if the attribute does not exist
        ConditionExpression = 'attribute_not_exists( new_id )'
        )

    response = table.delete_item(
            Key = { 'customer_id' : customer_id }
        )
    return response