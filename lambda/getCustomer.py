# getCustomer.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to manage the customers

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from botocore.exceptions import ClientError

# Definitions for DynamoDB Table
tableName = "apm-comics-prod"
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
table = dynamodb.Table(tableName)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    The API Gateway will pass a POST of an action, which will be handled accordingly
    :param event:
    :param context:
    :return:
    """
    global dynamodb
    global table
    if event['action'] == "get":
        return get_customer(event['email'])
    elif event['action'] == "create":
        cust_details = event['details']
        return create_customer(cust_details)


def create_customer(custdetails):
    """
    Adds a new customer to the database
    :param custdetails: Dictionary with Customer Details
    :return: Dictionary with the email address of the customer, and the create status
    """
    global dynamodb
    global table
    # Removes any keys from the dictionary for which there are no value
    r = {k: v for k, v in custdetails.items() if v != ''}
    try:
        # If the dictionary contains an email, which is the primary key for the Dynamo table
        if "email" in r:
            r['itemtype'] = "customer"
            r['itemid'] = r['email']
            table.put_item(TableName='apm-comics-prod', Item=r)
            return {"email": r['email'], "status": "created"}
    except Exception as e:
        print(e)
        print("Unable to create new user")
        return {"email": r['email'], "status": "failed"}


def get_customer(email):
    """
    Returns details about a given customer
    :param email: Email of the customer to return
    :return: If the customer exists, return a dictionary with the email, status of exist, and name of the customer.
        Else, return a dictionary with the email and a status of nonexistant.
    """
    global dynamodb
    global table
    try:
        response = table.get_item(
            Key={
                'itemtype': "customer",
                'itemid': str(email)
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # Since we are calling "get_item", only one item can possibly be returned. Therefore, 'Item' will be in the
        # response, instead of 'Items' if multiple can be returned
        if 'Item' in response:
            item = response['Item']
            return {"email": email, "status": "exists", "first_name": item['first_name'],
                    "last_name": item['last_name']}
        else:
            return {"email": email, "status": "nonexistant"}


if __name__ == "__main__":
    """
    Main method which can be used for testing locally against DynamoDB
    """
    event = {'action': 'create',
             'details': {'city': 'Staten Island', 'zip': '10306', 'last_name': 'Krauza', 'first_name': 'Austin',
                         'address': '2900 Amboy Road',
                         'email': 'krauza.austin@gmail.com', 'phone': '718-987-2900', 'state': 'New York'}}
    print(lambda_handler(event, None))
