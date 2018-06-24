# getCart.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to manage the cart

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
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


# Lambda Function Handler
def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    The API Gateway will pass a POST of an action, which will be handled accordingly
    :param event:
    :param context:
    :return:
    """
    if event['action'] == "getcart":
        return get_cart(event['sessionGUID'])
    elif event['action'] == "additem":
        return add_item_cart(event['sessionGUID'], event['isbn'], event['quantity'])
    elif event['action'] == "checkitem":
        return check_item_cart(event['sessionGUID'], event['isbn'])


def add_item_cart(session_guid, isbn, quantity):
    """
    Adds an item (by inserting it into DynamoDB) into the cart, as passed by the POST call
    :param session_guid: GUID of the session to insert the item into
    :param isbn: Item ID to insert into the cart
    :param quantity: Number of items to be added to the cart
    :return: Returns dictionary of "new attributes" of the updated object into DynamoDB
    """
    global dynamodb
    global table
    # An update item is used here because an upsert (rather than an insert) is needed.
    # If an existing object with the same keys are found, it is updated. If not, the object is inserted
    newval = table.update_item(
        Key={
            "itemtype": "cart",
            "itemid": str(session_guid) + "|" + str(isbn)
        },
        UpdateExpression="set quantity = :q , isbn = :isbn, iteminfo =  :details",
        ExpressionAttributeValues={
            ':q': int(quantity),
            ':isbn': str(isbn),
            ':details': get_item(str(isbn))
        },
        ReturnValues="ALL_NEW"
    )
    return newval['Attributes']


def get_cart(session_guid):
    """
    Returns the items that are currently in a cart for a given SessionID
    :param session_guid: SessionID
    :return: A dictionary with the isbn, quantity and JSON of information for each object "in the cart"
    """
    response = table.query(
        KeyConditionExpression=Key('itemtype').eq("cart") & Key('itemid').begins_with(session_guid),
        ScanIndexForward=False,
        FilterExpression=Attr('quantity').gt(0),
        ProjectionExpression="isbn, quantity, iteminfo"
    )

    if ('Items' in response) & (len(response['Items']) > 0):

        return response['Items']

    else:
        return {}


def check_item_cart(session_guid, isbn):
    """
    Checks whether a specified item is in the cart
    :param session_guid: GUID of the session to search
    :param isbn: isbn of the item to search
    :return: a dictionary with the isbn, and quantity of the item in the cart (0 if not found)
    """
    try:
        response = table.get_item(
            Key={
                "itemtype": "cart",
                "itemid": str(session_guid) + "|" + str(isbn)
            },
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return {"isbn": isbn, "quantity": response['Item']['quantity']}
        else:
            data = {"isbn": isbn, "quantity": 0}
            return data


def get_item(isbn):
    """
    Gets information about a given item from the DynamoDB Table
    :param isbn: Item to be returned
    :return: Dictionary containing the item information
    """
    try:
        response = table.get_item(
            Key={
                'itemtype': "book",
                'itemid': str(isbn)
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            item = response['Item']
            return item
        else:
            data = {}
            return data


if __name__ == "__main__":
    """
    Main method which can be used for testing locally against DynamoDB
    """
    event = {"action": "additem", 'sessionGUID': '0151cfee-6eae-4cd1-9b18-e7bb6366105a', "isbn": "9780785138655",
             "quantity": "22"}
    print(lambda_handler(event, None))
    event = {"action": "getcart", 'sessionGUID': '0151cfee-6eae-4cd1-9b18-e7bb6366105a'}
    print(lambda_handler(event, None))
    event = {"action": "checkitem", 'sessionGUID': '0151cfee-6eae-4cd1-9b18-e7bb6366105a', "isbn": "9780785138655"}
    print(lambda_handler(event, None))
    event = {"action": "checkitem", 'sessionGUID': '0151cfee-6eae-4cd1-9b18-e7bb6366105a', "isbn": "9780785138655"}
    print(lambda_handler(event, None))
