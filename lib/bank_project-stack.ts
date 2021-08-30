import * as cdk from '@aws-cdk/core';
import { Bucket } from '@aws-cdk/aws-s3';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import * as lambda from '@aws-cdk/aws-lambda';
import {CorsHttpMethod, HttpApi, HttpMethod} from '@aws-cdk/aws-apigatewayv2';
import {LambdaProxyIntegration} from '@aws-cdk/aws-apigatewayv2-integrations' ;
import { Integration } from '@aws-cdk/aws-apigateway';
import { Handler } from '@aws-cdk/aws-lambda';

export class BankProjectStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const testBucket = new Bucket(this, 'BankInterfaceBucket',{
      bucketName: 'xavier-double-ipa-bucket1'
    
    });

    /* create the dynamo DB table for bank account information */
    // *this* table is contained int he context of the stack
    const bankTable = new dynamodb.Table(this, 'customer-accounts', {
      partitionKey: { name: 'customer_id', type: dynamodb.AttributeType.STRING }
    });
    //CREATE ACCOUNT LAMBDA
    const fnCreateAccount = new lambda.Function(this, 'fnCreateAccount', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'create_account.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/create_account"),
    });
  
    bankTable.grantReadWriteData(fnCreateAccount)
    fnCreateAccount.addEnvironment("TABLE_NAME",bankTable.tableName)
    
    //DELETE ACCOUNT LAMBDA
    const fnRemoveAccount = new lambda.Function(this, 'fnRemoveAccount', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'remove_account.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/remove_account"),
    });

    bankTable.grantReadWriteData(fnRemoveAccount)
    fnRemoveAccount.addEnvironment("TABLE_NAME",bankTable.tableName)
    
    //CHANGE USER ID LAMBDA
    const fnChangeUserID = new lambda.Function(this, 'fnChangeUserID', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'change_userID.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/change_userID"),
    });

    bankTable.grantReadWriteData(fnChangeUserID)
    fnChangeUserID.addEnvironment("TABLE_NAME",bankTable.tableName)

    const fnDeposit = new lambda.Function(this, 'fnDeposit', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'deposit.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/deposit"),
    });

    bankTable.grantWriteData(fnDeposit)
    fnDeposit.addEnvironment("TABLE_NAME",bankTable.tableName)

    //RETRIEVE USER INFO LAMBDA
    const fnRetrieveAccountInfo = new lambda.Function(this, 'fnRetrieveAccountInfo', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'retrieve_account_info.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/retrieve_account_info"),
    });

    bankTable.grantReadData(fnRetrieveAccountInfo)
    fnRetrieveAccountInfo.addEnvironment("TABLE_NAME",bankTable.tableName)

    const fnRetrieveAccountDetail = new lambda.Function(this, 'fnRetrieveAccountDetail', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'retrieve_account_detail.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/retrieve_account_detail"),
    });

    bankTable.grantReadData(fnRetrieveAccountDetail)
    fnRetrieveAccountDetail.addEnvironment("TABLE_NAME",bankTable.tableName)

    //Special role to call other lambda functions

    const fnTransferBalance = new lambda.Function(this, 'fnTransferBalance', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'transfer_balance.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/transfer_balance"),
    });
    //SPECIAL PERMISSION TO CALL OTHER FUNCTION
    fnRetrieveAccountDetail.grantInvoke(fnTransferBalance)
    fnRetrieveAccountInfo.grantInvoke(fnTransferBalance)
    bankTable.grantReadWriteData(fnTransferBalance)

    fnTransferBalance.addEnvironment("TABLE_NAME",bankTable.tableName)

    const fnWithdraw = new lambda.Function(this, 'fnWithdraw', {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: 'withdraw.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/withdraw"),
    });

    const fnGetUsers = new lambda.Function(this,'fnGetUsers',{
      runtime: lambda.Runtime.PYTHON_3_7,
      handler : 'get_users.handler',
      code: lambda.Code.fromAsset("./interface_py_lambdas/get_users")
    });
    fnGetUsers.addEnvironment("TABLE_NAME",bankTable.tableName)
    bankTable.grantReadData(fnGetUsers)

    //SPECIAL PERMISSION TO CALL OTHER FUNCTION
    fnRetrieveAccountDetail.grantInvoke(fnWithdraw)
    fnTransferBalance.grantInvoke(fnWithdraw)
    fnRetrieveAccountInfo.grantInvoke(fnWithdraw)
    //
    bankTable.grantReadWriteData(fnWithdraw)
    fnWithdraw.addEnvironment("TABLE_NAME",bankTable.tableName)

    
    
    
    //API Gateway

    const httpApi = new HttpApi(this, 'bank-api', {
      description: 'HTTP API abstraction for banking interface',
      corsPreflight: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: [
          CorsHttpMethod.OPTIONS,
          CorsHttpMethod.GET,
          CorsHttpMethod.POST,
          CorsHttpMethod.PUT,
          CorsHttpMethod.PATCH,
          CorsHttpMethod.DELETE,
        ],
        allowCredentials: true,
      },
    });

    //Routes for each of the lambda functions

    //√
    httpApi.addRoutes({
      path: '/users',
      methods:[HttpMethod.GET],
      integration: new LambdaProxyIntegration({
        handler: fnGetUsers,
      }),
    })
    
    //√
    httpApi.addRoutes({
                            //{input} = {customer_id,initial_balance,full_legal_name,DOB,SSN}
      path: '/users/add/{input}',
      methods: [HttpMethod.GET,HttpMethod.POST],
      integration: new LambdaProxyIntegration({
        handler: fnCreateAccount,
      }),
    });

    //√
    httpApi.addRoutes({
                              //{input} = {customer_id}
      path: '/users/remove/{input}',
      methods: [HttpMethod.GET, HttpMethod.DELETE],
      integration: new LambdaProxyIntegration({
        handler: fnRemoveAccount,
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {customer_id,amount}
      path: '/users/deposit_to/{input}',
      methods: [HttpMethod.GET,HttpMethod.PATCH],
      integration: new LambdaProxyIntegration({
        handler: fnDeposit,
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {customer_id,new_id}     
      path: '/users/change_userID/{input}',
      methods: [HttpMethod.POST, HttpMethod.GET, HttpMethod.DELETE],
      integration: new LambdaProxyIntegration({
        handler: fnChangeUserID,
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {customer_id,amount_withdraw}
      path: '/users/withdraw_from/{input}',
      methods: [HttpMethod.GET,HttpMethod.PATCH,HttpMethod.PUT],
      integration: new LambdaProxyIntegration({
        handler: fnWithdraw
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {customer_id,required_info
      path: '/users/retrieve_customer_detail/{input}',
      methods: [HttpMethod.GET],
      integration: new LambdaProxyIntegration({
        handler: fnRetrieveAccountDetail
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {customer_id}
      path: '/users/retrieve_customer_info/{input}',
      methods: [HttpMethod.GET],
      integration: new LambdaProxyIntegration({
        handler: fnRetrieveAccountInfo
      }),
    });

    //√
    httpApi.addRoutes({
                            // {input} = {user_withdraw,user_deposit,amount)
      path: '/users/transfer/{input}',
      methods: [HttpMethod.GET, HttpMethod.PATCH ],
      integration: new LambdaProxyIntegration({
        handler: fnTransferBalance
      }),
    })



  }

}
