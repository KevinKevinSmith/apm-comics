# getBook.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to get the attributes of a book

import boto3
from botocore.exceptions import ClientError

# Definitions for DynamoDB Table
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
table = dynamodb.Table('apm-comics-prod')


def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    Returns all of the attributes for an item with a specified ISBN
    :param event:
    :param context:
    :return:
    """
    global dynamodb
    global table
    try:
        response = table.get_item(
            Key={
                'itemtype': "book",
                'itemid': str(event['isbn'])
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {}
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return {}


if __name__ == "__main__":
    """
    Main method which can be used for testing locally against DynamoDB
    """
    event = {"isbn": "9780785125211"}
    print(lambda_handler(event, None))
