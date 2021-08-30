

#√√√√√√√√√√
import json
from threading import Condition
import boto3
from os import environ

#permissions:
#read/write to lambdaDB table

def handler(event, context):
    #create_account(event,customer_id,initial_balance,full_legal_name,DOB,SSN)
    dynamodb = boto3.resource('dynamodb')
    table_name = environ.get("TABLE_NAME")
    table = dynamodb.Table(table_name)

    #print("event pathParams: ",event["pathParameters"])
    print("event pathParams input",event["pathParameters"]["input"])
    #print(type(event["pathParameters"]["input"]))
    inputs = json.loads( event["pathParameters"]["input"] )

    customer_id = inputs["customer_id"]
    initial_balance = int(inputs["initial_balance"])
    full_legal_name = inputs["full_legal_name"]
    dob = inputs["DOB"]
    ssn = inputs["SSN"]

    new_user = {
                'customer_id'          : customer_id,
                'balance'              : initial_balance,
                'Name'                 : full_legal_name,
                'D.O.B'                : dob,
                'SSN'                  : ssn
                }
                
    response = table.put_item( 
        Item = new_user ,
        #only add to the table if the attribute does not exist
        ConditionExpression = 'attribute_not_exists(customer_id)',
        )
    
    return response

#Test commands for http request
#{"customer_id":"originalHTTP","initial_balance":"1000000","full_legal_name":"OriginalHTTPUser","DOB":"08/13/2021","SSN":"123456789"}



#{"customer_id":"originalHTTP","initial_balance":"1000000","full_legal_name":"OriginalHTTPUser","DOB":"08/13/2021"}