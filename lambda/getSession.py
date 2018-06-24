# getSession.py
# APM Comics Demo
# Austin Krauza- June 2018
# Lambda function to manage the sessions

from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import datetime
import uuid
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


def lambda_handler(event, context):
    """
    Function handler. The "main" or "driver" of the Lambda Method.
    The API Gateway will pass a POST of an action, which will be handled accordingly
    :param event:
    :param context:
    :return:
    """
    if 'email' in event:
        email = str(event['email'])
        new_session = generate_new_session(email)
        return {"sessionGUID": new_session['sessionGUID'], "sessionActive": new_session['sessionActive']}
    elif 'sessionGUID' in event:
        return get_session(event['sessionGUID'])


def generate_new_session(email):
    """
    Generates a new session for a provided customer/email
    :param email:
    :return:
    """
    global table
    global tableName
    date = datetime.datetime.now().strftime("%Y%m%d")
    uuid_str = str(uuid.uuid4())
    # Create a variable of 14 days from current date and time
    ttl = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%s')
    item_id = str(uuid_str + "|" + email + "|" + date)

    # Form a new session item
    itm = {'itemtype': "session", 'itemid': item_id, 'sessionActive': True, 'cart': "{}", 'sessionGUID': uuid_str,
           'ttl': int(ttl)}

    try:
        # Put the new session item into the table, and return it
        table.put_item(TableName=tableName, Item=itm)
        return itm
    except Exception as e:
        print(e)
        print("Unable to create new session")
        return {}


def get_session(guid):
    """
    Gets the session state for a specified Session GUID
    :param guid: Session GUID
    :return: dictionary with the session GUID and the state of the GUID
    """
    global table
    try:
        response = table.query(
            KeyConditionExpression=Key('itemtype').eq("session") & Key('itemid').begins_with(guid),
            # Order the return set in descending order by 'itemid'
            ScanIndexForward=False,
            ProjectionExpression="sessionActive, sessionGUID"
        )

        if ('Items' in response) & (len(response['Items']) > 0):
            return response['Items'][0]
        else:
            # If there are no items returned, the GUID is not valid, therefore the session is not active
            return {"sessionGUID": guid, "sessionActive": False}

    except ClientError as e:
        # print(event["body-json"])
        print(e.response['Error']['Message'])


if __name__ == "__main__":
    """
        Main method which can be used for testing locally against DynamoDB
    """
    event = {'email': 'krauza.austin@gmail.com'}
    print(lambda_handler(event, None))
    event = {'sessionGUID': '0151cfee-6eae-4cd1-9b18-e7bb6366105d'}
    print(lambda_handler(event, None))
    event = {'sessionGUID': '5acf515d-079d-4bdd-9e48-ae5d189abbb1'}
    print(lambda_handler(event, None))
