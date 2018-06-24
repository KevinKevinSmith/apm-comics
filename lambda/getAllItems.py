# getAllItems.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to get all of the items in the table

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Definitions for DynamoDB Table
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
table = dynamodb.Table('apm-comics-prod')


def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    Returns all of the objects with an 'itemtype' of "book"
    :param event:
    :param context:
    :return:
    """
    global dynamodb
    global table
    try:
        response = table.query(
            TableName='apm-comics-prod',
            KeyConditionExpression=Key('itemtype').eq("book")
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {}
    else:
        items = response['Items']
        return items


if __name__ == "__main__":
    """
    Main method which can be used for testing locally against DynamoDB
    """
    print(lambda_handler(None, None))
